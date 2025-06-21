# -*- coding: utf-8 -*-
"""
🩺 MediMate - AI Medical Consultation Backend API
(Version 8: Unified Chat Endpoint for Text & Audio)
"""

# 1. Import Required Libraries
import logging
import os
import sys
import json
from typing import List, Tuple, Generator, Dict
from datetime import datetime
import tempfile
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("MediMateAPI")

# Third-party libraries
try:
    from flask import Flask, request, jsonify, Response, stream_with_context, send_file
    from flask_cors import CORS
    from dotenv import load_dotenv
    from openai import OpenAI
    from fpdf import FPDF
except ImportError as e:
    logger.error(f"❌ Critical import error: {e}. Please run 'pip install flask python-dotenv openai fpdf2 flask-cors'.")
    sys.exit(1)

# Local transcription requires the whisper library
try:
    import whisper
    from whisper.audio import SAMPLE_RATE
    from subprocess import run, CalledProcessError
    import numpy as np
except ImportError:
    logger.error("❌ Whisper library not found. Please run 'pip install openai-whisper numpy'")
    sys.exit(1)

# Special handling for Ollama
try:
    import ollama
except ImportError:
    logger.warning("⚠️ Ollama import failed. Local models will not be available.")
    ollama = None

# Load environment variables FROM .env file
load_dotenv()


# 2. Configuration Settings
class Config:
    FFMPEG_PATH = os.getenv("FFMPEG_PATH")
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "gemma:7b")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.2-9b-instruct:free")
    OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    LOCAL_WHISPER_MODEL = os.getenv("LOCAL_WHISPER_MODEL", "base")
    SERVER_PORT = int(os.getenv("SERVER_PORT", "7861"))
    AI_METHOD = os.getenv("AI_METHOD", "auto")
    MAX_HISTORY = int(os.getenv("MAX_HISTORY", "10"))
    CONVERSATION_DIR = os.getenv("CONVERSATION_DIR", "consultations")
    ENABLE_PDF_EXPORT = os.getenv("ENABLE_PDF_EXPORT", "true").lower() == "true"
    EMERGENCY_MODE = os.getenv("EMERGENCY_MODE", "true").lower() == "true"


# --- vvv MONKEY PATCH SECTION vvv ---
def patched_load_audio(file: str, sr: int = SAMPLE_RATE):
    if not Config.FFMPEG_PATH or not os.path.exists(os.path.join(Config.FFMPEG_PATH, "ffmpeg.exe")):
        raise FileNotFoundError(
            f"FFMPEG_PATH is not set or ffmpeg.exe not found in '{Config.FFMPEG_PATH}'. "
            "Please set the correct path to the ffmpeg 'bin' directory in your .env file."
        )
    ffmpeg_executable = os.path.join(Config.FFMPEG_PATH, "ffmpeg.exe")
    logger.info(f"Using ffmpeg executable at: {ffmpeg_executable}")
    cmd = [
        ffmpeg_executable, "-nostdin", "-threads", "0", "-i", file,
        "-f", "s16le", "-ac", "1", "-acodec", "pcm_s16le", "-ar", str(sr), "-"
    ]
    try:
        out = run(cmd, capture_output=True, check=True).stdout
    except CalledProcessError as e:
        raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e
    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0

whisper.audio.load_audio = patched_load_audio
logger.info("✅ Monkey-patch for whisper.audio.load_audio has been applied.")
# --- ^^^ END OF MONKEY PATCH ^^^ ---


# 5. Local Transcription Service
class LocalWhisper:
    def __init__(self, model_name="base"):
        self.model = None
        self.model_name = model_name
        try:
            logger.info(f"🎤 Loading local Whisper model '{model_name}'... This may take a moment.")
            self.model = whisper.load_model(model_name)
            logger.info("✅ Local Whisper model loaded successfully.")
        except Exception as e:
            logger.error(f"❌ Failed to load local Whisper model: {e}")

    def transcribe(self, audio_filepath: str) -> str:
        if not self.model:
            raise RuntimeError("Whisper model is not available or failed to load.")
        logger.info(f"Transcribing '{audio_filepath}' with local model...")
        result = self.model.transcribe(audio_filepath, fp16=False)
        logger.info(f"Transcription complete. Raw result: {result['text']}")
        return result["text"]

# ... other classes are unchanged ...
class AIService:
    def __init__(self):
        self.openrouter_client = None; self.ollama_available = False; self.openrouter_available = False; self.selected_method = None
        self.initialize_services()
    def initialize_services(self):
        logger.info("🔍 Checking AI service connections...")
        if Config.OPENROUTER_API_KEY:
            try: self.openrouter_client = OpenAI(base_url=Config.OPENROUTER_BASE_URL, api_key=Config.OPENROUTER_API_KEY); self.openrouter_available = True; logger.info("✅ OpenRouter client initialized for Chat.")
            except Exception as e: logger.error(f"❌ Failed to initialize OpenRouter client: {e}")
        if ollama:
            try: requests.get(f"{Config.OLLAMA_HOST}/api/version", timeout=5); self.ollama_available = True; logger.info("✅ Ollama is running and accessible!")
            except requests.exceptions.RequestException: logger.warning("❌ Cannot connect to Ollama.")
        if Config.AI_METHOD == "auto": self.selected_method = "ollama" if self.ollama_available else "openrouter" if self.openrouter_available else None
        else: self.selected_method = Config.AI_METHOD if (Config.AI_METHOD == "openrouter" and self.openrouter_available) or (Config.AI_METHOD == "ollama" and self.ollama_available) else None
        if self.selected_method: logger.info(f"🎯 Using AI Method for Chat: {self.selected_method.upper()}")
        else: logger.error("❌ No Chat AI services available!")
    def get_chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> Generator[str, None, None]:
        if self.selected_method == "ollama": yield from self._get_ollama_completion(messages, **kwargs)
        elif self.selected_method == "openrouter": yield from self._get_openrouter_completion(messages, **kwargs)
        else: yield "❌ No AI service is available."
    def _get_ollama_completion(self, messages, **kwargs) -> Generator[str, None, None]:
        try:
            for chunk in ollama.chat(model=Config.DEFAULT_MODEL, messages=messages, stream=True, options=kwargs):
                if 'message' in chunk and 'content' in chunk['message']: yield chunk['message']['content']
        except Exception as e: logger.error(f"❌ Ollama error: {e}"); yield f"❌ Ollama error: {e}"
    def _get_openrouter_completion(self, messages, **kwargs) -> Generator[str, None, None]:
        try:
            response = self.openrouter_client.chat.completions.create(model=Config.OPENROUTER_MODEL, messages=messages, stream=True, **kwargs)
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content: yield chunk.choices[0].delta.content
        except Exception as e: logger.error(f"❌ OpenRouter error: {e}"); yield f"❌ OpenRouter error: {e}"

class MedicalSystemPrompts:
    BASE = """You are Dr. MediMate, an experienced physician providing direct medical consultations..."""; EMERGENCY = BASE + """\n\nIMPORTANT: You are handling a potential medical emergency..."""; PEDIATRIC = BASE + """\n\nSPECIAL CONSIDERATIONS: You are treating a pediatric patient..."""; CHRONIC = BASE + """\n\nFOCUS: You are managing a patient with chronic condition(s)..."""
    @classmethod
    def get_prompt(cls, patient_type="standard", is_emergency=False):
        if is_emergency: return cls.EMERGENCY
        if patient_type == "pediatric": return cls.PEDIATRIC
        if patient_type == "chronic": return cls.CHRONIC
        return cls.BASE

class MedicalConsultation:
    def __init__(self, ai_service: AIService): self.ai_service = ai_service
    def process_user_message(self, message: str, history: List[Tuple[str, str]], patient_type: str = "auto") -> Generator[str, None, None]:
        is_emergency = any(keyword in message.lower() for keyword in ["emergency", "severe pain", "chest pain"]) if Config.EMERGENCY_MODE else False; final_patient_type = patient_type if patient_type != "auto" else ("pediatric" if any(i in message.lower() for i in ["child", "baby"]) else "standard"); system_prompt = MedicalSystemPrompts.get_prompt(patient_type=final_patient_type, is_emergency=is_emergency); conversation = [{"role": "system", "content": system_prompt}]
        for user_msg, assistant_msg in history[-Config.MAX_HISTORY:]: conversation.extend([{"role": "user", "content": user_msg}, {"role": "assistant", "content": assistant_msg}])
        conversation.append({"role": "user", "content": message})
        if is_emergency: yield "⚠️ **POTENTIAL EMERGENCY DETECTED**... \n\n"
        yield from self.ai_service.get_chat_completion(conversation, temperature=0.7, max_tokens=1500)

class PDFExporter:
    @staticmethod
    def export_to_pdf(history: List[Tuple[str, str]], patient_type: str, is_emergency: bool) -> str:
        if not Config.ENABLE_PDF_EXPORT: raise RuntimeError("PDF export is disabled."); os.makedirs(Config.CONVERSATION_DIR, exist_ok=True); fd, filepath = tempfile.mkstemp(suffix=".pdf", prefix="MediMate_", dir=Config.CONVERSATION_DIR); os.close(fd); pdf = FPDF(); pdf.add_page(); pdf.set_font("Arial", "B", 16); pdf.cell(0, 10, "MediMate Medical Consultation Record", ln=True, align="C"); pdf.set_font("Arial", "", 12); pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True); pdf.cell(0, 10, f"Patient Profile: {patient_type.capitalize()}", ln=True)
        if is_emergency: pdf.set_text_color(255, 0, 0); pdf.cell(0, 10, "Status: Potential Emergency Flagged", ln=True); pdf.set_text_color(0, 0, 0)
        pdf.ln(10)
        for user_msg, assistant_msg in history:
            pdf.set_font("Arial", "B", 11); pdf.multi_cell(0, 5, "Patient:"); pdf.set_font("Arial", "", 11); pdf.multi_cell(0, 5, user_msg.encode('latin-1', 'replace').decode('latin-1')); pdf.ln(3)
            pdf.set_font("Arial", "B", 11); pdf.multi_cell(0, 5, "Dr. MediMate:"); pdf.set_font("Arial", "", 11); pdf.multi_cell(0, 5, assistant_msg.encode('latin-1', 'replace').decode('latin-1')); pdf.ln(8)
        pdf.output(filepath); logger.info(f"✅ Consultation exported to temporary file: {filepath}"); return filepath

# 8. Flask API Implementation
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, resources={r"/api/*": {"origins": "*"}})

ai_service = AIService()
local_whisper = LocalWhisper(model_name=Config.LOCAL_WHISPER_MODEL)
consultation_manager = MedicalConsultation(ai_service)


@app.route("/api/status", methods=["GET"])
def get_status():
    return jsonify({
        "service_status": "running",
        "active_chat_method": ai_service.selected_method,
        "local_transcription_model": local_whisper.model_name if local_whisper.model else "Not Available"
    })


@app.route("/api/chat", methods=["POST"])
def unified_chat():
    """
    Unified chat endpoint that accepts multipart/form-data.
    It can process a user's query from either a text field or an audio file.

    Form Fields:
    - history (string): A JSON string representing the conversation history, e.g., '[["user msg", "ai reply"]]'.
    - patient_type (string, optional): e.g., 'pediatric', 'chronic'. Defaults to 'auto'.
    - message (string, optional): The user's text message.
    - audio_file (file, optional): The user's audio message.

    The endpoint prioritizes 'audio_file' over 'message' if both are provided.
    """
    if not ai_service.selected_method:
        return jsonify({"error": "No AI chat service is available."}), 503

    # --- 1. Extract form data ---
    try:
        history_str = request.form.get('history', '[]')
        history = json.loads(history_str)
        if not isinstance(history, list):
            raise ValueError("History must be a JSON array of [user, assistant] pairs.")
    except (json.JSONDecodeError, ValueError) as e:
        logger.error(f"Invalid history format received: {history_str}")
        return jsonify({"error": f"Invalid 'history' format. Must be a valid JSON array string. Error: {e}"}), 400

    patient_type = request.form.get('patient_type', 'auto')
    message = None

    # --- 2. Process input: prioritize audio file ---
    if 'audio_file' in request.files:
        logger.info("🎙️ Received audio file for transcription and chat.")
        file = request.files['audio_file']
        if file.filename == '':
            return jsonify({"error": "No audio file selected in 'audio_file' part."}), 400

        if not local_whisper or not local_whisper.model:
            return jsonify({"error": "Local audio transcription service is not available to process the file."}), 503

        tmp_path = None
        try:
            suffix = os.path.splitext(file.filename)[1] or '.wav' # Ensure a suffix
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                tmp_path = tmp_file.name
                file.save(tmp_path)
            message = local_whisper.transcribe(tmp_path)
            logger.info(f"Transcription successful. Message: '{message}'")
        except Exception as e:
            logger.error(f"❌ Error during audio processing: {e}", exc_info=True)
            return jsonify({"error": f"Audio processing failed: {e}"}), 500
        finally:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                    logger.info(f"🗑️ Cleaned up temporary audio file: {tmp_path}")
                except Exception as e:
                    logger.error(f"❌ Failed to clean up temporary file {tmp_path}: {e}")

    elif 'message' in request.form:
        logger.info("💬 Received text message for chat.")
        message = request.form['message']

    # --- 3. Validate that we have a message ---
    if message is None:
        return jsonify({"error": "Request form must contain either a 'message' text field or an 'audio_file' part."}), 400

    # --- 4. Generate and stream the chat response ---
    def generate_stream():
        try:
            for token in consultation_manager.process_user_message(message, history, patient_type):
                yield json.dumps({"token": token}) + '\n'
        except Exception as e:
            logger.error(f"Error during stream generation: {e}", exc_info=True)
            yield json.dumps({"error": str(e)}) + '\n'

    return Response(stream_with_context(generate_stream()), mimetype="application/x-json-stream; charset=utf-8")


@app.route("/api/export/pdf", methods=["POST"])
def export_pdf():
    if not Config.ENABLE_PDF_EXPORT:
        return jsonify({"error": "PDF export is disabled."}), 501

    data = request.get_json()
    if not data or 'history' not in data:
        return jsonify({"error": "Request must be JSON with 'history'."}), 400

    filepath = None
    try:
        filepath = PDFExporter.export_to_pdf(
            data['history'],
            data.get('patient_type', 'standard'),
            data.get('is_emergency', False)
        )
        return send_file(
            filepath,
            as_attachment=True,
            download_name=f"MediMate_Consultation_{datetime.now().strftime('%Y%m%d')}.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        logger.error(f"❌ Failed to generate or send PDF: {e}")
        return jsonify({"error": f"Failed to export PDF: {e}"}), 500
    finally:
        if filepath and os.path.exists(filepath):
            os.remove(filepath)

# 9. Main Execution
if __name__ == "__main__":
    if not ai_service.selected_method:
        logger.error("="*60 + "\n❌ MediMate cannot start - No AI chat backend is available.\n" + "="*60)
        sys.exit(1)
    logger.info("="*60 + f"\n👨‍⚕️ Dr. MediMate Backend is running on http://0.0.0.0:{Config.SERVER_PORT}\n" + "="*60)
    app.run(host="0.0.0.0", port=Config.SERVER_PORT, debug=False)