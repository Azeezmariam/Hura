#!/usr/bin/env python3
"""
Enhanced test script for deployed Hura Tourism Chatbot
Tests the menu-based version with Maps and Weather features
"""

import requests
import json
import time
from typing import Dict, Any

# Deployed chatbot URL
DEPLOYED_URL = "https://lola97-hura-chatbot.hf.space"

def test_menu_endpoint():
    """Test the menu endpoint"""
    print("📋 Testing Menu Endpoint...")
    
    try:
        response = requests.get(f"{DEPLOYED_URL}/menu", timeout=60)
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

def test_maps_endpoint():
    """Test the maps endpoint"""
    print("\n🗺️ Testing Maps Endpoint...")
    
    test_queries = [
        "Where is Kimironko?",
        "How do I get to Kigali International Airport?",
        "Where can I find restaurants near Kigali?"
    ]
    
    success_count = 0
    
    for query in test_queries:
        try:
            print(f"   Testing: '{query}'")
            response = requests.post(
                f"{DEPLOYED_URL}/maps",
                json={"query": query},
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Response: {data['response'][:100]}...")
                print(f"   ⏱️  Time: {data.get('processing_time', 'Unknown')}")
                print(f"   🔧 Service: {data.get('service_used', 'Unknown')}")
                success_count += 1
            else:
                print(f"   ❌ Failed: {response.status_code}")
                if response.text:
                    print(f"   Error: {response.text[:200]}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n   📊 Maps endpoint: {success_count}/{len(test_queries)} queries successful")
    return success_count > 0

def test_weather_endpoint():
    """Test the weather endpoint"""
    print("\n🌤️ Testing Weather Endpoint...")
    
    test_queries = [
        "What's the weather today?",
        "Will it rain tomorrow?",
        "Weather forecast for this week"
    ]
    
    success_count = 0
    
    for query in test_queries:
        try:
            print(f"   Testing: '{query}'")
            response = requests.post(
                f"{DEPLOYED_URL}/weather",
                json={"query": query},
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Response: {data['response'][:100]}...")
                print(f"   ⏱️  Time: {data.get('processing_time', 'Unknown')}")
                print(f"   🔧 Service: {data.get('service_used', 'Unknown')}")
                success_count += 1
            else:
                print(f"   ❌ Failed: {response.status_code}")
                if response.text:
                    print(f"   Error: {response.text[:200]}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n   📊 Weather endpoint: {success_count}/{len(test_queries)} queries successful")
    return success_count > 0

def test_enhanced_health_check():
    """Test enhanced health check with all services"""
    print("\n🏥 Testing Enhanced Health Check...")
    
    try:
        response = requests.get(f"{DEPLOYED_URL}/health", timeout=60)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed!")
            print(f"   Status: {data['status']}")
            print(f"   Services:")
            print(f"     - RAG: {data['details'].get('rag_service', False)}")
            print(f"     - Translation: {data['details'].get('translation_service', False)}")
            print(f"     - Maps: {data['details'].get('maps_service', False)}")
            print(f"     - Weather: {data['details'].get('weather_service', False)}")
            
            features = data['details'].get('features', {})
            print(f"   Features:")
            print(f"     - Maps API: {features.get('maps', False)}")
            print(f"     - Weather API: {features.get('weather', False)}")
            
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_root_endpoint():
    """Test the root endpoint for enhanced version"""
    print("\n🏠 Testing Root Endpoint...")
    
    try:
        response = requests.get(f"{DEPLOYED_URL}/", timeout=60)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root endpoint working!")
            print(f"   Message: {data['message']}")
            print(f"   Available endpoints: {list(data['endpoints'].keys())}")
            
            # Check if enhanced endpoints are available
            enhanced_endpoints = ['menu', 'location_service', 'weather_service']
            available_enhanced = [ep for ep in enhanced_endpoints if ep in data['endpoints']]
            
            if available_enhanced:
                print(f"   ✅ Enhanced endpoints: {available_enhanced}")
                return True
            else:
                print(f"   ⚠️ Enhanced endpoints not found")
                return False
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        return False

def test_core_features():
    """Test core features (ask and translation)"""
    print("\n🤖 Testing Core Features...")
    
    # Test ask endpoint
    try:
        print("   Testing ask endpoint...")
        response = requests.post(
            f"{DEPLOYED_URL}/ask",
            json={"text": "Tell me about Kigali"},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Ask: {data['response'][:100]}...")
            print(f"   ⏱️  Time: {data.get('processing_time', 'Unknown')}")
        else:
            print(f"   ❌ Ask failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Ask error: {e}")
    
    # Test translation
    try:
        print("   Testing translation...")
        response = requests.post(
            f"{DEPLOYED_URL}/translate/en2rw",
            json={"text": "Hello"},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Translation: 'Hello' → '{data['translation']}'")
        else:
            print(f"   ❌ Translation failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Translation error: {e}")

def test_api_keys_status():
    """Check if API keys are properly configured"""
    print("\n🔑 Testing API Keys Status...")
    
    try:
        # Test maps with a simple query
        response = requests.post(
            f"{DEPLOYED_URL}/maps",
            json={"query": "Where is Kigali?"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if "don't have access" in data['response'].lower():
                print("   ⚠️ Maps API key not configured or invalid")
                return False
            else:
                print("   ✅ Maps API key working")
                return True
        else:
            print(f"   ❌ Maps endpoint error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Maps test error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Enhanced Hura Tourism Chatbot Test Suite")
    print("=" * 60)
    print(f"🌐 Testing enhanced deployment at: {DEPLOYED_URL}")
    print("=" * 60)
    
    # Run tests
    tests = [
        ("Root Endpoint", test_root_endpoint),
        ("Enhanced Health Check", test_enhanced_health_check),
        ("Menu Endpoint", test_menu_endpoint),
        ("Maps Endpoint", test_maps_endpoint),
        ("Weather Endpoint", test_weather_endpoint),
        ("API Keys Status", test_api_keys_status),
        ("Core Features", test_core_features)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*20} {test_name} {'='*20}")
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 ENHANCED DEPLOYMENT TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed >= 5:  # Most core features working
        print("\n🎉 Your enhanced chatbot is working excellently!")
        print("\n✅ All features available:")
        print("   - Menu-based interface")
        print("   - Maps and location services")
        print("   - Weather information")
        print("   - Translation services")
        print("   - Tourism information")
        
        print("\n🚀 Your chatbot is ready for tourists!")
        print("   - Share the URL with visitors")
        print("   - Monitor usage and performance")
        print("   - Gather feedback for improvements")
        
    elif passed >= 3:
        print("\n⚠️ Some enhanced features are working.")
        print("   Check API keys and configuration.")
        
    else:
        print("\n❌ Enhanced features not working properly.")
        print("   Verify deployment and API keys.")

if __name__ == "__main__":
    main()