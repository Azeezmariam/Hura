#!/usr/bin/env python3
"""
Test script for Google Maps and OpenWeather APIs
Run this to verify your API keys are working correctly
"""

import os
import requests
import json
from typing import Dict, Optional

def test_google_maps_api(api_key: str) -> bool:
    """Test Google Maps API functionality"""
    print("🔍 Testing Google Maps API...")
    
    if not api_key:
        print("❌ No Google Maps API key provided")
        return False
    
    try:
        # Test Places API
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            "query": "Kigali Genocide Memorial",
            "key": api_key,
            "region": "rw"
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get("status") == "OK":
            place = data["results"][0]
            print(f"✅ Places API: Found '{place['name']}' at {place['formatted_address']}")
        else:
            print(f"❌ Places API failed: {data.get('status')} - {data.get('error_message', 'Unknown error')}")
            return False
        
        # Test Directions API
        url = "https://maps.googleapis.com/maps/api/directions/json"
        params = {
            "origin": "Kigali, Rwanda",
            "destination": "Kigali International Airport",
            "key": api_key,
            "region": "rw"
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get("status") == "OK":
            route = data["routes"][0]["legs"][0]
            print(f"✅ Directions API: {route['distance']['text']} in {route['duration']['text']}")
        else:
            print(f"❌ Directions API failed: {data.get('status')} - {data.get('error_message', 'Unknown error')}")
            return False
        
        print("✅ Google Maps API is working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Google Maps API test failed: {e}")
        return False

def test_openweather_api(api_key: str) -> bool:
    """Test OpenWeather API functionality"""
    print("\n🌤️ Testing OpenWeather API...")
    
    if not api_key:
        print("❌ No OpenWeather API key provided")
        return False
    
    try:
        # Test Current Weather API
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": "Kigali,RW",
            "appid": api_key,
            "units": "metric"
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get("cod") == 200:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            print(f"✅ Current Weather API: {temp}°C, {description} in Kigali")
        else:
            print(f"❌ Current Weather API failed: {data.get('cod')} - {data.get('message', 'Unknown error')}")
            return False
        
        # Test Forecast API
        url = "http://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": "Kigali,RW",
            "appid": api_key,
            "units": "metric",
            "cnt": 8  # 24 hours of forecasts
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get("cod") == "200":
            forecasts = data.get("list", [])
            print(f"✅ Forecast API: Retrieved {len(forecasts)} forecast periods")
        else:
            print(f"❌ Forecast API failed: {data.get('cod')} - {data.get('message', 'Unknown error')}")
            return False
        
        print("✅ OpenWeather API is working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ OpenWeather API test failed: {e}")
        return False

def test_enhanced_features():
    """Test the enhanced chatbot features"""
    print("\n🤖 Testing Enhanced Chatbot Features...")
    
    try:
        # Import services
        from services.maps_service import MapsService
        from services.weather_service import WeatherService
        
        # Test Maps Service
        maps_service = MapsService()
        maps_service.initialize()
        
        # Test weather service
        weather_service = WeatherService()
        weather_service.initialize()
        
        print("✅ Enhanced services initialized successfully!")
        
        # Test query detection
        test_queries = [
            "Where is Kimironko?",
            "What's the weather today?",
            "How do I get to the airport?",
            "Will it rain tomorrow?",
            "Translate hello to Kinyarwanda"
        ]
        
        print("\n🔍 Testing query detection:")
        for query in test_queries:
            is_maps = maps_service.is_maps_query(query)
            is_weather = weather_service.is_weather_query(query)
            
            query_type = []
            if is_maps:
                query_type.append("Maps")
            if is_weather:
                query_type.append("Weather")
            if not is_maps and not is_weather:
                query_type.append("General")
            
            print(f"  '{query}' → {', '.join(query_type)}")
        
        print("\n✅ Enhanced features are working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Enhanced features test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 API Integration Test Suite")
    print("=" * 50)
    
    # Get API keys from environment
    google_maps_key = os.getenv("GOOGLE_MAPS_API_KEY", "")
    openweather_key = os.getenv("OPENWEATHER_API_KEY", "")
    
    print(f"Google Maps API Key: {'✅ Set' if google_maps_key else '❌ Not set'}")
    print(f"OpenWeather API Key: {'✅ Set' if openweather_key else '❌ Not set'}")
    print()
    
    # Test APIs
    maps_working = test_google_maps_api(google_maps_key)
    weather_working = test_openweather_api(openweather_key)
    enhanced_working = test_enhanced_features()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    print(f"Google Maps API: {'✅ PASS' if maps_working else '❌ FAIL'}")
    print(f"OpenWeather API: {'✅ PASS' if weather_working else '❌ FAIL'}")
    print(f"Enhanced Features: {'✅ PASS' if enhanced_working else '❌ FAIL'}")
    
    if maps_working and weather_working and enhanced_working:
        print("\n🎉 All tests passed! Your enhanced chatbot is ready to use.")
        print("\nNext steps:")
        print("1. Run: python3 app_enhanced.py")
        print("2. Test with: curl -X POST http://localhost:8000/ask -H 'Content-Type: application/json' -d '{\"text\": \"Where is Kimironko?\"}'")
    else:
        print("\n⚠️ Some tests failed. Please check your API keys and configuration.")
        
        if not google_maps_key:
            print("- Set GOOGLE_MAPS_API_KEY environment variable")
        if not openweather_key:
            print("- Set OPENWEATHER_API_KEY environment variable")

if __name__ == "__main__":
    main() 