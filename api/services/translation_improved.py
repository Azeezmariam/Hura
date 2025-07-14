import logging
import requests
import time
from typing import Optional, Dict, Any
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch

from config import settings

logger = logging.getLogger(__name__)

class ImprovedTranslationService:
    def __init__(self):
        self.en2rw_translator = None
        self.rw2en_translator = None
        self.fallback_translator = None
        self.use_api_fallback = False
        
    def initialize_models(self):
        """Initialize translation models with better options"""
        try:
            logger.info("Loading improved translation models...")
            
            # Primary models (better than Helsinki-NLP)
            primary_models = {
                "en2rw": "facebook/nllb-200-distilled-600M",  # Better multilingual model
                "rw2en": "facebook/nllb-200-distilled-600M"
            }
            
            # Fallback models
            fallback_models = {
                "en2rw": "Helsinki-NLP/opus-mt-en-rw",
                "rw2en": "Helsinki-NLP/opus-mt-rw-en"
            }
            
            # Try to load primary models
            try:
                logger.info("Loading primary NLLB models...")
                self.en2rw_translator = pipeline(
                    "translation", 
                    model=primary_models["en2rw"],
                    src_lang="eng_Latn",
                    tgt_lang="kin_Latn"
                )
                self.rw2en_translator = pipeline(
                    "translation", 
                    model=primary_models["rw2en"],
                    src_lang="kin_Latn", 
                    tgt_lang="eng_Latn"
                )
                logger.info("Primary NLLB models loaded successfully")
                
            except Exception as e:
                logger.warning(f"Failed to load primary models: {e}")
                logger.info("Falling back to Helsinki-NLP models...")
                
                # Fallback to original models
                self.en2rw_translator = pipeline("translation", model=fallback_models["en2rw"])
                self.rw2en_translator = pipeline("translation", model=fallback_models["rw2en"])
            
            # Initialize API fallback if configured
            if hasattr(settings, 'google_translate_api_key') and settings.google_translate_api_key:
                self.use_api_fallback = True
                logger.info("Google Translate API fallback enabled")
            
            logger.info("Translation service initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing translation models: {e}")
            raise
    
    def translate_with_google_api(self, text: str, target_lang: str) -> Optional[str]:
        """Fallback to Google Translate API"""
        if not self.use_api_fallback:
            return None
            
        try:
            # This is a placeholder - you'd need to implement actual Google Translate API
            # For now, we'll return None to indicate API fallback is not implemented
            logger.warning("Google Translate API fallback not implemented")
            return None
        except Exception as e:
            logger.error(f"Google Translate API error: {e}")
            return None
    
    def post_process_translation(self, text: str, direction: str) -> str:
        """Post-process translations for better quality"""
        # Remove extra whitespace
        text = " ".join(text.split())
        
        # Fix common translation issues
        if direction == "en2rw":
            # Common English->Kinyarwanda fixes
            text = text.replace("  ", " ")
            # Add more specific fixes based on your observations
        elif direction == "rw2en":
            # Common Kinyarwanda->English fixes
            text = text.replace("  ", " ")
            # Add more specific fixes based on your observations
        
        return text.strip()
    
    def translate_en_to_rw(self, text: str) -> str:
        """Translate English text to Kinyarwanda with fallback"""
        if not self.en2rw_translator:
            raise RuntimeError("English to Kinyarwanda translator not initialized")
        
        try:
            # Try primary translation
            result = self.en2rw_translator(text)
            translation = result[0]['translation_text']
            
            # Post-process
            translation = self.post_process_translation(translation, "en2rw")
            
            # Log translation for quality monitoring
            logger.info(f"Translation (en->rw): '{text}' -> '{translation}'")
            
            return translation
            
        except Exception as e:
            logger.error(f"Translation error (en2rw): {e}")
            
            # Try API fallback
            if self.use_api_fallback:
                api_result = self.translate_with_google_api(text, "rw")
                if api_result:
                    return api_result
            
            # Return original text as last resort
            logger.warning(f"Translation failed, returning original text: {text}")
            return text
    
    def translate_rw_to_en(self, text: str) -> str:
        """Translate Kinyarwanda text to English with fallback"""
        if not self.rw2en_translator:
            raise RuntimeError("Kinyarwanda to English translator not initialized")
        
        try:
            # Try primary translation
            result = self.rw2en_translator(text)
            translation = result[0]['translation_text']
            
            # Post-process
            translation = self.post_process_translation(translation, "rw2en")
            
            # Log translation for quality monitoring
            logger.info(f"Translation (rw->en): '{text}' -> '{translation}'")
            
            return translation
            
        except Exception as e:
            logger.error(f"Translation error (rw2en): {e}")
            
            # Try API fallback
            if self.use_api_fallback:
                api_result = self.translate_with_google_api(text, "en")
                if api_result:
                    return api_result
            
            # Return original text as last resort
            logger.warning(f"Translation failed, returning original text: {text}")
            return text
    
    def get_translation_quality_score(self, original: str, translation: str) -> float:
        """Simple quality scoring (placeholder for more sophisticated metrics)"""
        # This is a basic implementation - you could use more sophisticated metrics
        if not original or not translation:
            return 0.0
        
        # Simple length ratio check
        length_ratio = len(translation) / len(original)
        if 0.3 <= length_ratio <= 3.0:
            return 0.8
        else:
            return 0.4
    
    def initialize(self):
        """Initialize the translation service"""
        self.initialize_models() 