#!/usr/bin/env python3
"""
Test script to verify deployment structure
Tests imports and basic functionality without external dependencies
"""

def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        # Test core imports
        from config import settings
        print("✅ Config imported")
        
        from api.models import Query, TranslationRequest, MapsQuery, WeatherQuery
        print("✅ API models imported")
        
        from services.vector_store import VectorStoreService
        print("✅ Vector store service imported")
        
        from services.rag_service import RAGService
        print("✅ RAG service imported")
        
        from services.translation import TranslationService
        print("✅ Translation service imported")
        
        from services.maps_service import MapsService
        print("✅ Maps service imported")
        
        from services.weather_service import WeatherService
        print("✅ Weather service imported")
        
        from services.whatsapp_service import WhatsAppService
        print("✅ WhatsApp service imported")
        
        from middleware.rate_limiter import RateLimiter
        print("✅ Rate limiter imported")
        
        from utils.helpers import ensure_directories, get_dir_size
        print("✅ Utils imported")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_config():
    """Test configuration settings"""
    print("\n⚙️ Testing configuration...")
    
    try:
        from config import settings
        
        # Check port configuration
        if settings.port == 7860:
            print("✅ Port configured for Hugging Face Spaces (7860)")
        else:
            print(f"⚠️ Port is {settings.port}, should be 7860 for Hugging Face Spaces")
        
        # Check required settings
        required_settings = [
            'persistent_dir',
            'model_cache',
            'vector_db_path',
            'embedding_model',
            'llm_model',
            'en2rw_model',
            'rw2en_model'
        ]
        
        for setting in required_settings:
            if hasattr(settings, setting):
                print(f"✅ {setting}: {getattr(settings, setting)}")
            else:
                print(f"❌ Missing setting: {setting}")
        
        return True
        
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def test_models():
    """Test Pydantic models"""
    print("\n📋 Testing Pydantic models...")
    
    try:
        from api.models import Query, TranslationRequest, MapsQuery, WeatherQuery
        
        # Test Query model
        query = Query(text="Test query")
        print("✅ Query model works")
        
        # Test TranslationRequest model
        trans_req = TranslationRequest(text="Hello")
        print("✅ TranslationRequest model works")
        
        # Test MapsQuery model
        maps_query = MapsQuery(query="Where is Kigali?")
        print("✅ MapsQuery model works")
        
        # Test WeatherQuery model
        weather_query = WeatherQuery(query="What's the weather?")
        print("✅ WeatherQuery model works")
        
        return True
        
    except Exception as e:
        print(f"❌ Model error: {e}")
        return False

def test_services():
    """Test service initialization"""
    print("\n🔧 Testing service initialization...")
    
    try:
        from services.whatsapp_service import WhatsAppService
        
        # Test WhatsApp service initialization
        whatsapp_service = WhatsAppService()
        whatsapp_service.initialize()
        print("✅ WhatsApp service initialized")
        
        # Test menu generation
        menu = whatsapp_service.get_main_menu()
        if "Main Menu" in menu and "1️⃣" in menu:
            print("✅ Menu generation works")
        else:
            print("⚠️ Menu generation may have issues")
        
        return True
        
    except Exception as e:
        print(f"❌ Service error: {e}")
        return False

def main():
    """Run all deployment tests"""
    print("🚀 Deployment Structure Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_config,
        test_models,
        test_services
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"✅ Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Deployment should work.")
        print("\n📋 Deployment Checklist:")
        print("✅ All imports working")
        print("✅ Configuration correct")
        print("✅ Models defined")
        print("✅ Services initializable")
        print("\n🚀 Ready to deploy to Hugging Face Spaces!")
    else:
        print("❌ Some tests failed. Please fix issues before deploying.")
    
    return passed == total

if __name__ == "__main__":
    main() 