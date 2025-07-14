import os
from pathlib import Path
from pydantic import BaseModel

class Settings(BaseModel):
    # Paths
    persistent_dir: str = os.getenv("PERSISTENT_DIR", "/data")
    model_cache: str = os.getenv("MODEL_CACHE", "/data/models")
    vector_db_path: str = os.getenv("VECTOR_DB_PATH", "/data/vector_db")
    
    # Models
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    llm_model: str = "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF"
    llm_model_file: str = "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
    
    # Translation models
    en2rw_model: str = "facebook/nllb-200-distilled-600M"
    rw2en_model: str = "facebook/nllb-200-distilled-600M"
    
    # Improved translation options
    use_improved_translation: bool = True
    google_translate_api_key: str = os.getenv("GOOGLE_TRANSLATE_API_KEY", "")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    
    # Google Maps API
    google_maps_api_key: str = os.getenv("GOOGLE_MAPS_API_KEY", "")
    default_location: str = "Kigali, Rwanda"
    
    # Weather API
    openweather_api_key: str = os.getenv("OPENWEATHER_API_KEY", "")
    weather_default_city: str = "Kigali"
    weather_default_country: str = "RW"
    
    # Twilio WhatsApp API
    twilio_account_sid: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    twilio_auth_token: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    twilio_phone_number: str = os.getenv("TWILIO_PHONE_NUMBER", "")
    whatsapp_api_base_url: str = os.getenv("WHATSAPP_API_BASE_URL", "https://lola97-hura-chatbot.hf.space")
    
    # API settings
    host: str = "0.0.0.0"
    port: int = 7860  # Hugging Face Spaces port
    
    # Model settings
    max_new_tokens: int = 256
    temperature: float = 0.3
    gpu_layers: int = 0
    batch_size: int = 32
    context_length: int = 2048
    threads: int = 8
    
    # Retrieval settings
    search_k: int = 2
    search_type: str = "mmr"
    
    @property
    def persistent_path(self) -> Path:
        return Path(self.persistent_dir)
    
    @property
    def model_cache_path(self) -> Path:
        return Path(self.model_cache)
    
    @property
    def vector_db_path_obj(self) -> Path:
        return Path(self.vector_db_path)

# Global settings instance
settings = Settings() 