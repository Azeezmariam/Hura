import os
import logging
from pathlib import Path
from typing import List
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

from config import settings
from utils.helpers import load_data, deduplicate_data, fix_chromadb_schema

logger = logging.getLogger(__name__)

class VectorStoreService:
    def __init__(self):
        self.embeddings = None
        self.vector_store = None
        
    def ensure_embedding_model(self):
        """Ensure embedding model exists in persistent storage"""
        try:
            embedding_model_path = settings.model_cache_path / "embedding_model"
            if not os.path.exists(embedding_model_path):
                logger.info("Creating new embedding model...")
                from sentence_transformers import SentenceTransformer
                model = SentenceTransformer(settings.embedding_model)
                model.save(str(embedding_model_path))
            else:
                logger.info("Using existing embedding model from cache")
        except Exception as e:
            logger.error(f"Error with embedding model: {e}")
            raise
    
    def load_embeddings(self):
        """Load embedding model"""
        embedding_model_path = settings.model_cache_path / "embedding_model"
        self.embeddings = HuggingFaceEmbeddings(
            model_name=str(embedding_model_path),
            model_kwargs={"device": "cuda" if os.getenv("USE_GPU", "false").lower() == "true" else "cpu"}
        )
    
    def create_vector_store(self):
        """Create a new vector store from source data using Document objects"""
        try:
            # Load source data
            tripadvisor_data = load_data("data/tripadvisor_forum.json")
            faq_data = load_data("data/tourism_faq_gov.json")
            blog_data = load_data("data/local_blog_etiquette.json")
            
            # Combine and deduplicate data
            combined_data = deduplicate_data(tripadvisor_data + faq_data + blog_data)

            # Create documents
            documents = []
            for idx, item in enumerate(combined_data):
                doc_text = f"QUESTION: {item['question']}\nANSWER: {item['answer']}"
                
                # Determine source
                if idx < len(tripadvisor_data):
                    source = "tripadvisor"
                elif idx < len(tripadvisor_data) + len(faq_data):
                    source = "gov_faq"
                else:
                    source = "blog"
                
                metadata = {"source": source, "original_question": item['question']}
                documents.append(Document(page_content=doc_text, metadata=metadata))
            
            # Create new vector store
            logger.info("Creating new vector database...")
            self.vector_store = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=str(settings.vector_db_path_obj),
                collection_name="kigali_tourism",
                collection_metadata={"hnsw:space": "cosine"}
            )
            self.vector_store.persist()
            return self.vector_store
        except Exception as e:
            logger.error(f"Error creating vector store: {e}")
            raise
    
    def load_existing_vector_store(self):
        """Load existing vector store"""
        db_file = settings.vector_db_path_obj / "chroma.sqlite3"
        
        if os.path.exists(db_file):
            # Fix schema if needed
            fix_chromadb_schema(str(db_file))
            
            logger.info("Loading existing vector database...")
            self.vector_store = Chroma(
                persist_directory=str(settings.vector_db_path_obj),
                embedding_function=self.embeddings,
                collection_name="kigali_tourism"
            )
            return True
        return False
    
    def get_retriever(self):
        """Get configured retriever"""
        if not self.vector_store:
            raise RuntimeError("Vector store not initialized")
        
        return self.vector_store.as_retriever(
            search_type=settings.search_type,
            search_kwargs={"k": settings.search_k}
        )
    
    def initialize(self):
        """Initialize vector store service"""
        # Ensure embedding model exists
        self.ensure_embedding_model()
        
        # Load embedding model
        logger.info("Loading embedding model...")
        self.load_embeddings()
        
        # Try to load existing vector store, create new one if needed
        if not self.load_existing_vector_store():
            logger.info("Creating new vector database...")
            self.create_vector_store()
        
        logger.info("Vector store service initialized successfully") 