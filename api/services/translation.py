import logging
from transformers import pipeline

from config import settings

logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        self.en2rw_translator = None
        self.rw2en_translator = None
        
    def initialize_models(self):
        """Initialize translation models with NLLB-200"""
        try:
            logger.info("Loading NLLB-200 translation models for English<->Kinyarwanda...")
            
            # Use NLLB-200 for both directions with proper language codes
            self.en2rw_translator = pipeline(
                "translation", 
                model=settings.en2rw_model,
                src_lang="eng_Latn",
                tgt_lang="kin_Latn"
            )
            self.rw2en_translator = pipeline(
                "translation", 
                model=settings.rw2en_model,
                src_lang="kin_Latn",
                tgt_lang="eng_Latn"
            )
            logger.info("NLLB-200 translation models loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading NLLB-200 models: {e}")
            logger.info("Falling back to Helsinki-NLP models...")
            
            # Fallback to original models
            self.en2rw_translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-rw")
            self.rw2en_translator = pipeline("translation", model="Helsinki-NLP/opus-mt-rw-en")
    
    def translate_en_to_rw(self, text: str) -> str:
        """Translate English text to Kinyarwanda"""
        if not self.en2rw_translator:
            raise RuntimeError("English to Kinyarwanda translator not initialized")
        
        try:
            result = self.en2rw_translator(text)
            return result[0]['translation_text']
        except Exception as e:
            logger.error(f"Translation error (en2rw): {e}")
            raise
    
    def translate_rw_to_en(self, text: str) -> str:
        """Translate Kinyarwanda text to English"""
        if not self.rw2en_translator:
            raise RuntimeError("Kinyarwanda to English translator not initialized")
        
        try:
            result = self.rw2en_translator(text)
            return result[0]['translation_text']
        except Exception as e:
            logger.error(f"Translation error (rw2en): {e}")
            raise
    
    def initialize(self):
        """Initialize the translation service"""
        self.initialize_models() 