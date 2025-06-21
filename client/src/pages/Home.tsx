"use client"

import type React from "react"
import { Stethoscope, Shield, Brain, Lock, Server, Heart, CheckCircle, UserCheck } from "lucide-react"
import { useTheme } from "../components/ThemeContext"
import HeaderCompo from "@/pages/components/Header";

const HomePage: React.FC = () => {
    const { theme } = useTheme()

    const features = [
        {
            icon: <Stethoscope className="w-8 h-8" />,
            title: "Professional Medical Consultations",
            description: "Clinical assessments, treatment plans, diagnostic guidance, and follow-up care recommendations.",
        },
        {
            icon: <Server className="w-8 h-8" />,
            title: "Dual AI Backend Support",
            description: "Ollama (Local) for privacy and OpenRouter (API) for easy access with auto-failover capability.",
        },
        {
            icon: <Shield className="w-8 h-8" />,
            title: "Privacy & Security",
            description: "Local processing option, secure API, no data storage, and HIPAA-friendly configuration.",
        },
        {
            icon: <Brain className="w-8 h-8" />,
            title: "Advanced AI Models",
            description: "Powered by Llama 3.2, Gemma 7B, and Gemini 2.0 for comprehensive medical analysis.",
        },
    ]

    const useCases = [
        {
            category: "For Patients",
            icon: <Heart className="w-6 h-6" />,
            items: [
                "Symptom Analysis & Preliminary Diagnosis",
                "Treatment Guidance & Medication Recommendations",
                "Health Education & Medical Understanding",
                "Emergency Assessment & Urgency Determination",
            ],
        },
        {
            category: "For Healthcare Professionals",
            icon: <UserCheck className="w-6 h-6" />,
            items: [
                "AI-Assisted Clinical Assessments",
                "Patient Education Material Generation",
                "Differential Diagnosis Exploration",
                "Workflow Enhancement & Consultation Support",
            ],
        },
    ]

    const techSpecs = [
        { label: "Backend", value: "Python 3.8+ with Jupyter" },
        { label: "AI Models", value: "Llama 3.2, Gemma 7B, Gemini 2.0" },
        { label: "Interface", value: "Gradio Web UI" },
        { label: "Deployment", value: "Local server, Docker ready" },
        { label: "APIs", value: "OpenRouter, Ollama" },
        { label: "Response Time", value: "2-5 seconds" },
        { label: "Uptime", value: "99.9% availability" },
    ]

    return (
        <div
            className={`min-h-screen transition-colors duration-300 ${
                theme === "dark"
                    ? "bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900 text-white"
                    : "bg-gradient-to-br from-white via-blue-50 to-white text-gray-900"
            }`}
        >
            <HeaderCompo/>

            {/* Hero Section */}
            <section className="relative py-20 px-4 sm:px-6 lg:px-8">
                <div className="max-w-5xl mx-auto text-center">
                    {/* Headline */}
                    <h1
                        className={`text-4xl sm:text-5xl md:text-6xl font-extrabold leading-tight ${
                            theme === 'dark' ? 'text-white' : 'text-gray-900'
                        }`}
                    >
                        <span className="block">AI that builds AI for</span>
                        <span className="block mt-2">
        <span className={`${theme === 'dark' ? 'text-white' : 'text-black'}`}>Building </span>
        <span className={`${theme === 'dark' ? 'text-cyan-400' : 'text-blue-600'}`}>Custom AI Agents</span>
      </span>
                    </h1>

                    {/* Subtext */}
                    <p
                        className={`mt-6 text-lg ${
                            theme === 'dark' ? 'text-gray-300' : 'text-gray-600'
                        }`}
                    >
                        Create fully customized AI agents for any task with just a few prompts
                    </p>

                    {/* Input form */}
                    <form
                        onSubmit={(e) => {
                            e.preventDefault();
                            // handle input submit here
                        }}
                        className="mt-10 flex justify-center items-center max-w-2xl mx-auto"
                    >
                        <input
                            type="text"
                            placeholder="What prompt do you want to create today?"
                            className={`flex-1 px-5 py-4 rounded-l-xl border'bg-white text-gray-900 border-gray-300 placeholder-gray-500 shadow-md focus:outline-none focus:ring-2 focus:ring-blue-500`}
                        />
                        <button
                            type="submit"
                            className={`p-4 rounded-r-xl transition ${
                                theme === 'dark'
                                    ? 'bg-white text-gray-900 hover:bg-gray-200'
                                    : 'bg-black text-white hover:bg-gray-800'
                            }`}
                            title="Send"
                        >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                className="h-5 w-5"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M5 12h14M12 5l7 7-7 7"
                                />
                            </svg>
                        </button>
                    </form>
                </div>
            </section>


        </div>
    )
}

export default HomePage
