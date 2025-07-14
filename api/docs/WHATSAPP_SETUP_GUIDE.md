# WhatsApp Integration Setup Guide

## 🎯 **Overview**

This guide will help you integrate your Hura Tourism Chatbot with WhatsApp using Twilio. Users will be able to interact with your chatbot directly through WhatsApp, accessing all the same features (Q&A, translation, maps, weather).

## 📋 **Prerequisites**

### **1. Twilio Account Setup**

#### **Create Twilio Account**

1. Go to [Twilio Console](https://console.twilio.com/)
2. Sign up for a free account
3. Verify your email and phone number

#### **Get WhatsApp Sandbox**

1. In Twilio Console, go to **Messaging** → **Try it out** → **Send a WhatsApp message**
2. Follow the instructions to join your WhatsApp sandbox
3. Note your sandbox phone number (e.g., `+14155238886`)

#### **Get API Credentials**

1. Go to **Console Dashboard** → **Account Info**
2. Copy your **Account SID** and **Auth Token**
3. Note your **Twilio Phone Number** (the WhatsApp sandbox number)

### **2. Environment Variables**

Create a `.env` file in your project root:

```bash
# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+14155238886  # Your WhatsApp sandbox number

# API Base URL (your deployed chatbot)
WHATSAPP_API_BASE_URL=https://lola9-hura-chatbot.hf.space

# Optional: Other API keys for enhanced features
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
```

## 🚀 **Implementation Steps**

### **Step 1: Install Dependencies**

```bash
pip install -r requirements.txt
```

### **Step 2: Test WhatsApp Service Locally**

```bash
python app_whatsapp.py
```

### **Step 3: Deploy to Production**

Deploy your WhatsApp-enabled app to your hosting platform (Hugging Face Spaces, Heroku, etc.)

### **Step 4: Configure Twilio Webhook**

1. **Get Your Webhook URL**

   - If deployed to Hugging Face Spaces: `https://your-app.hf.space/whatsapp/webhook`
   - If using ngrok for testing: `https://your-ngrok-url.ngrok.io/whatsapp/webhook`

2. **Set Webhook in Twilio Console**
   - Go to **Messaging** → **Settings** → **WhatsApp Sandbox Settings**
   - Set **When a message comes in** to: `https://your-webhook-url/whatsapp/webhook`
   - Set **HTTP Method** to: `POST`

## 🧪 **Testing the Integration**

### **1. Join WhatsApp Sandbox**

Send the provided code to your Twilio WhatsApp number to join the sandbox.

### **2. Test Basic Functionality**

Send these messages to your WhatsApp bot:

```
Hi
```

```
1
```

```
Tell me about Kigali
```

```
menu
```

```
2
```

```
a
```

```
Hello, how are you?
```

```
menu
```

```
3
```

```
Where is Kimironko?
```

```
quit
```

### **3. Expected Responses**

- **Welcome**: Initial greeting and instructions
- **Main Menu**: Shows numbered options (1-4)
- **Q&A**: Tourism information about Kigali
- **Translation**: Step-by-step translation process
- **Maps**: Location information (if API key configured)
- **Weather**: Weather information (if API key configured)
- **Reset**: "quit" command returns to welcome

## 📱 **WhatsApp Message Flow**

### **Message Processing Pipeline**

1. **User sends message** → WhatsApp
2. **WhatsApp** → Twilio
3. **Twilio** → Your webhook (`/whatsapp/webhook`)
4. **Webhook** → Intent detection
5. **Intent** → Appropriate service (RAG, Translation, Maps, Weather)
6. **Service** → API call to your FastAPI backend
7. **Response** → Format for WhatsApp
8. **Formatted response** → Twilio → WhatsApp → User

### **Menu-Based Flow**

The system uses a structured menu approach:

| User Action      | Bot Response                | Next Step                   |
| ---------------- | --------------------------- | --------------------------- |
| **Any greeting** | Welcome message + Main menu | User selects option (1-4)   |
| **Type "1"**     | Q&A service menu            | User asks question          |
| **Type "2"**     | Translation direction menu  | User selects "a" or "b"     |
| **Type "3"**     | Location service menu       | User asks location question |
| **Type "4"**     | Weather service menu        | User asks weather question  |
| **Type "menu"**  | Main menu (anytime)         | User selects option         |
| **Type "quit"**  | Reset to welcome            | Fresh start                 |

## 🔧 **Configuration Options**

### **WhatsApp Service Configuration**

```python
# config.py
class Settings(BaseModel):
    # Twilio WhatsApp API
    twilio_account_sid: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    twilio_auth_token: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    twilio_phone_number: str = os.getenv("TWILIO_PHONE_NUMBER", "")
    whatsapp_api_base_url: str = os.getenv("WHATSAPP_API_BASE_URL", "https://lola9-hura-chatbot.hf.space")
```

### **Customizing Responses**

Edit `services/whatsapp_service.py` to customize:

- **Menu message**: Modify `get_menu_message()`
- **Response formatting**: Modify response formatting in each handler
- **Intent detection**: Modify `detect_intent()` for custom logic

## 💰 **Cost Estimation**

### **Twilio WhatsApp Pricing**

- **Sandbox**: Free (limited to 1000 messages/month)
- **Production**: $0.0049 per message (both directions)
- **Typical usage**: 1000 messages/month = ~$5

### **Total Estimated Cost**

- **Twilio WhatsApp**: $5-10/month
- **Google Maps API**: $15-25/month (if enabled)
- **OpenWeather API**: $0 (free tier)
- **Total**: $20-35/month for full functionality

## 🛡️ **Security & Best Practices**

### **Webhook Security**

1. **Validate Twilio requests** (implement signature validation)
2. **Use HTTPS** for all webhook URLs
3. **Rate limiting** (already implemented)
4. **Error handling** (graceful fallbacks)

### **Environment Variables**

1. **Never commit API keys** to version control
2. **Use environment variables** for all sensitive data
3. **Rotate keys regularly**
4. **Monitor usage** in Twilio console

## 🔍 **Monitoring & Debugging**

### **Twilio Console**

- **Logs**: View message logs and delivery status
- **Analytics**: Monitor usage and performance
- **Errors**: Check for failed message deliveries

### **Your Application Logs**

```bash
# Check application logs
tail -f app.log

# Monitor webhook requests
grep "whatsapp" app.log
```

### **Common Issues**

#### **Webhook Not Receiving Messages**

- Check webhook URL is correct
- Verify HTTPS is enabled
- Check firewall settings
- Test webhook endpoint manually

#### **Messages Not Sending**

- Verify Twilio credentials
- Check phone number format
- Monitor Twilio console for errors
- Check application logs

#### **Slow Response Times**

- Monitor API response times
- Check model loading status
- Consider caching responses
- Optimize database queries

## 🚀 **Production Deployment**

### **1. Upgrade to Production WhatsApp**

1. **Apply for WhatsApp Business API** through Twilio
2. **Verify your business** with Meta
3. **Get production phone number**
4. **Update environment variables**

### **2. Scale Your Application**

1. **Load balancing** for multiple instances
2. **Database optimization** for high traffic
3. **Caching layer** for faster responses
4. **Monitoring and alerting**

### **3. User Onboarding**

1. **QR code** for easy WhatsApp joining
2. **Welcome message** with instructions
3. **Help documentation** for users
4. **Feedback collection** mechanism

## 📞 **Support**

### **Twilio Support**

- **Documentation**: [Twilio WhatsApp API](https://www.twilio.com/docs/whatsapp)
- **Community**: [Twilio Community](https://community.twilio.com/)
- **Support**: Available with paid plans

### **Your Application**

- **Logs**: Check application logs for errors
- **Health Check**: `/health` endpoint for system status
- **Documentation**: Check this guide and API reference

## 🎉 **Success Metrics**

Track these metrics to measure success:

- **Message volume**: Messages per day/week
- **Response time**: Average response time
- **User engagement**: Active users per day
- **Feature usage**: Which features are most popular
- **User satisfaction**: Feedback and ratings

---

**Your WhatsApp chatbot is now ready to help tourists explore Kigali! 🇷🇼**
