# Enhanced Menu-Based Chatbot Deployment Guide

## 🚀 **Deploying the Enhanced Version with Maps & Weather**

This guide will help you deploy the enhanced menu-based version of your Hura Tourism Chatbot with Google Maps and Weather features.

## 📋 **Prerequisites**

### **✅ Already Done:**

- ✅ API keys stored as Hugging Face Secrets
- ✅ Basic chatbot working at https://lola9-hura-chatbot.hf.space
- ✅ Enhanced code ready (`app_menu_based.py`)

### **🔑 Required API Keys (Already in HF Secrets):**

- `GOOGLE_MAPS_API_KEY` - Google Maps API key
- `OPENWEATHER_API_KEY` - OpenWeather API key

## 🎯 **Deployment Steps**

### **Step 1: Update Your Hugging Face Space**

1. **Go to your Hugging Face Space**: https://huggingface.co/spaces/lola9/hura-chatbot

2. **Update the main app file**:

   - Replace `app.py` with `app_menu_based.py`
   - Or rename `app_menu_based.py` to `app.py`

3. **Ensure all required files are present**:
   ```
   app.py (or app_menu_based.py)
   config.py
   requirements.txt
   services/
   api/
   middleware/
   utils/
   data/
   ```

### **Step 2: Verify API Keys in Secrets**

In your Hugging Face Space settings, ensure these secrets are set:

- `GOOGLE_MAPS_API_KEY` - Your Google Maps API key
- `OPENWEATHER_API_KEY` - Your OpenWeather API key

### **Step 3: Update Requirements (if needed)**

Make sure `requirements.txt` includes:

```txt
requests>=2.31.0  # For API calls
```

### **Step 4: Deploy and Test**

1. **Commit and push** your changes to Hugging Face
2. **Wait for deployment** (usually 2-5 minutes)
3. **Test the new endpoints**

## 🧪 **Testing the Enhanced Version**

### **New Endpoints Available:**

1. **Menu Endpoint**: `GET /menu`
2. **Maps Service**: `POST /maps`
3. **Weather Service**: `POST /weather`

### **Test Commands:**

```bash
# Test menu endpoint
curl -X GET 'https://lola9-hura-chatbot.hf.space/menu'

# Test maps service
curl -X POST 'https://lola9-hura-chatbot.hf.space/maps' \
     -H 'Content-Type: application/json' \
     -d '{"query": "Where is Kimironko?"}'

# Test weather service
curl -X POST 'https://lola9-hura-chatbot.hf.space/weather' \
     -H 'Content-Type: application/json' \
     -d '{"query": "What is the weather today?"}'
```

### **Expected Features:**

✅ **Menu Interface** - Clear feature discovery
✅ **Maps Integration** - Location search and directions
✅ **Weather Updates** - Current weather and forecasts
✅ **Translation** - English ↔ Kinyarwanda
✅ **Tourism Info** - General questions about Kigali

## 🎯 **Enhanced Features**

### **🗺️ Maps Service:**

- Location search: "Where is Kimironko?"
- Directions: "How do I get to the airport?"
- Nearby places: "Restaurants near Kigali"
- Place details: Addresses, ratings, types

### **🌤️ Weather Service:**

- Current weather: "What's the weather today?"
- Forecasts: "Weather tomorrow?"
- Time-specific: "Will it rain this afternoon?"
- Weather advice: Clothing recommendations

### **📱 Menu Interface:**

- Clear feature discovery
- Easy navigation
- Example queries
- Service status indicators

## 🔧 **Troubleshooting**

### **If Maps/Weather Don't Work:**

1. **Check API keys** in Hugging Face Secrets
2. **Verify API quotas** (Google Maps: $200/month free, OpenWeather: 1000 calls/day)
3. **Check logs** in Hugging Face Space

### **If Deployment Fails:**

1. **Check requirements.txt** - ensure all dependencies listed
2. **Verify file structure** - all services and modules present
3. **Check logs** for specific error messages

### **Performance Issues:**

- **Response times**: 30-60 seconds normal for free tier
- **Memory limits**: Free tier has constraints
- **Cold starts**: First requests after inactivity are slower

## 📊 **Expected Test Results**

After deployment, running `test_deployed.py` should show:

```
✅ Root Endpoint: PASS
✅ Health Check: PASS
✅ Ask Endpoint: PASS
✅ Translation Endpoints: PASS
✅ Menu Endpoint: PASS
✅ Maps Endpoint: PASS
✅ Weather Endpoint: PASS
```

## 🎉 **Success Indicators**

Your enhanced chatbot is working when:

1. **Menu endpoint** returns available features
2. **Maps queries** return location information
3. **Weather queries** return current conditions
4. **Health check** shows all services as active
5. **All endpoints** respond within 60 seconds

## 🚀 **Next Steps After Deployment**

1. **Test all features** with the provided test scripts
2. **Update web interface** to use new endpoints
3. **Monitor usage** and performance
4. **Gather user feedback** and iterate

## 💡 **Pro Tips**

- **API Key Security**: Never commit API keys to code
- **Rate Limiting**: Respect API quotas and limits
- **Error Handling**: Graceful fallbacks when APIs are unavailable
- **User Experience**: Clear loading states and error messages

Your enhanced chatbot will provide a comprehensive tourism experience for visitors to Kigali! 🌍
