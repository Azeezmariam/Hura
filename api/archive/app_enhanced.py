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
from services.enhanced_rag_service import EnhancedRAGService
from services.translation import TranslationService
from api.models import Query, TranslationRequest, QueryResponse, TranslationResponse, HealthResponse, RootResponse
from middleware.rate_limiter import RateLimiter, rate_limit_middleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check GPU availability
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
logger.info(f"Using device: {DEVICE.upper()}")

# Initialize FastAPI app
app = FastAPI(
    title="Hura Tourism Chatbot (Enhanced)",
    description="AI assistant for tourists visiting Kigali, Rwanda with Maps & Weather",
    version="2.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Initialize rate limiter
rate_limiter = RateLimiter(requests_per_minute=60)
app.middleware("http")(rate_limit_middleware(rate_limiter))

# Global service instances
vector_store_service = None
enhanced_rag_service = None
translation_service = None

@app.on_event("startup")
async def startup_event():
    """Initialize application with enhanced services"""
    global vector_store_service, enhanced_rag_service, translation_service
    
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
        
        # Initialize translation service
        logger.info("Initializing translation service...")
        translation_service = TranslationService()
        translation_service.initialize()
        
        # Initialize enhanced RAG service (includes maps and weather)
        logger.info("Initializing enhanced RAG service...")
        enhanced_rag_service = EnhancedRAGService(vector_store_service, translation_service)
        enhanced_rag_service.initialize()
        
        logger.info("Enhanced application startup complete! Features: RAG + Maps + Weather + Translation")
        
    except Exception as e:
        logger.critical(f"Startup failed: {e}")
        # Attempt to clear corrupted files
        shutil.rmtree(settings.vector_db_path_obj, ignore_errors=True)
        os.makedirs(settings.vector_db_path_obj, exist_ok=True)
        raise RuntimeError("Startup initialization failed") from e

@app.get("/", response_model=RootResponse)
def read_root():
    return RootResponse(
        message="Welcome to Enhanced Hura Tourism Chatbot! Features: RAG + Maps + Weather + Translation",
        endpoints={
            "ask_question": "POST /ask",
            "health_check": "GET /health",
            "translate_en2rw": "POST /translate/en2rw",
            "translate_rw2en": "POST /translate/rw2en"
        },
        documentation="/docs"
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        details={
            "model_loaded": enhanced_rag_service is not None,
            "persistent_storage": str(settings.persistent_path),
            "storage_usage": f"{get_dir_size(settings.persistent_path)/1024/1024:.2f} MB",
            "features": {
                "rag": enhanced_rag_service is not None,
                "maps": settings.google_maps_api_key != "",
                "weather": settings.openweather_api_key != "",
                "translation": translation_service is not None
            }
        }
    )

@app.post("/ask", response_model=QueryResponse)
async def answer_query(query: Query, request: Request):
    if not enhanced_rag_service:
        raise HTTPException(status_code=503, detail="Service initializing, try again in 30 seconds")
    
    try:
        start_time = time.time()
        response = enhanced_rag_service.query(query.text)
        process_time = time.time() - start_time
        
        return QueryResponse(
            response=response,
            processing_time=f"{process_time:.2f} seconds"
        )
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail="Error processing your request") from e

@app.post("/translate/en2rw", response_model=TranslationResponse)
async def translate_en2rw(req: TranslationRequest, request: Request):
    if not translation_service:
        raise HTTPException(status_code=503, detail="Translation model not loaded yet.")
    
    try:
        translation = translation_service.translate_en_to_rw(req.text)
        return TranslationResponse(translation=translation)
    except Exception as e:
        logger.error(f"Translation error (en2rw): {e}")
        raise HTTPException(status_code=500, detail="Translation failed.")

@app.post("/translate/rw2en", response_model=TranslationResponse)
async def translate_rw2en(req: TranslationRequest, request: Request):
    if not translation_service:
        raise HTTPException(status_code=503, detail="Translation model not loaded yet.")
    
    try:
        translation = translation_service.translate_rw_to_en(req.text)
        return TranslationResponse(translation=translation)
    except Exception as e:
        logger.error(f"Translation error (rw2en): {e}")
        raise HTTPException(status_code=500, detail="Translation failed.")

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