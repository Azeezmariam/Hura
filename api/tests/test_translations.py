#!/usr/bin/env python3
"""
Translation Quality Test Script
Compare different translation models for English-Kinyarwanda
"""

import time
from transformers import pipeline

def test_helsinki_nlp():
    """Test current Helsinki-NLP models"""
    print("🔍 Testing Helsinki-NLP models...")
    
    try:
        en2rw = pipeline("translation", model="Helsinki-NLP/opus-mt-en-rw")
        rw2en = pipeline("translation", model="Helsinki-NLP/opus-mt-rw-en")
        
        return en2rw, rw2en
    except Exception as e:
        print(f"❌ Error loading Helsinki-NLP: {e}")
        return None, None

def test_nllb_200():
    """Test Facebook NLLB-200 model"""
    print("🔍 Testing NLLB-200 model...")
    
    try:
        # NLLB-200 can handle both directions with language codes
        translator = pipeline("translation", model="facebook/nllb-200-distilled-600M")
        return translator
    except Exception as e:
        print(f"❌ Error loading NLLB-200: {e}")
        return None

def translate_with_nllb(translator, text: str, direction: str):
    """Translate using NLLB-200 with proper language codes"""
    if direction == "en2rw":
        return translator(text, src_lang="eng_Latn", tgt_lang="kin_Latn")
    else:
        return translator(text, src_lang="kin_Latn", tgt_lang="eng_Latn")

def test_translations():
    """Test both models with tourism phrases"""
    
    # Tourism-specific test phrases
    test_phrases = [
        "Where is the nearest ATM?",
        "How much does a taxi cost?",
        "What time does the museum open?",
        "Can you recommend a good restaurant?",
        "I need help with directions",
        "Where can I buy souvenirs?",
        "Is it safe to walk at night?",
        "How do I get to the airport?",
        "What is the weather like today?",
        "Do you speak English?"
    ]
    
    print("🧪 Testing Translation Quality")
    print("=" * 60)
    
    # Test Helsinki-NLP
    en2rw_helsinki, rw2en_helsinki = test_helsinki_nlp()
    
    # Test NLLB-200
    nllb_translator = test_nllb_200()
    
    if not en2rw_helsinki or not nllb_translator:
        print("❌ Could not load translation models")
        return
    
    print("\n📊 Translation Comparison Results:")
    print("=" * 60)
    
    for i, phrase in enumerate(test_phrases, 1):
        print(f"\n{i}. Original: {phrase}")
        
        # Helsinki-NLP translation
        try:
            start_time = time.time()
            helsinki_result = en2rw_helsinki(phrase)
            helsinki_time = time.time() - start_time
            helsinki_translation = helsinki_result[0]['translation_text']
        except Exception as e:
            helsinki_translation = f"ERROR: {e}"
            helsinki_time = 0
        
        # NLLB-200 translation
        try:
            start_time = time.time()
            nllb_result = translate_with_nllb(nllb_translator, phrase, "en2rw")
            nllb_time = time.time() - start_time
            nllb_translation = nllb_result[0]['translation_text']
        except Exception as e:
            nllb_translation = f"ERROR: {e}"
            nllb_time = 0
        
        print(f"   Helsinki-NLP: {helsinki_translation} ({helsinki_time:.2f}s)")
        print(f"   NLLB-200:     {nllb_translation} ({nllb_time:.2f}s)")
        
        # Simple quality comparison
        if "ERROR" not in helsinki_translation and "ERROR" not in nllb_translation:
            helsinki_length = len(helsinki_translation)
            nllb_length = len(nllb_translation)
            
            if abs(helsinki_length - nllb_length) > 10:
                print(f"   ⚠️  Length difference: {abs(helsinki_length - nllb_length)} chars")
    
    print("\n" + "=" * 60)
    print("📈 Summary:")
    print("- Helsinki-NLP: Current model, smaller size, faster")
    print("- NLLB-200: Better accuracy, larger size, slightly slower")
    print("\n💡 Recommendation: Try NLLB-200 for better quality!")

def test_model_sizes():
    """Test model loading times and sizes"""
    print("\n📏 Model Size Comparison:")
    print("=" * 40)
    
    # Helsinki-NLP models
    try:
        print("Loading Helsinki-NLP models...")
        start_time = time.time()
        en2rw = pipeline("translation", model="Helsinki-NLP/opus-mt-en-rw")
        rw2en = pipeline("translation", model="Helsinki-NLP/opus-mt-rw-en")
        helsinki_time = time.time() - start_time
        print(f"✅ Helsinki-NLP loaded in {helsinki_time:.2f}s")
    except Exception as e:
        print(f"❌ Helsinki-NLP failed: {e}")
    
    # NLLB-200 model
    try:
        print("Loading NLLB-200 model...")
        start_time = time.time()
        nllb = pipeline("translation", model="facebook/nllb-200-distilled-600M")
        nllb_time = time.time() - start_time
        print(f"✅ NLLB-200 loaded in {nllb_time:.2f}s")
    except Exception as e:
        print(f"❌ NLLB-200 failed: {e}")

if __name__ == "__main__":
    print("🚀 Translation Quality Test")
    print("This script will test different translation models")
    print("Make sure you have the required dependencies installed:")
    print("pip install transformers[torch] sentencepiece")
    print()
    
    # Test model loading
    test_model_sizes()
    
    # Test translations
    test_translations()
    
    print("\n🎯 Next Steps:")
    print("1. Review the translation quality above")
    print("2. If NLLB-200 looks better, update your config.py")
    print("3. Replace services/translation.py with services/translation_improved.py")
    print("4. Test with your actual tourism chatbot") 