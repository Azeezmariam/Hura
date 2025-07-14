# Google Maps & Weather Integration Setup Guide

## 🎯 **Overview**

This guide will help you implement Google Maps and Weather forecasting features in your Hura Tourism Chatbot. These features will allow users to:

- **Maps**: Ask for locations, directions, and nearby places
- **Weather**: Get current weather and forecasts for Kigali and other Rwandan cities

## 📋 **Prerequisites**

### **1. API Keys Required**

#### **Google Maps API Key**

- **Cost**: $200 free credit monthly (typically sufficient for tourism chatbot)
- **Setup**:
  1. Go to [Google Cloud Console](https://console.cloud.google.com/)
  2. Create a new project or select existing
  3. Enable these APIs:
     - Places API
     - Directions API
     - Geocoding API
  4. Create credentials (API Key)
  5. Set usage restrictions (recommended)

#### **OpenWeather API Key**

- **Cost**: Free tier (1000 calls/day) - sufficient for most use cases
- **Setup**:
  1. Go to [OpenWeatherMap](https://openweathermap.org/api)
  2. Sign up for free account
  3. Get API key (immediate activation)

### **2. Environment Variables**

Create a `.env` file in your project root:

```bash
# Google Maps API
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here

# OpenWeather API
OPENWEATHER_API_KEY=your_openweather_api_key_here

# Existing variables
PERSISTENT_DIR=/data
USE_GPU=false
```

## 🚀 **Implementation Steps**

### **Step 1: Install Dependencies**

```bash
pip install -r requirements.txt
```

### **Step 2: Test API Keys**

Create a test script to verify your API keys work:

```bash
python3 test_apis.py
```

### **Step 3: Run Enhanced App**

```bash
python3 app_enhanced.py
```

## 🧪 **Testing the Features**

### **Maps Queries to Test**

```bash
# Location queries
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"text": "Where is Kimironko?"}'

curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"text": "How do I get to Kigali International Airport?"}'

curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"text": "Where can I find restaurants near Kigali Genocide Memorial?"}'
```

### **Weather Queries to Test**

```bash
# Current weather
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"text": "What is the weather today?"}'

curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"text": "Will it rain this afternoon?"}'

curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"text": "What is the weather forecast for tomorrow?"}'
```

### **Combined Queries**

```bash
# Translation + Maps
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"text": "Translate: Where is the nearest ATM?"}'

# General tourism + Weather
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"text": "What should I wear today for visiting the Genocide Memorial?"}'
```

## 📊 **Feature Capabilities**

### **Maps Features**

| Query Type          | Example                             | Response                        |
| ------------------- | ----------------------------------- | ------------------------------- |
| **Location Search** | "Where is Kimironko?"               | Address, coordinates, rating    |
| **Directions**      | "How do I get to the airport?"      | Distance, duration, route steps |
| **Nearby Places**   | "Restaurants near Kigali"           | List of nearby restaurants      |
| **Place Details**   | "What is Kigali Genocide Memorial?" | Description, address, hours     |

### **Weather Features**

| Query Type          | Example                        | Response                          |
| ------------------- | ------------------------------ | --------------------------------- |
| **Current Weather** | "What's the weather today?"    | Temperature, conditions, humidity |
| **Forecast**        | "Weather tomorrow?"            | 3-day forecast with details       |
| **Time-specific**   | "Will it rain this afternoon?" | Specific time period weather      |
| **Advice**          | "What should I wear?"          | Weather-based recommendations     |

### **Supported Cities**

- **Kigali** (default)
- **Butare**
- **Gitarama**
- **Ruhengeri**
- **Kibuye**
- **Kibungo**
- **Gisenyi**
- **Cyangugu**
- **Byumba**
- **Rwamagana**
- **Kayonza**

## 🔧 **Configuration Options**

### **Maps Configuration**

```python
# config.py
google_maps_api_key: str = os.getenv("GOOGLE_MAPS_API_KEY", "")
default_location: str = "Kigali, Rwanda"
```

### **Weather Configuration**

```python
# config.py
openweather_api_key: str = os.getenv("OPENWEATHER_API_KEY", "")
weather_default_city: str = "Kigali"
weather_default_country: str = "RW"
```

## 💰 **Cost Estimation**

### **Google Maps API**

- **Free Tier**: $200 monthly credit
- **Typical Usage**:
  - 1000 location searches/month: ~$5
  - 500 direction requests/month: ~$10
  - **Total**: ~$15-25/month for typical tourism chatbot

### **OpenWeather API**

- **Free Tier**: 1000 calls/day
- **Typical Usage**:
  - 100 weather queries/day: 3000/month
  - **Cost**: $0 (within free tier)

### **Total Estimated Cost**: $15-25/month

## 🛡️ **Security & Best Practices**

### **API Key Security**

1. **Never commit API keys** to version control
2. **Use environment variables** for all API keys
3. **Set usage restrictions** on Google Cloud Console
4. **Monitor usage** regularly

### **Rate Limiting**

- **Google Maps**: 100 requests/second
- **OpenWeather**: 60 calls/minute
- **Your App**: 60 requests/minute per user

### **Error Handling**

- **Graceful degradation** when APIs are unavailable
- **Fallback responses** for failed requests
- **User-friendly error messages**

## 📈 **Performance Optimization**

### **Caching Strategy**

- **Weather data**: Cache for 10 minutes
- **Maps data**: Cache for 1 hour
- **Popular queries**: Cache for 24 hours

### **Response Time**

- **Maps queries**: 2-5 seconds
- **Weather queries**: 1-3 seconds
- **Combined queries**: 3-8 seconds

## 🔍 **Monitoring & Analytics**

### **What to Monitor**

- API response times
- Error rates
- Usage patterns
- User satisfaction

### **Key Metrics**

- Queries per day
- Most popular locations
- Weather query frequency
- Translation usage

## 🚨 **Troubleshooting**

### **Common Issues**

#### **Google Maps API Errors**

```
Error: REQUEST_DENIED
Solution: Check API key and enable required APIs
```

#### **OpenWeather API Errors**

```
Error: 401 Unauthorized
Solution: Verify API key is correct
```

#### **Rate Limit Exceeded**

```
Error: OVER_QUERY_LIMIT
Solution: Implement caching or upgrade plan
```

### **Debug Commands**

```bash
# Test API connectivity
python3 test_apis.py

# Check service health
curl http://localhost:8000/health

# View logs
tail -f app.log
```

## 🎯 **Next Steps**

### **Phase 1: Basic Implementation**

- ✅ Set up API keys
- ✅ Test basic functionality
- ✅ Deploy to production

### **Phase 2: Enhancement**

- 🔄 Add caching layer
- 🔄 Implement user preferences
- 🔄 Add more Rwandan cities

### **Phase 3: Advanced Features**

- 🔄 Voice integration
- 🔄 Offline maps
- 🔄 Personalized recommendations

## 📞 **Support**

If you encounter issues:

1. **Check API documentation**:

   - [Google Maps API](https://developers.google.com/maps/documentation)
   - [OpenWeather API](https://openweathermap.org/api)

2. **Verify API keys** are active and have proper permissions

3. **Check usage limits** and billing status

4. **Review logs** for specific error messages

## 🎉 **Success Metrics**

Your enhanced chatbot will now support:

- ✅ **Location queries** with detailed responses
- ✅ **Weather forecasts** with advice
- ✅ **Translation** for all features
- ✅ **Combined queries** (e.g., "What should I wear today?")
- ✅ **Graceful fallbacks** when APIs are unavailable

This makes your tourism chatbot a comprehensive travel assistant for visitors to Kigali!
