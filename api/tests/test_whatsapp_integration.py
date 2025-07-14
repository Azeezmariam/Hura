#!/usr/bin/env python3
"""
Test script for WhatsApp integration
Tests the WhatsApp service and webhook functionality with menu-based flow
"""

import requests
import json
import time
from typing import Dict, Any

# Configuration
API_BASE_URL = "https://lola97-hura-chatbot.hf.space"
WHATSAPP_WEBHOOK_URL = f"{API_BASE_URL}/whatsapp/webhook"

def test_health_check():
    """Test the health endpoint to ensure the app is running"""
    print("🔍 Testing health check...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            print(f"   WhatsApp service: {data['details']['whatsapp_service']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_menu_based_flow():
    """Test the new menu-based flow"""
    print("\n📱 Testing Menu-Based Flow...")
    
    # Test conversation flow
    test_conversation = [
        ("Hi", "Welcome message"),
        ("menu", "Main menu"),
        ("1", "Q&A menu"),
        ("Tell me about Kigali", "Q&A response"),
        ("menu", "Main menu again"),
        ("2", "Translation menu"),
        ("a", "English to Kinyarwanda input"),
        ("Hello, how are you?", "Translation response"),
        ("menu", "Main menu again"),
        ("3", "Location menu"),
        ("Where is Kimironko?", "Location response"),
        ("menu", "Main menu again"),
        ("4", "Weather menu"),
        ("What's the weather today?", "Weather response"),
        ("quit", "Reset to welcome"),
        ("Hi", "Welcome message again"),
    ]
    
    for i, (message, description) in enumerate(test_conversation, 1):
        print(f"\n🧪 Test {i}: {description}")
        print(f"   Message: '{message}'")
        
        try:
            # Simulate webhook call
            webhook_data = {
                "From": "whatsapp:+1234567890",
                "Body": message,
                "To": "whatsapp:+14155238886"
            }
            
            response = requests.post(
                WHATSAPP_WEBHOOK_URL,
                data=webhook_data,
                timeout=60
            )
            
            if response.status_code == 200:
                print(f"   ✅ Response received (length: {len(response.text)} chars)")
                
                # Check if it's valid TwiML
                if "<?xml" in response.text and "<Response>" in response.text:
                    print("   ✅ Valid TwiML response")
                    
                    # Extract message content for verification
                    if "<Message>" in response.text:
                        start = response.text.find("<Message>") + 9
                        end = response.text.find("</Message>")
                        if start > 8 and end > start:
                            message_content = response.text[start:end].strip()
                            # Check for expected content based on flow
                            if i == 1 and "Welcome" in message_content:
                                print("   ✅ Welcome message detected")
                            elif i == 2 and "Main Menu" in message_content:
                                print("   ✅ Main menu detected")
                            elif i == 3 and "Question & Answer" in message_content:
                                print("   ✅ Q&A menu detected")
                            elif i == 4 and "Answer:" in message_content:
                                print("   ✅ Q&A response detected")
                            elif i == 5 and "Main Menu" in message_content:
                                print("   ✅ Return to main menu detected")
                            elif i == 6 and "Translation Service" in message_content:
                                print("   ✅ Translation menu detected")
                            elif i == 7 and "English to Kinyarwanda" in message_content:
                                print("   ✅ Translation direction selected")
                            elif i == 8 and "Translation" in message_content:
                                print("   ✅ Translation response detected")
                            elif i == 9 and "Main Menu" in message_content:
                                print("   ✅ Return to main menu detected")
                            elif i == 10 and "Location Service" in message_content:
                                print("   ✅ Location menu detected")
                            elif i == 11 and "Location Information" in message_content:
                                print("   ✅ Location response detected")
                            elif i == 12 and "Main Menu" in message_content:
                                print("   ✅ Return to main menu detected")
                            elif i == 13 and "Weather Service" in message_content:
                                print("   ✅ Weather menu detected")
                            elif i == 14 and "Weather Information" in message_content:
                                print("   ✅ Weather response detected")
                            elif i == 15 and "Welcome" in message_content:
                                print("   ✅ Reset to welcome detected")
                            elif i == 16 and "Welcome" in message_content:
                                print("   ✅ Welcome message after reset detected")
                            else:
                                print(f"   ⚠️  Unexpected content: {message_content[:50]}...")
                else:
                    print("   ⚠️  Response is not valid TwiML")
                    
            else:
                print(f"   ❌ Failed: {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(1)  # Rate limiting

def test_global_commands():
    """Test global commands like menu and quit"""
    print("\n🔧 Testing Global Commands...")
    
    global_commands = [
        ("menu", "Should show main menu"),
        ("quit", "Should reset to welcome"),
        ("MENU", "Should show main menu (case insensitive)"),
        ("Menu", "Should show main menu (case insensitive)"),
    ]
    
    for message, description in global_commands:
        print(f"\n🧪 Testing: {description}")
        print(f"   Command: '{message}'")
        
        try:
            webhook_data = {
                "From": "whatsapp:+1234567890",
                "Body": message,
                "To": "whatsapp:+14155238886"
            }
            
            response = requests.post(
                WHATSAPP_WEBHOOK_URL,
                data=webhook_data,
                timeout=60
            )
            
            if response.status_code == 200:
                print(f"   ✅ Response received (length: {len(response.text)} chars)")
                
                # Check for expected content
                if "menu" in message.lower() and "Main Menu" in response.text:
                    print("   ✅ Main menu displayed correctly")
                elif "quit" in message.lower() and "Welcome" in response.text:
                    print("   ✅ Reset to welcome correctly")
                else:
                    print("   ⚠️  Unexpected response content")
                    
            else:
                print(f"   ❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(1)  # Rate limiting

def test_error_handling():
    """Test error handling and invalid inputs"""
    print("\n⚠️  Testing Error Handling...")
    
    error_cases = [
        ("", "Empty message"),
        ("invalid_option", "Invalid menu selection"),
        ("99", "Invalid menu number"),
        ("z", "Invalid translation option"),
    ]
    
    for message, description in error_cases:
        print(f"\n🧪 Testing: {description}")
        print(f"   Input: '{message}'")
        
        try:
            webhook_data = {
                "From": "whatsapp:+1234567890",
                "Body": message,
                "To": "whatsapp:+14155238886"
            }
            
            response = requests.post(
                WHATSAPP_WEBHOOK_URL,
                data=webhook_data,
                timeout=60
            )
            
            if response.status_code == 200:
                print(f"   ✅ Response received (length: {len(response.text)} chars)")
                
                # Check for error handling
                if "valid option" in response.text or "Please select" in response.text:
                    print("   ✅ Proper error handling detected")
                else:
                    print("   ⚠️  No specific error handling detected")
                    
            else:
                print(f"   ❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(1)  # Rate limiting

def main():
    """Run all WhatsApp integration tests"""
    print("🚀 Starting WhatsApp Menu-Based Integration Tests")
    print("=" * 60)
    
    # Test health check first
    if not test_health_check():
        print("❌ Health check failed. Please ensure the app is running.")
        return
    
    # Run all tests
    test_menu_based_flow()
    test_global_commands()
    test_error_handling()
    
    print("\n" + "=" * 60)
    print("✅ WhatsApp Menu-Based Integration Tests Complete!")
    print("\n📋 Next Steps:")
    print("1. Set up Twilio account and get credentials")
    print("2. Configure environment variables")
    print("3. Set webhook URL in Twilio console")
    print("4. Test with real WhatsApp messages")
    print("\n📖 See docs/WHATSAPP_SETUP_GUIDE.md for detailed setup instructions")

if __name__ == "__main__":
    main() 