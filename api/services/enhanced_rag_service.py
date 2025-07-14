import logging
import time
from typing import Optional, Dict, Any
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain_community.llms import CTransformers
from langchain.schema.output_parser import StrOutputParser

from config import settings
from services.maps_service import MapsService
from services.weather_service import WeatherService

logger = logging.getLogger(__name__)

class EnhancedRAGService:
    def __init__(self, vector_store_service, translation_service):
        self.vector_store_service = vector_store_service
        self.translation_service = translation_service
        self.maps_service = MapsService()
        self.weather_service = WeatherService()
        self.llm = None
        self.rag_chain = None
        
    def initialize_services(self):
        """Initialize all services"""
        # Initialize maps and weather services
        self.maps_service.initialize()
        self.weather_service.initialize()
        
        logger.info("Enhanced RAG services initialized")
    
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
You are a tourism assistant for Kigali, Rwanda. Answer the user's question as helpfully and specifically as possible, using the information provided below and any additional information. Do not mention or refer to the information source or context in your answer. If you don't know the answer, say: \"I couldn't find official info, contact tourism@rdb.rw\". Respond concisely in 1-2 sentences.</s>

Information:
{context}

Additional Information:
{additional_info}

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
    
    def detect_query_type(self, query: str) -> Dict[str, Any]:
        """Detect the type of query and extract relevant information"""
        query_lower = query.lower()
        
        result = {
            "is_maps": False,
            "is_weather": False,
            "is_translation": False,
            "is_general": True,
            "extracted_info": {}
        }
        
        # Check for maps queries
        if self.maps_service.is_maps_query(query):
            result["is_maps"] = True
            result["is_general"] = False
            result["extracted_info"]["location"] = self.maps_service.extract_location_from_query(query)
        
        # Check for weather queries
        if self.weather_service.is_weather_query(query):
            result["is_weather"] = True
            result["is_general"] = False
            result["extracted_info"]["location"] = self.weather_service.extract_location_from_query(query)
            result["extracted_info"]["time_period"] = self.weather_service.extract_time_period(query)
        
        # Check for translation requests
        translation_keywords = ["translate", "in kinyarwanda", "in english", "what does this mean"]
        if any(keyword in query_lower for keyword in translation_keywords):
            result["is_translation"] = True
            result["is_general"] = False
        
        return result
    
    def process_maps_query(self, query: str) -> str:
        """Process maps-related queries"""
        return self.maps_service.process_maps_query(query)
    
    def process_weather_query(self, query: str) -> str:
        """Process weather-related queries"""
        return self.weather_service.process_weather_query(query)
    
    def process_translation_query(self, query: str) -> str:
        """Process translation requests"""
        # Extract text to translate
        query_lower = query.lower()
        
        if "translate" in query_lower:
            # Extract text after "translate"
            parts = query_lower.split("translate")
            if len(parts) > 1:
                text_to_translate = parts[1].strip()
                if text_to_translate:
                    # Determine direction
                    if "kinyarwanda" in query_lower or "rwanda" in query_lower:
                        return self.translation_service.translate_en_to_rw(text_to_translate)
                    else:
                        return self.translation_service.translate_rw_to_en(text_to_translate)
        
        return "Please specify what you'd like to translate. For example: 'Translate hello to Kinyarwanda' or 'Translate Muraho to English'"
    
    def build_rag_chain(self):
        """Build the RAG chain with query optimization"""
        # Get retriever from vector store service
        retriever = self.vector_store_service.get_retriever()
        
        # Create prompt template
        prompt = self.create_prompt_template()
        
        # Build RAG chain
        self.rag_chain = (
            {"context": retriever, 
             "question": RunnablePassthrough() | RunnableLambda(self.expand_query),
             "additional_info": RunnablePassthrough() | RunnableLambda(lambda x: "")}
            | prompt
            | self.llm
            | StrOutputParser()
        )
    
    def query(self, text: str) -> str:
        """Process a query through the enhanced RAG system"""
        start_time = time.time()
        
        try:
            # Detect query type
            query_type = self.detect_query_type(text)
            
            # Process based on query type
            if query_type["is_maps"]:
                response = self.process_maps_query(text)
                logger.info(f"Maps query processed: {text[:50]}...")
                
            elif query_type["is_weather"]:
                response = self.process_weather_query(text)
                logger.info(f"Weather query processed: {text[:50]}...")
                
            elif query_type["is_translation"]:
                response = self.process_translation_query(text)
                logger.info(f"Translation query processed: {text[:50]}...")
                
            else:
                # Use regular RAG for general queries
                if not self.rag_chain:
                    raise RuntimeError("RAG chain not initialized")
                
                response = self.rag_chain.invoke(text)
                logger.info(f"General RAG query processed: {text[:50]}...")
            
            process_time = time.time() - start_time
            logger.info(f"Query processed in {process_time:.2f}s")
            
            return response
            
        except Exception as e:
            logger.error(f"Query processing error: {e}")
            return f"I'm sorry, I encountered an error processing your request: {str(e)}"
    
    def initialize(self):
        """Initialize the enhanced RAG service"""
        # Initialize services
        self.initialize_services()
        
        # Initialize LLM
        self.initialize_llm()
        
        # Build RAG chain
        self.build_rag_chain()
        
        logger.info("Enhanced RAG service initialized successfully") 