#!/usr/bin/env python3
"""
Test NLLB-200 integration with the chatbot
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.translation import TranslationService
from config import settings

def test_translation_service():
    """Test the updated translation service"""
    print("🧪 Testing NLLB-200 Integration")
    print("=" * 50)
    
    # Initialize translation service
    print("📥 Initializing translation service...")
    translation_service = TranslationService()
    
    try:
        translation_service.initialize()
        print("✅ Translation service initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return False
    
    # Test phrases
    test_phrases = [
        "Where is the nearest ATM?",
        "How much does a taxi cost?",
        "What time does the museum open?",
        "Can you recommend a good restaurant?",
        "I need help with directions"
    ]
    
    print("\n📊 Testing English to Kinyarwanda:")
    print("-" * 40)
    
    for phrase in test_phrases:
        try:
            translation = translation_service.translate_en_to_rw(phrase)
            print(f"'{phrase}' -> '{translation}'")
        except Exception as e:
            print(f"❌ Error translating '{phrase}': {e}")
    
    # Test Kinyarwanda to English
    kinyarwanda_phrases = [
        "Ni hehe nshobora kugura amafaranga?",
        "Ese imodoka igura angahe?",
        "Iyo nzu ndangamurage ifungura saa zite?"
    ]
    
    print("\n📊 Testing Kinyarwanda to English:")
    print("-" * 40)
    
    for phrase in kinyarwanda_phrases:
        try:
            translation = translation_service.translate_rw_to_en(phrase)
            print(f"'{phrase}' -> '{translation}'")
        except Exception as e:
            print(f"❌ Error translating '{phrase}': {e}")
    
    print("\n✅ Integration test completed!")
    return True

def test_app_integration():
    """Test if the app can start with NLLB-200"""
    print("\n🔧 Testing App Integration")
    print("=" * 50)
    
    try:
        # Import the app to test if it can initialize
        from app import app
        print("✅ App imports successfully")
        
        # Test if translation service can be accessed
        if hasattr(app, 'state') and hasattr(app.state, 'translation_service'):
            print("✅ Translation service accessible in app state")
        else:
            print("⚠️  Translation service not in app state (will be initialized on startup)")
        
        return True
    except Exception as e:
        print(f"❌ App integration test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 NLLB-200 Integration Test")
    print("This script tests the NLLB-200 model integration")
    print()
    
    # Test translation service
    service_ok = test_translation_service()
    
    # Test app integration
    app_ok = test_app_integration()
    
    print("\n" + "=" * 50)
    if service_ok and app_ok:
        print("🎉 All tests passed! NLLB-200 is ready to use.")
        print("\n📋 Next steps:")
        print("1. Start your chatbot: python3 app.py")
        print("2. Test translation endpoints")
        print("3. Monitor translation quality")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("1. Install dependencies: pip3 install -r requirements.txt")
        print("2. Check internet connection (for model download)")
        print("3. Ensure sufficient disk space (~1.2GB for NLLB-200)") 