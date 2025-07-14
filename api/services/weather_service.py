import logging
import requests
import re
from typing import Dict, Optional
from datetime import datetime, timedelta

from config import settings

logger = logging.getLogger(__name__)

class WeatherService:
    def __init__(self):
        self.api_key = settings.openweather_api_key
        self.default_city = settings.weather_default_city
        self.default_country = settings.weather_default_country
        
    def is_weather_query(self, text: str) -> bool:
        """Detect if a query is related to weather"""
        weather_keywords = [
            "weather", "temperature", "rain", "sunny", "cloudy", "forecast",
            "hot", "cold", "humid", "dry", "wind", "storm", "thunder",
            "today", "tomorrow", "this week", "this afternoon", "tonight",
            "morning", "evening", "night"
        ]
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in weather_keywords)
    
    def extract_location_from_query(self, text: str) -> Optional[str]:
        """Extract location from weather query"""
        # Default to Kigali if no specific location mentioned
        if "kigali" in text.lower():
            return "Kigali"
        
        # Look for other cities in Rwanda
        rwanda_cities = [
            "butare", "gitarama", "ruhengeri", "kibuye", "kibungo",
            "gisenyi", "cyangugu", "byumba", "rwamagana", "kayonza"
        ]
        
        text_lower = text.lower()
        for city in rwanda_cities:
            if city in text_lower:
                return city.title()
        
        # If no specific location, default to Kigali
        return "Kigali"
    
    def extract_time_period(self, text: str) -> str:
        """Extract time period from weather query"""
        text_lower = text.lower()
        
        if "tomorrow" in text_lower:
            return "tomorrow"
        elif "tonight" in text_lower or "this evening" in text_lower:
            return "tonight"
        elif "this afternoon" in text_lower:
            return "afternoon"
        elif "this morning" in text_lower:
            return "morning"
        elif "this week" in text_lower or "week" in text_lower:
            return "week"
        else:
            return "today"  # Default to today
    
    def get_current_weather(self, city: str = None) -> Optional[Dict]:
        """Get current weather for a city"""
        if not self.api_key:
            logger.warning("OpenWeather API key not configured")
            return None
        
        if not city:
            city = self.default_city
        
        try:
            url = "http://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": f"{city},{self.default_country}",
                "appid": self.api_key,
                "units": "metric"  # Use Celsius
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("cod") == 200:
                return {
                    "city": data.get("name", city),
                    "country": data.get("sys", {}).get("country", self.default_country),
                    "temperature": round(data.get("main", {}).get("temp", 0)),
                    "feels_like": round(data.get("main", {}).get("feels_like", 0)),
                    "humidity": data.get("main", {}).get("humidity", 0),
                    "description": data.get("weather", [{}])[0].get("description", ""),
                    "icon": data.get("weather", [{}])[0].get("icon", ""),
                    "wind_speed": data.get("wind", {}).get("speed", 0),
                    "pressure": data.get("main", {}).get("pressure", 0),
                    "visibility": data.get("visibility", 0),
                    "sunrise": data.get("sys", {}).get("sunrise", 0),
                    "sunset": data.get("sys", {}).get("sunset", 0)
                }
            else:
                logger.warning(f"Weather API error: {data.get('message', 'Unknown error')}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting current weather: {e}")
            return None
    
    def get_forecast(self, city: str = None, days: int = 5) -> Optional[Dict]:
        """Get weather forecast for a city"""
        if not self.api_key:
            logger.warning("OpenWeather API key not configured")
            return None
        
        if not city:
            city = self.default_city
        
        try:
            url = "http://api.openweathermap.org/data/2.5/forecast"
            params = {
                "q": f"{city},{self.default_country}",
                "appid": self.api_key,
                "units": "metric",
                "cnt": days * 8  # 8 forecasts per day (every 3 hours)
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("cod") == "200":
                forecasts = []
                for item in data.get("list", []):
                    forecast = {
                        "datetime": item.get("dt_txt", ""),
                        "temperature": round(item.get("main", {}).get("temp", 0)),
                        "feels_like": round(item.get("main", {}).get("feels_like", 0)),
                        "humidity": item.get("main", {}).get("humidity", 0),
                        "description": item.get("weather", [{}])[0].get("description", ""),
                        "icon": item.get("weather", [{}])[0].get("icon", ""),
                        "wind_speed": item.get("wind", {}).get("speed", 0),
                        "rain_probability": item.get("pop", 0) * 100  # Convert to percentage
                    }
                    forecasts.append(forecast)
                
                return {
                    "city": data.get("city", {}).get("name", city),
                    "country": data.get("city", {}).get("country", self.default_country),
                    "forecasts": forecasts
                }
            else:
                logger.warning(f"Forecast API error: {data.get('message', 'Unknown error')}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting forecast: {e}")
            return None
    
    def format_weather_response(self, weather_data: Dict, time_period: str = "today") -> str:
        """Format weather data into a user-friendly response"""
        if not weather_data:
            return "I'm sorry, I couldn't get the weather information at the moment. Please try again later."
        
        city = weather_data.get("city", "Kigali")
        temp = weather_data.get("temperature", 0)
        feels_like = weather_data.get("feels_like", 0)
        description = weather_data.get("description", "").title()
        humidity = weather_data.get("humidity", 0)
        wind_speed = weather_data.get("wind_speed", 0)
        
        response = f"🌤️ **Weather in {city} ({time_period.title()})**\n\n"
        response += f"🌡️ Temperature: {temp}°C"
        
        if feels_like != temp:
            response += f" (feels like {feels_like}°C)"
        
        response += f"\n☁️ Conditions: {description}\n"
        response += f"💧 Humidity: {humidity}%\n"
        response += f"💨 Wind: {wind_speed} m/s\n"
        
        # Add weather advice
        if temp > 30:
            response += "\n☀️ **Advice**: It's quite hot today! Stay hydrated and avoid prolonged sun exposure."
        elif temp < 15:
            response += "\n❄️ **Advice**: It's a bit cool today. You might want to bring a light jacket."
        elif "rain" in description.lower():
            response += "\n🌧️ **Advice**: Don't forget your umbrella! It might rain today."
        elif "sunny" in description.lower():
            response += "\n☀️ **Advice**: Great weather for outdoor activities! Don't forget sunscreen."
        
        return response
    
    def format_forecast_response(self, forecast_data: Dict, time_period: str = "week") -> str:
        """Format forecast data into a user-friendly response"""
        if not forecast_data:
            return "I'm sorry, I couldn't get the forecast information at the moment. Please try again later."
        
        city = forecast_data.get("city", "Kigali")
        forecasts = forecast_data.get("forecasts", [])
        
        if not forecasts:
            return f"I couldn't get the forecast for {city}."
        
        response = f"📅 **Weather Forecast for {city}**\n\n"
        
        # Group forecasts by day
        daily_forecasts = {}
        for forecast in forecasts:
            date = forecast["datetime"].split(" ")[0]
            if date not in daily_forecasts:
                daily_forecasts[date] = []
            daily_forecasts[date].append(forecast)
        
        # Show next 3 days
        for i, (date, day_forecasts) in enumerate(list(daily_forecasts.items())[:3]):
            if i == 0:
                day_name = "Today"
            elif i == 1:
                day_name = "Tomorrow"
            else:
                day_name = datetime.strptime(date, "%Y-%m-%d").strftime("%A")
            
            # Get average temperature for the day
            temps = [f["temperature"] for f in day_forecasts]
            avg_temp = round(sum(temps) / len(temps))
            
            # Get most common weather description
            descriptions = [f["description"] for f in day_forecasts]
            most_common = max(set(descriptions), key=descriptions.count)
            
            # Check for rain
            rain_prob = max([f["rain_probability"] for f in day_forecasts])
            
            response += f"📆 **{day_name} ({date})**\n"
            response += f"🌡️ Average: {avg_temp}°C\n"
            response += f"☁️ {most_common.title()}\n"
            
            if rain_prob > 30:
                response += f"🌧️ Rain chance: {rain_prob:.0f}%\n"
            
            response += "\n"
        
        return response
    
    def process_weather_query(self, query: str) -> str:
        """Process a weather-related query and return a response"""
        if not self.api_key:
            return "I'm sorry, but I don't have access to weather information at the moment. Please check a weather app or website for current conditions."
        
        # Extract location and time period
        location = self.extract_location_from_query(query)
        time_period = self.extract_time_period(query)
        
        # Get weather data
        if time_period in ["today", "tonight", "morning", "afternoon"]:
            weather_data = self.get_current_weather(location)
            return self.format_weather_response(weather_data, time_period)
        elif time_period in ["tomorrow", "week"]:
            forecast_data = self.get_forecast(location)
            return self.format_forecast_response(forecast_data, time_period)
        else:
            # Default to current weather
            weather_data = self.get_current_weather(location)
            return self.format_weather_response(weather_data, "today")
    
    def initialize(self):
        """Initialize the weather service"""
        if not self.api_key:
            logger.warning("OpenWeather API key not configured - weather features will be disabled")
        else:
            logger.info("Weather service initialized successfully") 