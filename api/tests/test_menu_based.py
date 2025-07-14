#!/usr/bin/env python3
"""
Test script for menu-based chatbot approach
Demonstrates the separate endpoints for each feature
"""

import requests
import json
import time
from typing import Dict, Any

def test_menu_endpoint():
    """Test the menu endpoint"""
    print("📋 Testing Menu Endpoint...")
    
    try:
        response = requests.get("http://localhost:8000/menu", timeout=5)
        if response.status_code == 200:
            menu = response.json()
            print(f"✅ Menu loaded successfully!")
            print(f"   Title: {menu['title']}")
            print(f"   Options: {len(menu['options'])}")
            
            for option in menu['options']:
                print(f"   {option['id']}. {option['title']}")
            
            print(f"   Features Status: {menu['features_status']}")
            return True
        else:
            print(f"❌ Menu endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Menu test failed: {e}")
        return False

def test_ask_endpoint():
    """Test the general questions endpoint"""
    print("\n🤖 Testing Ask Endpoint...")
    
    test_queries = [
        "Tell me about Kigali",
        "What is the Kigali Genocide Memorial?",
        "What are the best restaurants in Kigali?"
    ]
    
    for query in test_queries:
        try:
            response = requests.post(
                "http://localhost:8000/ask",
                json={"text": query},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Query: '{query}'")
                print(f"   Response: {data['response'][:100]}...")
                print(f"   Service: {data['service_used']}")
                print(f"   Time: {data['processing_time']}")
            else:
                print(f"❌ Query failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Query error: {e}")

def test_translation_endpoints():
    """Test translation endpoints"""
    print("\n🔄 Testing Translation Endpoints...")
    
    # Test English to Kinyarwanda
    try:
        response = requests.post(
            "http://localhost:8000/translate/en2rw",
            json={"text": "Hello, how are you?"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ EN→RW: 'Hello, how are you?' → '{data['translation']}'")
            print(f"   Service: {data['service_used']}")
        else:
            print(f"❌ EN→RW failed: {response.status_code}")
    except Exception as e:
        print(f"❌ EN→RW error: {e}")
    
    # Test Kinyarwanda to English
    try:
        response = requests.post(
            "http://localhost:8000/translate/rw2en",
            json={"text": "Muraho, amakuru?"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ RW→EN: 'Muraho, amakuru?' → '{data['translation']}'")
            print(f"   Service: {data['service_used']}")
        else:
            print(f"❌ RW→EN failed: {response.status_code}")
    except Exception as e:
        print(f"❌ RW→EN error: {e}")

def test_maps_endpoint():
    """Test maps endpoint"""
    print("\n🗺️ Testing Maps Endpoint...")
    
    test_queries = [
        "Where is Kimironko?",
        "How do I get to Kigali International Airport?",
        "Where can I find restaurants near Kigali?"
    ]
    
    for query in test_queries:
        try:
            response = requests.post(
                "http://localhost:8000/maps",
                json={"query": query},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Maps Query: '{query}'")
                print(f"   Response: {data['response'][:100]}...")
                print(f"   Service: {data['service_used']}")
                print(f"   Time: {data['processing_time']}")
            else:
                print(f"❌ Maps query failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Maps query error: {e}")

def test_weather_endpoint():
    """Test weather endpoint"""
    print("\n🌤️ Testing Weather Endpoint...")
    
    test_queries = [
        "What's the weather today?",
        "Will it rain tomorrow?",
        "Weather forecast for this week"
    ]
    
    for query in test_queries:
        try:
            response = requests.post(
                "http://localhost:8000/weather",
                json={"query": query},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Weather Query: '{query}'")
                print(f"   Response: {data['response'][:100]}...")
                print(f"   Service: {data['service_used']}")
                print(f"   Time: {data['processing_time']}")
            else:
                print(f"❌ Weather query failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Weather query error: {e}")

def test_health_endpoint():
    """Test health endpoint"""
    print("\n🏥 Testing Health Endpoint...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed!")
            print(f"   Status: {data['status']}")
            print(f"   Services: {data['details']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def compare_approaches():
    """Compare single endpoint vs menu-based approach"""
    print("\n📊 Comparing Approaches...")
    
    print("\n🔍 Single Endpoint Approach (app_enhanced.py):")
    print("   ✅ Natural conversation flow")
    print("   ✅ Automatic intent detection")
    print("   ❌ Complex error handling")
    print("   ❌ Harder to debug")
    print("   ❌ Users might not discover all features")
    
    print("\n🎯 Menu-Based Approach (app_menu_based.py):")
    print("   ✅ Clear feature discovery")
    print("   ✅ Better user experience")
    print("   ✅ Easier to maintain and debug")
    print("   ✅ Predictable API behavior")
    print("   ✅ Better for mobile apps")
    print("   ❌ Less natural conversation")
    print("   ❌ More endpoints to manage")

def main():
    """Main test function"""
    print("🧪 Menu-Based Chatbot Test Suite")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("❌ Server not responding. Start with: python3 app_menu_based.py")
            return
    except:
        print("❌ Cannot connect to server. Start with: python3 app_menu_based.py")
        return
    
    # Run tests
    tests = [
        ("Menu Endpoint", test_menu_endpoint),
        ("Health Endpoint", test_health_endpoint),
        ("Ask Endpoint", test_ask_endpoint),
        ("Translation Endpoints", test_translation_endpoints),
        ("Maps Endpoint", test_maps_endpoint),
        ("Weather Endpoint", test_weather_endpoint)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*20} {test_name} {'='*20}")
            test_func()
            results.append((test_name, True))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Compare approaches
    compare_approaches()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print("\n🎯 Recommendation:")
    print("The menu-based approach is more practical for:")
    print("- Tourism chatbots with clear feature sets")
    print("- Mobile applications")
    print("- Simple web interfaces")
    print("- Better user experience and feature discovery")
    
    print("\n🚀 Next steps:")
    print("1. Open static/index.html in your browser")
    print("2. Test the interactive menu interface")
    print("3. Deploy with proper API keys for full functionality")

if __name__ == "__main__":
    main() 