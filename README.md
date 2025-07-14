# 🌍 Hura AI Chatbot

**Your AI-powered tourism assistant for Kigali, Rwanda — available on the web and WhatsApp!**

---

## 🚀 Live Demo

- **Web App:** [huraaichat.com](https://huraaichat.com)
- **Contact:** info@huraaichat.com

## Video Demo

A 5-minute minimum video demo of the application is available to showcase the core functionalities:

- How the user interacts with the system.
- How the chatbot answers questions, translates text, and explains cultural norms.
- [Video Demo Link](https://drive.google.com/drive/folders/1BQ2yAP6d5eGcBhZacCWorZS2LvhQQWA8?usp=sharing)

---

## ✨ Features (Web & WhatsApp)

- **Tourism Q&A:** Ask about Kigali’s attractions, culture, safety, restaurants, and more.
- **Translation:** English ↔ Kinyarwanda, powered by NLLB-200.
- **Location Services:** Find places, get directions, discover nearby spots.
- **Weather Updates:** Get current weather and forecasts for Kigali.
- **Unified Experience:** All features accessible via both the web app and WhatsApp.

---

## 🧑‍💻 User Experience

### Web App

1. Visit [huraaichat.com](https://huraaichat.com).
2. Ask questions, request translations, or get maps/weather info.
3. Receive instant, AI-generated responses.

### WhatsApp

1. Add the Hura AI WhatsApp number (see deployment for number).
2. Send any message (e.g., "Hi").
3. Follow the menu prompts:
   - 1️⃣ Ask Questions
   - 2️⃣ Translation
   - 3️⃣ Location Help
   - 4️⃣ Weather
4. Type "menu" to return to the main menu, or "quit" to reset.

---

## 🏗️ Technical Architecture

- **Backend:** FastAPI (Python), modular services (RAG, translation, WhatsApp, maps, weather), MongoDB(Database)
- **Frontend:** HTML, CSS, JS (organized by feature)
- **WhatsApp Bot:** Twilio integration, menu-driven, session management
- **Data:** Local tourism data, vector store for retrieval
- **Deployment:** Docker support, scripts for migration/testing

---

## 🛠️ Getting Started

### Prerequisites

- Python 3.9+
- 4GB+ RAM
- [Docker](https://www.docker.com/) (optional, for containerized deployment)
- Twilio account (for WhatsApp integration)

### Installation (Local)

```bash
git clone https://github.com/Azeezmariam/Hura.git
cd Hura
pip install -r api/requirements.txt
```

### Environment Variables

Create a `.env` file in `api/` (see `api/config.py` for all options):

```
# Twilio WhatsApp
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_number

# Google Maps & OpenWeather (optional)
GOOGLE_MAPS_API_KEY=your_maps_key
OPENWEATHER_API_KEY=your_weather_key
```

### Running the App

- **Web API:**
  ```bash
  cd api
  python app.py
  # Visit https://lola97-hura-chatbot-web.hf.space/docs for API docs
  ```
- **WhatsApp Bot:**
  ```bash
  cd api
  python app_whatsapp.py
  # Set your Twilio webhook to https://lola97-hura-chatbot.hf.space/whatsapp/webhook
  ```

---

## 📡 API Reference (Key Endpoints)

| Endpoint            | Method | Description                       |
| ------------------- | ------ | --------------------------------- |
| `/`                 | GET    | API info & available endpoints    |
| `/health`           | GET    | Health check                      |
| `/ask`              | POST   | Ask tourism questions             |
| `/translate/en2rw`  | POST   | English → Kinyarwanda translation |
| `/translate/rw2en`  | POST   | Kinyarwanda → English translation |
| `/maps`             | POST   | Location queries                  |
| `/weather`          | POST   | Weather queries                   |
| `/whatsapp/webhook` | POST   | WhatsApp integration (Twilio)     |

**Example:**

```bash
curl -X POST "https://lola97-hura-chatbot.hf.space/ask" \
     -H "Content-Type: application/json" \
     -d '{"text": "Tell me about Kigali Genocide Memorial"}'
```

---

## 🤝 Contributing

- Fork the repo and create a feature branch.
- Add/fix code and tests (see `api/tests/`).
- Run tests: `pytest api/tests/`
- Submit a pull request!

---

## 📝 Credits & License

- **Lead:** Mariam Azeez
- **License:** Apache 2.0
- **Special Thanks:** Kigali tourism community, My Supervisor - Ms Samiratu Ntoshi

---

## 📚 Further Reading

- [API Reference](api/docs/API_REFERENCE.md)
- [WhatsApp Setup Guide](api/docs/WHATSAPP_SETUP_GUIDE.md)
- [Flow Diagrams](api/docs/WHATSAPP_FLOW_DIAGRAM.md)

---

_Empowering travelers in Rwanda with AI._
