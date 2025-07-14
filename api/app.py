import os
import gc
import logging
import time
import shutil
import torch
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Import our modular components
from config import settings
from utils.helpers import ensure_directories, get_dir_size
from services.vector_store import VectorStoreService
from services.rag_service import RAGService
from services.translation import TranslationService
from services.maps_service import MapsService
from services.weather_service import WeatherService
from api.models_enhanced import (
    Query, TranslationRequest, QueryResponse, TranslationResponse, 
    HealthResponse, RootResponse, MenuResponse, MapsQuery, WeatherQuery
)
from middleware.rate_limiter import RateLimiter, rate_limit_middleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check GPU availability
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
logger.info(f"Using device: {DEVICE.upper()}")

# Initialize FastAPI app
app = FastAPI(
    title="Hura Tourism Chatbot (Menu-Based)",
    description="AI assistant for tourists visiting Kigali, Rwanda with dedicated endpoints for each feature",
    version="2.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Initialize rate limiter
rate_limiter = RateLimiter(requests_per_minute=60)
app.middleware("http")(rate_limit_middleware(rate_limiter))

# Global service instances
vector_store_service = None
rag_service = None
translation_service = None
maps_service = None
weather_service = None

@app.on_event("startup")
async def startup_event():
    """Initialize application with all services"""
    global vector_store_service, rag_service, translation_service, maps_service, weather_service
    
    try:
        # Optimize memory usage
        gc.collect()
        gc.freeze()
        
        # Ensure directories exist
        ensure_directories(
            settings.persistent_path,
            settings.model_cache_path,
            settings.vector_db_path_obj
        )
        
        # Initialize vector store service
        logger.info("Initializing vector store service...")
        vector_store_service = VectorStoreService()
        vector_store_service.initialize()
        
        # Initialize RAG service
        logger.info("Initializing RAG service...")
        rag_service = RAGService(vector_store_service)
        rag_service.initialize()
        
        # Initialize translation service
        logger.info("Initializing translation service...")
        translation_service = TranslationService()
        translation_service.initialize()
        
        # Initialize maps service
        logger.info("Initializing maps service...")
        maps_service = MapsService()
        maps_service.initialize()
        
        # Initialize weather service
        logger.info("Initializing weather service...")
        weather_service = WeatherService()
        weather_service.initialize()
        
        logger.info("Menu-based application startup complete! All services ready.")
        
    except Exception as e:
        logger.critical(f"Startup failed: {e}")
        shutil.rmtree(settings.vector_db_path_obj, ignore_errors=True)
        os.makedirs(settings.vector_db_path_obj, exist_ok=True)
        raise RuntimeError("Startup initialization failed") from e

@app.get("/", response_model=RootResponse)
def read_root():
    return RootResponse(
        message="Welcome to Hura Tourism Chatbot! Choose your service from the menu below.",
        endpoints={
            "menu": "GET /menu",
            "ask_question": "POST /ask",
            "translate_en2rw": "POST /translate/en2rw",
            "translate_rw2en": "POST /translate/rw2en",
            "location_service": "POST /maps",
            "weather_service": "POST /weather",
            "health_check": "GET /health"
        },
        documentation="/docs"
    )

@app.get("/menu", response_model=MenuResponse)
def get_menu():
    """Get the main menu with all available features"""
    return MenuResponse(
        title="🌍 Hura Tourism Chatbot - Main Menu",
        description="Choose a service to get started:",
        options=[
            {
                "id": "1",
                "title": "🤖 Ask a Question",
                "description": "Get information about Kigali, tourism, culture, and more",
                "endpoint": "/ask",
                "method": "POST",
                "example": {"text": "Tell me about Kigali Genocide Memorial"}
            },
            {
                "id": "2a",
                "title": "🔄 Translate: English → Kinyarwanda",
                "description": "Translate English text to Kinyarwanda",
                "endpoint": "/translate/en2rw",
                "method": "POST",
                "example": {"text": "Hello, how are you?"}
            },
            {
                "id": "2b",
                "title": "🔄 Translate: Kinyarwanda → English",
                "description": "Translate Kinyarwanda text to English",
                "endpoint": "/translate/rw2en",
                "method": "POST",
                "example": {"text": "Muraho, amakuru?"}
            },
            {
                "id": "3",
                "title": "🗺️ Location Service",
                "description": "Find places, get directions, and discover nearby locations",
                "endpoint": "/maps",
                "method": "POST",
                "example": {"query": "Where is Kimironko?"}
            },
            {
                "id": "4",
                "title": "🌤️ Weather Updates",
                "description": "Get current weather and forecasts for Kigali and Rwanda",
                "endpoint": "/weather",
                "method": "POST",
                "example": {"query": "What's the weather today?"}
            }
        ],
        features_status={
            "rag": rag_service is not None,
            "translation": translation_service is not None,
            "maps": maps_service is not None and settings.google_maps_api_key != "",
            "weather": weather_service is not None and settings.openweather_api_key != ""
        }
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        details={
            "rag_service": rag_service is not None,
            "translation_service": translation_service is not None,
            "maps_service": maps_service is not None,
            "weather_service": weather_service is not None,
            "persistent_storage": str(settings.persistent_path),
            "storage_usage": f"{get_dir_size(settings.persistent_path)/1024/1024:.2f} MB",
            "features": {
                "rag": rag_service is not None,
                "translation": translation_service is not None,
                "maps": settings.google_maps_api_key != "",
                "weather": settings.openweather_api_key != ""
            }
        }
    )

# ===== ENDPOINT 1: General Questions (RAG) =====
@app.post("/ask", response_model=QueryResponse)
async def answer_query(query: Query, request: Request):
    """Endpoint 1: Ask general questions about Kigali and tourism"""
    if not rag_service:
        raise HTTPException(status_code=503, detail="RAG service initializing, try again in 30 seconds")
    
    try:
        start_time = time.time()
        response = rag_service.query(query.text)
        process_time = time.time() - start_time
        
        return QueryResponse(
            response=response,
            processing_time=f"{process_time:.2f} seconds",
            service_used="RAG"
        )
    except Exception as e:
        logger.error(f"RAG query processing error: {e}")
        raise HTTPException(status_code=500, detail="Error processing your question") from e

# ===== ENDPOINT 2: Translation Services =====
@app.post("/translate/en2rw", response_model=TranslationResponse)
async def translate_en2rw(req: TranslationRequest, request: Request):
    """Endpoint 2a: Translate English to Kinyarwanda"""
    if not translation_service:
        raise HTTPException(status_code=503, detail="Translation service not loaded yet.")
    
    try:
        translation = translation_service.translate_en_to_rw(req.text)
        return TranslationResponse(
            translation=translation,
            source_language="English",
            target_language="Kinyarwanda",
            service_used="NLLB-200"
        )
    except Exception as e:
        logger.error(f"Translation error (en2rw): {e}")
        raise HTTPException(status_code=500, detail="Translation failed.")

@app.post("/translate/rw2en", response_model=TranslationResponse)
async def translate_rw2en(req: TranslationRequest, request: Request):
    """Endpoint 2b: Translate Kinyarwanda to English"""
    if not translation_service:
        raise HTTPException(status_code=503, detail="Translation service not loaded yet.")
    
    try:
        translation = translation_service.translate_rw_to_en(req.text)
        return TranslationResponse(
            translation=translation,
            source_language="Kinyarwanda",
            target_language="English",
            service_used="NLLB-200"
        )
    except Exception as e:
        logger.error(f"Translation error (rw2en): {e}")
        raise HTTPException(status_code=500, detail="Translation failed.")

# ===== ENDPOINT 3: Location Service =====
@app.post("/maps", response_model=QueryResponse)
async def maps_service_endpoint(query: MapsQuery, request: Request):
    """Endpoint 3: Location and directions service"""
    if not maps_service:
        raise HTTPException(status_code=503, detail="Maps service not available.")
    
    try:
        start_time = time.time()
        response = maps_service.process_maps_query(query.query)
        process_time = time.time() - start_time
        
        return QueryResponse(
            response=response,
            processing_time=f"{process_time:.2f} seconds",
            service_used="Google Maps"
        )
    except Exception as e:
        logger.error(f"Maps query processing error: {e}")
        raise HTTPException(status_code=500, detail="Error processing location request") from e

# ===== ENDPOINT 4: Weather Service =====
@app.post("/weather", response_model=QueryResponse)
async def weather_service_endpoint(query: WeatherQuery, request: Request):
    """Endpoint 4: Weather information service"""
    if not weather_service:
        raise HTTPException(status_code=503, detail="Weather service not available.")
    
    try:
        start_time = time.time()
        response = weather_service.process_weather_query(query.query)
        process_time = time.time() - start_time
        
        return QueryResponse(
            response=response,
            processing_time=f"{process_time:.2f} seconds",
            service_used="OpenWeather"
        )
    except Exception as e:
        logger.error(f"Weather query processing error: {e}")
        raise HTTPException(status_code=500, detail="Error processing weather request") from e

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=settings.host, 
        port=settings.port,
        server_header=False,
        date_header=False,
        timeout_keep_alive=30
    ) 