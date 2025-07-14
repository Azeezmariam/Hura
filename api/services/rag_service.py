import logging
import time
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain_community.llms import CTransformers
from langchain.schema.output_parser import StrOutputParser

from config import settings

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self, vector_store_service):
        self.vector_store_service = vector_store_service
        self.llm = None
        self.rag_chain = None
        
    def initialize_llm(self):
        """Initialize the language model"""
        logger.info("Initializing TinyLlama-1.1B-Chat model...")
        self.llm = CTransformers(
            model=settings.llm_model,
            model_file=settings.llm_model_file,
            model_type="llama",
            config={
                'max_new_tokens': settings.max_new_tokens,
                'temperature': settings.temperature,
                'gpu_layers': settings.gpu_layers,
                'batch_size': settings.batch_size,
                'context_length': settings.context_length,
                'threads': settings.threads,
            }
        )
    
    def create_prompt_template(self):
        """Create the prompt template for the RAG chain"""
        template = """<|system|>
You are a tourism assistant for Kigali, Rwanda. Answer the user's question as helpfully and specifically as possible, using the information provided below. Do not mention or refer to the information source or context in your answer. If you don't know the answer, say: \"I couldn't find official info, contact tourism@rdb.rw\". Respond concisely in 2-3 sentences.</s>

Information:
{context}

<|user|>
{question}</s>
<|assistant|>
"""
        return ChatPromptTemplate.from_template(template)
    
    def expand_query(self, input_text: str) -> str:
        """Expand query with location-specific keywords"""
        location_keywords = ["how to get", "transport", "where is", "directions to"]
        if any(kw in input_text.lower() for kw in location_keywords):
            return input_text + " in Kigali, Rwanda"
        return input_text
    
    def build_rag_chain(self):
        """Build the RAG chain with query optimization"""
        # Get retriever from vector store service
        retriever = self.vector_store_service.get_retriever()
        
        # Create prompt template
        prompt = self.create_prompt_template()
        
        # Build RAG chain
        self.rag_chain = (
            {"context": retriever, 
             "question": RunnablePassthrough() | RunnableLambda(self.expand_query)}
            | prompt
            | self.llm
            | StrOutputParser()
        )
    
    def query(self, text: str) -> str:
        """Process a query through the RAG chain"""
        if not self.rag_chain:
            raise RuntimeError("RAG chain not initialized")
        
        start_time = time.time()
        try:
            response = self.rag_chain.invoke(text)
            process_time = time.time() - start_time
            
            logger.info(f"Processed query in {process_time:.2f}s: {text[:50]}{'...' if len(text) > 50 else ''}")
            return response
        except Exception as e:
            logger.error(f"Query processing error: {e}")
            raise
    
    def initialize(self):
        """Initialize the RAG service"""
        # Initialize LLM
        self.initialize_llm()
        
        # Build RAG chain
        self.build_rag_chain()
        
        logger.info("RAG service initialized successfully") 