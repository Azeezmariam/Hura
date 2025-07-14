#!/usr/bin/env python3
"""
Test script for deployed Hura Tourism Chatbot
Tests the live deployment at https://lola97-hura-chatbot.hf.space
"""

import requests
import json
import time
from typing import Dict, Any

# Deployed chatbot URL
DEPLOYED_URL = "https://lola97-hura-chatbot.hf.space"

def test_root_endpoint():
    """Test the root endpoint"""
    print("🏠 Testing Root Endpoint...")
    
    try:
        response = requests.get(f"{DEPLOYED_URL}/", timeout=60)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root endpoint working!")
            print(f"   Message: {data['message']}")
            print(f"   Available endpoints: {list(data['endpoints'].keys())}")
            return True
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        return False

def test_health_endpoint():
    """Test the health endpoint"""
    print("\n🏥 Testing Health Endpoint...")
    
    try:
        response = requests.get(f"{DEPLOYED_URL}/health", timeout=60)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed!")
            print(f"   Status: {data['status']}")
            print(f"   Model loaded: {data['details'].get('model_loaded', 'Unknown')}")
            print(f"   Storage usage: {data['details'].get('storage_usage', 'Unknown')}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_ask_endpoint():
    """Test the general questions endpoint"""
    print("\n🤖 Testing Ask Endpoint...")
    
    test_queries = [
        "Tell me about Kigali",
        "What is the Kigali Genocide Memorial?",
        "What are the best restaurants in Kigali?",
        "How safe is Kigali for tourists?"
    ]
    
    success_count = 0
    
    for query in test_queries:
        try:
            print(f"\n   Testing: '{query}'")
            response = requests.post(
                f"{DEPLOYED_URL}/ask",
                json={"text": query},
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Response: {data['response'][:100]}...")
                print(f"   ⏱️  Time: {data.get('processing_time', 'Unknown')}")
                success_count += 1
            else:
                print(f"   ❌ Failed: {response.status_code}")
                if response.text:
                    print(f"   Error: {response.text[:200]}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n   📊 Ask endpoint: {success_count}/{len(test_queries)} queries successful")
    return success_count > 0

def test_translation_endpoints():
    """Test translation endpoints"""
    print("\n🔄 Testing Translation Endpoints...")
    
    success_count = 0
    
    # Test English to Kinyarwanda
    try:
        print("   Testing EN→RW translation...")
        response = requests.post(
            f"{DEPLOYED_URL}/translate/en2rw",
            json={"text": "Hello, how are you?"},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ EN→RW: 'Hello, how are you?' → '{data['translation']}'")
            success_count += 1
        else:
            print(f"   ❌ EN→RW failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ EN→RW error: {e}")
    
    # Test Kinyarwanda to English
    try:
        print("   Testing RW→EN translation...")
        response = requests.post(
            f"{DEPLOYED_URL}/translate/rw2en",
            json={"text": "Muraho, amakuru?"},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ RW→EN: 'Muraho, amakuru?' → '{data['translation']}'")
            success_count += 1
        else:
            print(f"   ❌ RW→EN failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ RW→EN error: {e}")
    
    print(f"\n   📊 Translation: {success_count}/2 endpoints working")
    return success_count > 0

def test_menu_endpoint():
    """Test if menu endpoint exists (for menu-based version)"""
    print("\n📋 Testing Menu Endpoint...")
    
    try:
        response = requests.get(f"{DEPLOYED_URL}/menu", timeout=60)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Menu endpoint available!")
            print(f"   Title: {data['title']}")
            print(f"   Options: {len(data['options'])}")
            for option in data['options']:
                print(f"   - {option['id']}: {option['title']}")
            return True
        else:
            print(f"⚠️ Menu endpoint not available (status: {response.status_code})")
            print("   This is expected for the single endpoint version")
            return False
    except Exception as e:
        print(f"⚠️ Menu endpoint not available: {e}")
        print("   This is expected for the single endpoint version")
        return False

def test_maps_and_weather_endpoints():
    """Test maps and weather endpoints if they exist"""
    print("\n🗺️🌤️ Testing Maps & Weather Endpoints...")
    
    # Test maps endpoint
    try:
        response = requests.post(
            f"{DEPLOYED_URL}/maps",
            json={"query": "Where is Kimironko?"},
            timeout=60
        )
        if response.status_code == 200:
            print("✅ Maps endpoint available!")
        else:
            print("⚠️ Maps endpoint not available (expected for basic version)")
    except:
        print("⚠️ Maps endpoint not available (expected for basic version)")
    
    # Test weather endpoint
    try:
        response = requests.post(
            f"{DEPLOYED_URL}/weather",
            json={"query": "What's the weather today?"},
            timeout=60
        )
        if response.status_code == 200:
            print("✅ Weather endpoint available!")
        else:
            print("⚠️ Weather endpoint not available (expected for basic version)")
    except:
        print("⚠️ Weather endpoint not available (expected for basic version)")

def test_performance():
    """Test response times"""
    print("\n⚡ Testing Performance...")
    
    test_query = "Tell me about Kigali"
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{DEPLOYED_URL}/ask",
            json={"text": test_query},
            timeout=60
        )
        end_time = time.time()
        
        if response.status_code == 200:
            total_time = end_time - start_time
            data = response.json()
            processing_time = data.get('processing_time', 'Unknown')
            
            print(f"✅ Query processed successfully!")
            print(f"   Total time: {total_time:.2f} seconds")
            print(f"   Processing time: {processing_time}")
            print(f"   Network overhead: {total_time - float(processing_time.split()[0]):.2f} seconds")
            
            if total_time < 5:
                print("   🚀 Performance: Excellent")
            elif total_time < 10:
                print("   ⚡ Performance: Good")
            else:
                print("   ⏳ Performance: Slow")
        else:
            print(f"❌ Performance test failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Performance test error: {e}")

def main():
    """Main test function"""
    print("🧪 Deployed Hura Tourism Chatbot Test Suite")
    print("=" * 60)
    print(f"🌐 Testing deployment at: {DEPLOYED_URL}")
    print("=" * 60)
    
    # Run tests
    tests = [
        ("Root Endpoint", test_root_endpoint),
        ("Health Check", test_health_endpoint),
        ("Ask Endpoint", test_ask_endpoint),
        ("Translation Endpoints", test_translation_endpoints),
        ("Menu Endpoint", test_menu_endpoint),
        ("Maps & Weather Endpoints", test_maps_and_weather_endpoints),
        ("Performance", test_performance)
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
    print("📊 DEPLOYMENT TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed >= 4:  # At least core features working
        print("\n🎉 Your deployed chatbot is working well!")
        print("\n✅ Core features available:")
        print("   - General tourism questions")
        print("   - English ↔ Kinyarwanda translation")
        print("   - Health monitoring")
        
        print("\n💡 Next steps:")
        print("   1. Test with real users")
        print("   2. Monitor performance")
        print("   3. Consider adding Maps & Weather features")
        
    else:
        print("\n⚠️ Some core features are not working properly.")
        print("   Check the deployment logs and configuration.")

if __name__ == "__main__":
    main() 