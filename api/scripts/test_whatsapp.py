#!/usr/bin/env python3
"""
Simple WhatsApp integration test script
Tests the menu-based flow
"""

import requests
import sys

def test_whatsapp_webhook(message: str, api_url: str = "http://localhost:8000"):
    """Test the WhatsApp webhook with a given message"""
    
    webhook_url = f"{api_url}/whatsapp/webhook"
    
    # Simulate Twilio webhook data
    webhook_data = {
        "From": "whatsapp:+1234567890",
        "Body": message,
        "To": "whatsapp:+14155238886"
    }
    
    print(f"📱 Testing: '{message}'")
    
    try:
        response = requests.post(
            webhook_url,
            data=webhook_data,
            timeout=60
        )
        
        if response.status_code == 200:
            print(f"   ✅ Success! Response length: {len(response.text)} chars")
            
            # Extract message content if it's TwiML
            if "<?xml" in response.text and "<Message>" in response.text:
                start = response.text.find("<Message>") + 9
                end = response.text.find("</Message>")
                if start > 8 and end > start:
                    message_content = response.text[start:end].strip()
                    print(f"   📄 Content: {message_content[:100]}...")
        else:
            print(f"   ❌ Failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_menu_flow():
    """Test the complete menu flow"""
    print("🚀 Testing Menu-Based Flow")
    print("=" * 40)
    
    # Test the complete conversation flow
    flow = [
        ("Hi", "Welcome message"),
        ("menu", "Main menu"),
        ("1", "Select Q&A"),
        ("Tell me about Kigali", "Q&A response"),
        ("menu", "Back to main menu"),
        ("2", "Select Translation"),
        ("a", "Select English to Kinyarwanda"),
        ("Hello, how are you?", "Translation response"),
        ("menu", "Back to main menu"),
        ("quit", "Reset to welcome"),
    ]
    
    api_url = "http://localhost:8000"
    
    for message, description in flow:
        print(f"\n🧪 {description}")
        test_whatsapp_webhook(message, api_url)
        print()

def main():
    """Main function"""
    
    # Check if custom message provided
    if len(sys.argv) > 1:
        custom_message = " ".join(sys.argv[1:])
        api_url = "http://localhost:8000"
        
        # Check if custom API URL provided
        if "--url" in sys.argv:
            try:
                url_index = sys.argv.index("--url")
                api_url = sys.argv[url_index + 1]
            except (ValueError, IndexError):
                print("❌ Invalid --url parameter")
                return
        
        print(f"🚀 Testing custom message: '{custom_message}'")
        test_whatsapp_webhook(custom_message, api_url)
    else:
        # Run the complete menu flow test
        test_menu_flow()
    
    print("\n✅ Test complete!")

if __name__ == "__main__":
    main() 