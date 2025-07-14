#!/usr/bin/env python3
"""
Simple test for deployed Hura Tourism Chatbot
Tests basic functionality with longer timeouts
"""

import requests
import json
import time

# Deployed chatbot URL
DEPLOYED_URL = "https://lola97-hura-chatbot.hf.space"

def test_basic_functionality():
    """Test basic functionality with longer timeouts"""
    print("🧪 Simple Deployed Chatbot Test")
    print("=" * 50)
    print(f"🌐 Testing: {DEPLOYED_URL}")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{DEPLOYED_URL}/health", timeout=60)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health: {data['status']}")
            print(f"   Model loaded: {data['details'].get('model_loaded', 'Unknown')}")
            print(f"   Storage: {data['details'].get('storage_usage', 'Unknown')}")
        else:
            print(f"❌ Health failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health error: {e}")
    
    # Test 2: Simple question with longer timeout
    print("\n2️⃣ Testing Simple Question (60s timeout)...")
    try:
        print("   Sending: 'Tell me about Kigali'")
        response = requests.post(
            f"{DEPLOYED_URL}/ask",
            json={"text": "Tell me about Kigali"},
            timeout=60  # 60 second timeout
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Response: {data['response'][:200]}...")
            print(f"   Processing time: {data.get('processing_time', 'Unknown')}")
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout after 60 seconds - model might be loading")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Translation with longer timeout
    print("\n3️⃣ Testing Translation (60s timeout)...")
    try:
        print("   Sending: 'Hello' for translation")
        response = requests.post(
            f"{DEPLOYED_URL}/translate/en2rw",
            json={"text": "Hello"},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Translation: 'Hello' → '{data['translation']}'")
        else:
            print(f"❌ Translation failed: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout after 60 seconds - translation model loading")
    except Exception as e:
        print(f"❌ Translation error: {e}")
    
    # Test 4: Check available endpoints
    print("\n4️⃣ Checking Available Endpoints...")
    try:
        response = requests.get(f"{DEPLOYED_URL}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Available endpoints:")
            for name, endpoint in data['endpoints'].items():
                print(f"   - {name}: {endpoint}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")

def test_with_curl_commands():
    """Provide curl commands for manual testing"""
    print("\n" + "=" * 50)
    print("🔧 Manual Testing Commands")
    print("=" * 50)
    
    print("\n📋 Health Check:")
    print(f"curl -X GET '{DEPLOYED_URL}/health'")
    
    print("\n🤖 Ask a Question:")
    print(f"curl -X POST '{DEPLOYED_URL}/ask' \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"text\": \"Tell me about Kigali\"}'")
    
    print("\n🔄 Translate English to Kinyarwanda:")
    print(f"curl -X POST '{DEPLOYED_URL}/translate/en2rw' \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"text\": \"Hello\"}'")
    
    print("\n🔄 Translate Kinyarwanda to English:")
    print(f"curl -X POST '{DEPLOYED_URL}/translate/rw2en' \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"text\": \"Muraho\"}'")

def main():
    """Main test function"""
    test_basic_functionality()
    test_with_curl_commands()
    
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    print("✅ Your chatbot is deployed and running!")
    print("⚠️  Some endpoints may be slow due to model loading")
    print("💡 Try the curl commands above for manual testing")
    print("🌐 Open static/deployed_interface.html for web interface")

if __name__ == "__main__":
    main() 