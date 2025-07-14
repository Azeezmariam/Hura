from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain_community.llms import CTransformers
from langchain.schema.output_parser import StrOutputParser
from langchain.schema import Document
import os
import sqlite3
import logging
import json
import gc
import time
import shutil
from pathlib import Path
import torch
from transformers import pipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Hugging Face Spaces specific configuration
PERSISTENT_DIR = Path(os.getenv("PERSISTENT_DIR", "/data"))
MODEL_CACHE = PERSISTENT_DIR / "models"
VECTOR_DB_PATH = PERSISTENT_DIR / "vector_db"
EMBEDDING_MODEL_PATH = MODEL_CACHE / "embedding_model"

app = FastAPI(
    title="Hura Tourism Chatbot",
    description="AI assistant for tourists visiting Kigali, Rwanda",
    version="1.0"
)

# Check GPU availability
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
logger.info(f"Using device: {DEVICE.upper()}")

def load_data(path: str):
    """Load JSON data files with improved error handling"""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading {path}: {e}")
        return []

def create_vector_store(embeddings):
    """Create a new vector store from source data using Document objects"""
    try:
        # Load source data
        tripadvisor_data = load_data("data/tripadvisor_forum.json")
        faq_data = load_data("data/tourism_faq_gov.json")
        blog_data = load_data("data/local_blog_etiquette.json")
        combined_data = tripadvisor_data + faq_data + blog_data

        # Create documents
        documents = []
        for idx, item in enumerate(combined_data):
            # Skip invalid items
            if 'question' not in item or 'answer' not in item:
                logger.warning(f"Skipping invalid item at index {idx}")
                continue
                
            doc_text = f"QUESTION: {item['question']}\nANSWER: {item['answer']}"
            source = "tripadvisor" if idx < len(tripadvisor_data) else "gov_faq" if idx < len(tripadvisor_data)+len(faq_data) else "blog"
            metadata = {"source": source, "original_question": item['question']}
            
            # Create proper Document objects
            documents.append(Document(page_content=doc_text, metadata=metadata))
        
        # Create new vector store
        logger.info("Creating new vector database...")
        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory=str(VECTOR_DB_PATH),
            collection_name="kigali_tourism",
            collection_metadata={"hnsw:space": "cosine"}
        )
        vector_store.persist()
        return vector_store
    except Exception as e:
        logger.error(f"Error creating vector store: {e}")
        raise

def fix_chromadb_schema(db_path):
    """Fix ChromaDB schema compatibility issues"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if topic column exists
        cursor.execute("PRAGMA table_info(collections)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'topic' not in columns:
            logger.info("Fixing ChromaDB schema...")
            # Add missing columns
            cursor.execute("ALTER TABLE collections ADD COLUMN topic TEXT")
            cursor.execute("ALTER TABLE collections ADD COLUMN dimensionality INTEGER")
            conn.commit()
        
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Schema fix failed: {e}")
        return False

def ensure_embedding_model():
    """Ensure embedding model exists in persistent storage"""
    try:
        if not os.path.exists(EMBEDDING_MODEL_PATH):
            logger.info("Creating new embedding model...")
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            model.save(str(EMBEDDING_MODEL_PATH))
        else:
            logger.info("Using existing embedding model from cache")
    except Exception as e:
        logger.error(f"Error with embedding model: {e}")
        raise

# Remove global translation pipeline variables
# en2rw_translator = None
# rw2en_translator = None

@app.on_event("startup")
async def startup_event():
    """Initialize application with GPU optimizations"""
    try:
        # Optimize memory usage
        gc.collect()
        gc.freeze()
        
        for path in [PERSISTENT_DIR, MODEL_CACHE, VECTOR_DB_PATH]:
            try:
                os.makedirs(path, exist_ok=True)
            except PermissionError:
                logger.warning(f"Skipping creation of {path} - already exists")
        
        # Ensure embedding model exists
        ensure_embedding_model()
        
        # Load embedding model
        logger.info("Loading embedding model...")
        embeddings = HuggingFaceEmbeddings(
            model_name=str(EMBEDDING_MODEL_PATH),
            model_kwargs={"device": DEVICE}
        )
        
        # Handle vector store
        db_file = VECTOR_DB_PATH / "chroma.sqlite3"
        
        if os.path.exists(db_file):
            # Fix schema if needed
            fix_chromadb_schema(str(db_file))
            
            logger.info("Loading existing vector database...")
            vector_store = Chroma(
                persist_directory=str(VECTOR_DB_PATH),
                embedding_function=embeddings,
                collection_name="kigali_tourism"
            )
        else:
            logger.info("Creating new vector database...")
            vector_store = create_vector_store(embeddings)
        
        # Load optimized model (TinyLlama-1.1B-Chat quantized)
        logger.info("Initializing TinyLlama-1.1B-Chat model...")
        llm = CTransformers(
            model="TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF",
            model_file="tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
            model_type="llama",
            config={
                'max_new_tokens': 256,
                'temperature': 0.3,
                'gpu_layers': 0,
                'batch_size': 32,
                'context_length': 2048,
                'threads': 8,
            }
        )
        
        # Create optimized prompt template
        template = """<|system|>
You are a tourism assistant for Kigali, Rwanda. Answer based ONLY on this context.
If answer isn't in context, say: "I couldn't find official info, contact tourism@rdb.rw".
Respond concisely in 1-2 sentences.</s>

Context:
{context}

<|user|>
{question}</s>
<|assistant|>
"""
        prompt = ChatPromptTemplate.from_template(template)
        
        # Build RAG chain with query optimization
        def expand_query(input: str):
            location_keywords = ["how to get", "transport", "where is", "directions to"]
            if any(kw in input.lower() for kw in location_keywords):
                return input + " in Kigali, Rwanda"
            return input

        # Use lightweight retriever configuration
        retriever = vector_store.as_retriever(
            search_type="mmr",  # Maximal marginal relevance for diversity
            search_kwargs={"k": 2}  # Only 2 documents to reduce processing
        )

        app.state.rag_chain = (
            {"context": retriever, 
             "question": RunnablePassthrough() | RunnableLambda(expand_query)}
            | prompt
            | llm
            | StrOutputParser()
        )
        
        # Load translation models
        logger.info("Loading translation models for English<->Kinyarwanda...")
        app.state.en2rw_translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-rw")
        app.state.rw2en_translator = pipeline("translation", model="Helsinki-NLP/opus-mt-rw-en")
        logger.info("Translation models loaded.")
        
        logger.info("Application startup complete! Running on CPU with limited resources")
        
    except Exception as e:
        logger.critical(f"Startup failed: {e}")
        # Attempt to clear corrupted files
        shutil.rmtree(VECTOR_DB_PATH, ignore_errors=True)
        os.makedirs(VECTOR_DB_PATH, exist_ok=True)
        raise RuntimeError("Startup initialization failed") from e

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Hura Tourism Chatbot API! (CPU Optimized)",
        "endpoints": {
            "ask_question": "POST /ask",
            "health_check": "GET /health"
        },
        "documentation": "/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "details": {
            "model_loaded": hasattr(app.state, "rag_chain"),
            "persistent_storage": str(PERSISTENT_DIR),
            "storage_usage": f"{get_dir_size(PERSISTENT_DIR)/1024/1024:.2f} MB"
        }
    }

def get_dir_size(path):
    total = 0
    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += get_dir_size(entry.path)
    return total

class Query(BaseModel):
    text: str

@app.post("/ask")
async def answer_query(query: Query, request: Request):
    if not hasattr(app.state, "rag_chain"):
        raise HTTPException(status_code=503, detail="Service initializing, try again in 30 seconds")
    
    try:
        start_time = time.time()
        response = app.state.rag_chain.invoke(query.text)
        process_time = time.time() - start_time
        
        logger.info(f"Processed query in {process_time:.2f}s: {query.text[:50]}{'...' if len(query.text) > 50 else ''}")
        return {
            "response": response,
            "processing_time": f"{process_time:.2f} seconds"
        }
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail="Error processing your request") from e

class TranslationRequest(BaseModel):
    text: str

@app.post("/translate/en2rw")
async def translate_en2rw(req: TranslationRequest, request: Request):
    translator = request.app.state.en2rw_translator
    if translator is None:
        raise HTTPException(status_code=503, detail="Translation model not loaded yet.")
    try:
        result = translator(req.text)
        return {"translation": result[0]['translation_text']}
    except Exception as e:
        logger.error(f"Translation error (en2rw): {e}")
        raise HTTPException(status_code=500, detail="Translation failed.")

@app.post("/translate/rw2en")
async def translate_rw2en(req: TranslationRequest, request: Request):
    translator = request.app.state.rw2en_translator
    if translator is None:
        raise HTTPException(status_code=503, detail="Translation model not loaded yet.")
    try:
        result = translator(req.text)
        return {"translation": result[0]['translation_text']}
    except Exception as e:
        logger.error(f"Translation error (rw2en): {e}")
        raise HTTPException(status_code=500, detail="Translation failed.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        server_header=False,
        date_header=False,
        timeout_keep_alive=30
    )