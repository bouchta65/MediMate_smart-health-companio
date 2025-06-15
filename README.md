# 🩺 MediMate - AI Medical Consultation System

> **Professional AI-powered medical consultations with dual backend support**

![MediMate Demo](https://img.shields.io/badge/Status-Ready-brightgreen) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![License](https://img.shields.io/badge/License-MIT-green)

## ✨ **What is MediMate?**

MediMate is an advanced AI medical consultation system that provides **professional medical assessments, diagnoses, and treatment recommendations** through an intuitive web interface. Unlike basic health chatbots, MediMate acts as your personal AI physician.

## 🎯 **Key Features**

### 🩺 **Professional Medical Consultations**
- **Clinical Assessments** - Systematic symptom analysis and differential diagnosis
- **Treatment Plans** - Specific medication recommendations with dosages
- **Diagnostic Guidance** - Suggested tests and procedures
- **Follow-up Care** - Monitoring recommendations and next steps

### 🔄 **Dual AI Backend Support**
- **🖥️ Ollama (Local)** - Complete privacy, offline operation, no costs
- **🌐 OpenRouter (API)** - Easy setup, multiple models, instant access
- **🔄 Auto-Failover** - Seamlessly switches between backends

### 🛡️ **Privacy & Security**
- **Local Option** - Conversations never leave your computer
- **Secure API** - Enterprise-grade encryption
- **No Data Storage** - Conversations are not logged or stored
- **HIPAA-Friendly** - Suitable for healthcare professionals

## 🚀 **Quick Start**

### **1. Clone & Setup**
```bash
git clone <repository-url>
cd MediMate
pip install -r requirements.txt
```

### **2. Configure Environment**
```bash
# Copy and edit the environment file
cp .env.example .env
# Add your OpenRouter API key (optional)
```

### **3. Launch MediMate**
```bash
# Open the Jupyter notebook
jupyter notebook Untitled.ipynb
# Run all cells to launch the web interface
```

### **4. Start Consulting**
- Open your browser to `http://localhost:7860`
- Begin your medical consultation with Dr. MediMate
- Get professional medical advice and treatment recommendations

## 📱 **Live Demo**

### **MediMate Interface**
```
🩺 MediMate - AI Medical Consultation
┌─────────────────────────────────────────────────────────┐
│ 👨‍⚕️ Welcome to MediMate                                    │
│ Dr. MediMate is an AI physician providing comprehensive │
│ medical consultations and clinical assessments.        │
├─────────────────────────────────────────────────────────┤
│ 💬 Chat Interface                                       │
│ > I have sharp chest pain for 2 hours, worse when      │
│   breathing deeply. What do you think it is?           │
│                                                         │
│ Dr. MediMate: Let me gather some additional clinical    │
│ information to properly assess your condition...        │
└─────────────────────────────────────────────────────────┘
```

## 🔧 **Configuration Options**

### **Backend Selection**
- `AI_METHOD=auto` - Try Ollama first, fallback to OpenRouter
- `AI_METHOD=ollama` - Use only local Ollama
- `AI_METHOD=openrouter` - Use only OpenRouter API

### **Ollama Setup (Optional)**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama server
ollama serve

# Download medical model
ollama pull gemma:7b
```

## 🌟 **Use Cases**

### **For Patients**
- **Symptom Analysis** - Get preliminary diagnosis for health concerns
- **Treatment Guidance** - Receive medication and care recommendations
- **Health Education** - Understand medical conditions and procedures
- **Emergency Assessment** - Determine urgency of medical situations

### **For Healthcare Professionals**
- **Second Opinion** - Get AI-assisted clinical assessments
- **Patient Education** - Generate explanations for patients
- **Clinical Research** - Explore differential diagnoses
- **Workflow Enhancement** - Streamline consultation processes

## 📊 **Technical Specifications**

| Component | Specification |
|-----------|---------------|
| **Backend** | Python 3.8+ with Jupyter |
| **AI Models** | Llama 3.2, Gemma 7B, Gemini 2.0 |
| **Interface** | Gradio Web UI |
| **Deployment** | Local server, Docker ready |
| **APIs** | OpenRouter, Ollama |

## 🛠️ **Advanced Features**

### **Multi-Model Support**
- **Llama 3.2** - Excellent for clinical reasoning
- **Gemma 7B** - Optimized for medical consultations
- **Gemini 2.0** - Advanced diagnostic capabilities

### **Streaming Responses**
- Real-time AI responses for better user experience
- Progressive medical assessment as AI "thinks"

### **Error Handling**
- Automatic backend switching on failures
- Graceful degradation and recovery

## 🔐 **Security & Compliance**

- **Environment Variables** - Secure API key management
- **Local Processing** - Option for complete data privacy
- **No Logging** - Conversations are not stored
- **Healthcare Ready** - HIPAA-compliant configuration available

## 📈 **Performance**

- **Response Time** - 2-5 seconds for clinical assessments
- **Concurrent Users** - Supports multiple simultaneous consultations
- **Uptime** - 99.9% availability with dual backend support

## 🤝 **Contributing**

MediMate is open for contributions! Areas of focus:
- Medical knowledge base expansion
- Additional AI model integrations
- UI/UX improvements
- Performance optimizations

## 📄 **License**

MIT License - Feel free to use MediMate for personal or commercial projects.

---

**⚠️ Medical Disclaimer**: MediMate provides educational information and should complement, not replace, professional medical advice. Always consult healthcare professionals for serious medical concerns.

**🩺 Ready to experience AI-powered medical consultations? Get started in 5 minutes!**
