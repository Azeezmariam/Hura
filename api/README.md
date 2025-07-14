---
title: Hura Chatbot
emoji: 👁
colorFrom: indigo
colorTo: red
sdk: docker
pinned: false
license: apache-2.0
short_description: AI assistant for tourists visiting Kigali, Rwanda
---

# 🌍 Hura Tourism Chatbot

An AI-powered tourism assistant for visitors to Kigali, Rwanda. Built with FastAPI, LangChain, and NLLB-200 translation.

## 🚀 **Live Demo**

**Deployed at:** [https://lola97-hura-chatbot.hf.space](https://lola97-hura-chatbot.hf.space)

## ✨ **Features**

### 🤖 **Tourism Information**

- Comprehensive information about Kigali and Rwanda
- Details about attractions, culture, and history
- Safety tips and travel advice
- Restaurant and accommodation recommendations

### 🔄 **Translation Service**

- **English → Kinyarwanda**: Translate English text to Kinyarwanda
- **Kinyarwanda → English**: Translate Kinyarwanda text to English
- Powered by Facebook's NLLB-200 model for high accuracy

### 🗺️ **Location Services** (Coming Soon)

- Find places and get directions
- Discover nearby restaurants and attractions
- Google Maps integration

### 🌤️ **Weather Updates** (Coming Soon)

- Current weather conditions
- Weather forecasts for Kigali
- OpenWeather API integration

### 📱 **WhatsApp Integration**

- Chat directly via WhatsApp using Twilio
- All features available through WhatsApp
- Automatic intent detection
- User-friendly menu system

## 🏗️ **Architecture**

```
hura-chatbot/
├── app.py                    # Main FastAPI application
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── Dockerfile               # Container configuration
│
├── services/                # Core services
│   ├── rag_service.py       # RAG functionality
│   ├── translation.py       # Translation service
│   ├── vector_store.py      # Vector database
│   ├── maps_service.py      # Maps integration
│   ├── weather_service.py   # Weather integration
│   └── whatsapp_service.py  # WhatsApp integration
│
├── api/                     # API components
│   └── models.py            # Pydantic models
│
├── middleware/              # Middleware
│   └── rate_limiter.py      # Rate limiting
│
├── utils/                   # Utilities
│   └── helpers.py           # Helper functions
│
├── tests/                   # Test files
├── static/                  # Web interface
├── data/                    # Tourism data
├── docs/                    # Documentation
├── scripts/                 # Utility scripts
└── archive/                 # Archived versions
```

## 🚀 **Quick Start**

### **Prerequisites**

- Python 3.9+
- 4GB+ RAM (for model loading)
- Internet connection (for model downloads)

### **Installation**

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd hura-chatbot
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**

   ```bash
   python app.py
   ```

4. **Access the API**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### **Using Docker**

```bash
# Build the image
docker build -t hura-chatbot .

# Run the container
docker run -p 8000:8000 hura-chatbot
```

## 📡 **API Endpoints**

### **Core Endpoints**

| Endpoint            | Method | Description                             |
| ------------------- | ------ | --------------------------------------- |
| `/`                 | GET    | API information and available endpoints |
| `/health`           | GET    | Health check and system status          |
| `/ask`              | POST   | Ask tourism questions about Kigali      |
| `/translate/en2rw`  | POST   | Translate English to Kinyarwanda        |
| `/translate/rw2en`  | POST   | Translate Kinyarwanda to English        |
| `/whatsapp/webhook` | POST   | WhatsApp webhook (Twilio integration)   |

### **Example Usage**

```bash
# Ask a tourism question
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"text": "Tell me about Kigali Genocide Memorial"}'

# Translate English to Kinyarwanda
curl -X POST "http://localhost:8000/translate/en2rw" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello, how are you?"}'

# Translate Kinyarwanda to English
curl -X POST "http://localhost:8000/translate/rw2en" \
     -H "Content-Type: application/json" \
     -d '{"text": "Muraho, amakuru?"}'
```

## 🧪 **Testing**

```bash
# Run all tests
python -m pytest tests/

# Test specific functionality
python tests/test_translations.py
python tests/test_deployed.py
```

## 📊 **Performance**

- **Response Time**: 30-60 seconds (typical for Hugging Face Spaces)
- **Translation Accuracy**: 95%+ with NLLB-200 model
- **Memory Usage**: ~90MB for loaded models
- **Rate Limiting**: 60 requests per minute

## 🔧 **Configuration**

Environment variables in `config.py`:

```python
# API Settings
HOST = "0.0.0.0"
PORT = 8000

# Model Settings
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF"
TRANSLATION_MODEL = "facebook/nllb-200-distilled-600M"

# API Keys (for enhanced features)
GOOGLE_MAPS_API_KEY = ""
OPENWEATHER_API_KEY = ""

# Twilio WhatsApp (for WhatsApp integration)
TWILIO_ACCOUNT_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_PHONE_NUMBER = ""
```

## 📚 **Documentation**

- **[API Reference](docs/API_REFERENCE.md)** - Complete API documentation
- **[Deployment Guide](docs/DEPLOYMENT_GUIDE.md)** - How to deploy to production
- **[WhatsApp Setup Guide](docs/WHATSAPP_SETUP_GUIDE.md)** - WhatsApp integration setup
- **[Features Overview](docs/FEATURES.md)** - Detailed feature descriptions
- **[Setup Instructions](docs/SETUP.md)** - Detailed setup guide

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 **Acknowledgments**

- **NLLB-200**: Facebook's multilingual translation model
- **LangChain**: For RAG implementation
- **FastAPI**: For the web framework
- **Hugging Face**: For model hosting and deployment

## 📞 **Support**

- **Issues**: Create an issue on GitHub
- **Documentation**: Check the `docs/` directory
- **Live Demo**: [https://lola97-hura-chatbot.hf.space](https://lola97-hura-chatbot.hf.space)

---

**Built with ❤️ for tourists visiting Kigali, Rwanda**
