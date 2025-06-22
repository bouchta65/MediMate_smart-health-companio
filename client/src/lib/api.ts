// api.ts
"use client"

import axios from "axios"

const API_BASE_URL = import.meta.env.VITE_API_URL || "https://cbaf-34-16-245-59.ngrok-free.app";

// Axios is great for standard JSON/blob requests
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // Increased timeout for potentially long PDF generation
})

export interface BackendStatus {
  service_status: string
  active_chat_method: string
  local_transcription_model: string
}

// Keep a simple request type for clarity
export interface ChatRequest {
  message?: string
  audioFile?: Blob
  // History format matches backend: [ [user, ai], [user, ai] ]
  history: [string, string][] 
  patient_type: string
}

export interface StreamCallbacks {
  onToken: (token: string) => void
  onComplete: () => void
  onError: (error: string) => void
}

export interface ExportRequest {
  history: [string, string][]
  patient_type: string
  is_emergency: boolean
}

export async function checkBackendStatus(): Promise<BackendStatus> {
  const response = await api.get("/api/status")
  return response.data
}

// ** Rewritten for streaming with Fetch API **
export async function streamChatCompletion(
    request: ChatRequest,
    callbacks: StreamCallbacks
): Promise<void> {
  const formData = new FormData();
  formData.append("message", request.message || "");

  if (request.audioFile) {
    formData.append("audio_file", request.audioFile, "audio.wav");
  }

  formData.append("history", JSON.stringify(request.history));
  formData.append("patient_type", request.patient_type);

  try {
    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }

    if (!response.body) {
      throw new Error("Response body is null");
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        // Process any remaining content in the buffer before completing
        if (buffer.trim()) {
          try {
            const parsed = JSON.parse(buffer);
            if (parsed.token) {
              callbacks.onToken(parsed.token);
            }
          } catch (e) {
            console.error("Failed to parse final buffer content:", buffer, e);
          }
        }
        break;
      }

      buffer += decoder.decode(value, { stream: true });

      // Process complete JSON objects (separated by newlines)
      let boundary;
      while ((boundary = buffer.indexOf('\n')) >= 0) {
        const line = buffer.substring(0, boundary).trim();
        buffer = buffer.substring(boundary + 1);

        if (!line) continue;

        try {
          const parsed = JSON.parse(line);
          if (parsed.error) {
            throw new Error(parsed.error);
          }
          if (parsed.token !== undefined) { // Check for undefined since token might be empty string
            callbacks.onToken(parsed.token);
          }
        } catch (e: any) {
          console.error("Failed to parse stream line:", line, e);
          callbacks.onError(`An error occurred while processing the response: ${e.message}`);
          return;
        }
      }
    }

    callbacks.onComplete();

  } catch (error: any) {
    console.error("Failed to send message:", error);
    callbacks.onError(error.message || "An unknown network error occurred.");
  }
}


export async function exportToPDF(request: ExportRequest): Promise<void> {
  try {
    const response = await api.post("/api/export/pdf", request, {
      responseType: "blob",
    })

    const blob = new Blob([response.data], { type: "application/pdf" })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement("a")
    link.href = url
    
    const date = new Date().toISOString().split("T")[0].replace(/-/g, "")
    link.download = `MediMate_Consultation_${date}.pdf`

    document.body.appendChild(link)
    link.click()
    
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)

  } catch (error: any) {
    // Try to parse the error blob
    if (error.response?.data instanceof Blob) {
      const errText = await error.response.data.text()
      try {
        const errJson = JSON.parse(errText)
        throw new Error(errJson.error || "Failed to export PDF")
      } catch {
        throw new Error("An unknown error occurred during PDF export.")
      }
    }
    throw new Error(error.response?.data?.error || "Failed to export PDF")
  }
}