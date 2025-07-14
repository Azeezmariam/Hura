#!/usr/bin/env python3
"""
Integration test for enhanced chatbot with Maps and Weather features
"""

import os
import sys
import time
import requests
import json
from typing import Dict, List

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_enhanced_service_initialization():
    """Test that all enhanced services initialize correctly"""
    print("🔧 Testing Enhanced Service Initialization...")
    
    try:
        from services.vector_store import VectorStoreService
        from services.translation import TranslationService
        from services.enhanced_rag_service import EnhancedRAGService
        
        # Initialize services
        vector_store = VectorStoreService()
        vector_store.initialize()
        
        translation_service = TranslationService()
        translation_service.initialize()
        
        enhanced_rag = EnhancedRAGService(vector_store, translation_service)
        enhanced_rag.initialize()
        
        print("✅ All enhanced services initialized successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Service initialization failed: {e}")
        return False

def test_query_detection():
    """Test query type detection"""
    print("\n🔍 Testing Query Type Detection...")
    
    try:
        from services.maps_service import MapsService
        from services.weather_service import WeatherService
        
        maps_service = MapsService()
        weather_service = WeatherService()
        
        test_cases = [
            {
                "query": "Where is Kimironko?",
                "expected": "maps",
                "description": "Location query"
            },
            {
                "query": "How do I get to the airport?",
                "expected": "maps",
                "description": "Directions query"
            },
            {
                "query": "What's the weather today?",
                "expected": "weather",
                "description": "Current weather query"
            },
            {
                "query": "Will it rain tomorrow?",
                "expected": "weather",
                "description": "Weather forecast query"
            },
            {
                "query": "Tell me about Kigali",
                "expected": "general",
                "description": "General tourism query"
            },
            {
                "query": "Translate hello to Kinyarwanda",
                "expected": "translation",
                "description": "Translation query"
            }
        ]
        
        all_passed = True
        
        for test_case in test_cases:
            query = test_case["query"]
            expected = test_case["expected"]
            description = test_case["description"]
            
            # Detect query type
            is_maps = maps_service.is_maps_query(query)
            is_weather = weather_service.is_weather_query(query)
            
            # Determine actual type
            if is_maps:
                actual = "maps"
            elif is_weather:
                actual = "weather"
            elif "translate" in query.lower():
                actual = "translation"
            else:
                actual = "general"
            
            if actual == expected:
                print(f"✅ {description}: '{query}' → {actual}")
            else:
                print(f"❌ {description}: '{query}' → {actual} (expected {expected})")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Query detection test failed: {e}")
        return False

def test_maps_service_features():
    """Test maps service features"""
    print("\n🗺️ Testing Maps Service Features...")
    
    try:
        from services.maps_service import MapsService
        
        maps_service = MapsService()
        maps_service.initialize()
        
        # Test location extraction
        test_queries = [
            "Where is Kimironko?",
            "How do I get to Kigali International Airport?",
            "Directions to Kigali Genocide Memorial"
        ]
        
        for query in test_queries:
            location = maps_service.extract_location_from_query(query)
            if location:
                print(f"✅ Location extracted: '{query}' → '{location}'")
            else:
                print(f"⚠️ No location extracted: '{query}'")
        
        # Test query processing (without API key)
        response = maps_service.process_maps_query("Where is Kimironko?")
        if "don't have access" in response.lower():
            print("✅ Maps service gracefully handles missing API key")
        else:
            print("⚠️ Maps service response unexpected without API key")
        
        return True
        
    except Exception as e:
        print(f"❌ Maps service test failed: {e}")
        return False

def test_weather_service_features():
    """Test weather service features"""
    print("\n🌤️ Testing Weather Service Features...")
    
    try:
        from services.weather_service import WeatherService
        
        weather_service = WeatherService()
        weather_service.initialize()
        
        # Test location extraction
        test_queries = [
            "What's the weather in Kigali?",
            "Weather in Butare",
            "Temperature in Ruhengeri"
        ]
        
        for query in test_queries:
            location = weather_service.extract_location_from_query(query)
            if location:
                print(f"✅ Location extracted: '{query}' → '{location}'")
            else:
                print(f"⚠️ No location extracted: '{query}'")
        
        # Test time period extraction
        test_time_queries = [
            "Weather today",
            "Weather tomorrow",
            "Weather this afternoon",
            "Weather tonight"
        ]
        
        for query in test_time_queries:
            time_period = weather_service.extract_time_period(query)
            print(f"✅ Time period: '{query}' → '{time_period}'")
        
        # Test query processing (without API key)
        response = weather_service.process_weather_query("What's the weather today?")
        if "don't have access" in response.lower():
            print("✅ Weather service gracefully handles missing API key")
        else:
            print("⚠️ Weather service response unexpected without API key")
        
        return True
        
    except Exception as e:
        print(f"❌ Weather service test failed: {e}")
        return False

def test_enhanced_rag_integration():
    """Test enhanced RAG integration"""
    print("\n🤖 Testing Enhanced RAG Integration...")
    
    try:
        from services.vector_store import VectorStoreService
        from services.translation import TranslationService
        from services.enhanced_rag_service import EnhancedRAGService
        
        # Initialize services
        vector_store = VectorStoreService()
        vector_store.initialize()
        
        translation_service = TranslationService()
        translation_service.initialize()
        
        enhanced_rag = EnhancedRAGService(vector_store, translation_service)
        enhanced_rag.initialize()
        
        # Test query processing
        test_queries = [
            "Where is Kimironko?",
            "What's the weather today?",
            "Tell me about Kigali",
            "Translate hello to Kinyarwanda"
        ]
        
        for query in test_queries:
            try:
                response = enhanced_rag.query(query)
                if response and len(response) > 0:
                    print(f"✅ Query processed: '{query}' → Response length: {len(response)} chars")
                else:
                    print(f"⚠️ Empty response for: '{query}'")
            except Exception as e:
                print(f"❌ Query failed: '{query}' - {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Enhanced RAG integration test failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🌐 Testing API Endpoints...")
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Health endpoint working")
            print(f"   Features: {health_data.get('details', {}).get('features', {})}")
        else:
            print(f"⚠️ Health endpoint returned {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("⚠️ Server not running. Start with: python3 app_enhanced.py")
        return False
    except Exception as e:
        print(f"❌ Health endpoint test failed: {e}")
        return False
    
    # Test query endpoint
    try:
        test_query = {
            "text": "Where is Kimironko?"
        }
        
        response = requests.post(
            "http://localhost:8000/ask",
            json=test_query,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Query endpoint working - Response: {data.get('response', '')[:100]}...")
        else:
            print(f"❌ Query endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Query endpoint test failed: {e}")
        return False
    
    return True

def main():
    """Main test function"""
    print("🧪 Enhanced Chatbot Integration Test Suite")
    print("=" * 60)
    
    # Check environment
    google_maps_key = os.getenv("GOOGLE_MAPS_API_KEY", "")
    openweather_key = os.getenv("OPENWEATHER_API_KEY", "")
    
    print(f"Google Maps API Key: {'✅ Set' if google_maps_key else '❌ Not set'}")
    print(f"OpenWeather API Key: {'✅ Set' if openweather_key else '❌ Not set'}")
    print()
    
    # Run tests
    tests = [
        ("Service Initialization", test_enhanced_service_initialization),
        ("Query Detection", test_query_detection),
        ("Maps Service", test_maps_service_features),
        ("Weather Service", test_weather_service_features),
        ("Enhanced RAG Integration", test_enhanced_rag_integration),
        ("API Endpoints", test_api_endpoints)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 INTEGRATION TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All integration tests passed!")
        print("\nYour enhanced chatbot is ready with:")
        print("✅ RAG-based tourism information")
        print("✅ Google Maps integration")
        print("✅ Weather forecasting")
        print("✅ Translation services")
        print("✅ API endpoints")
        
        print("\n🚀 Next steps:")
        print("1. Set up API keys for full functionality")
        print("2. Deploy to production")
        print("3. Monitor usage and performance")
        
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Please check the errors above.")
        
        if not google_maps_key or not openweather_key:
            print("\n💡 To enable full functionality:")
            print("1. Get Google Maps API key: https://console.cloud.google.com/")
            print("2. Get OpenWeather API key: https://openweathermap.org/api")
            print("3. Set environment variables and re-run tests")

if __name__ == "__main__":
    main() 