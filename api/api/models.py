from pydantic import BaseModel, validator
from typing import Optional

class Query(BaseModel):
    text: str
    
    @validator('text')
    def validate_text(cls, v):
        """Validate and sanitize query text"""
        if not v or len(v.strip()) == 0:
            raise ValueError('Query cannot be empty')
        if len(v) > 1000:
            raise ValueError('Query too long (max 1000 characters)')
        
        # Basic sanitization - remove potentially harmful characters
        sanitized = v.strip()
        # Remove any null bytes or control characters
        sanitized = ''.join(char for char in sanitized if ord(char) >= 32)
        
        return sanitized

class TranslationRequest(BaseModel):
    text: str
    
    @validator('text')
    def validate_text(cls, v):
        """Validate and sanitize translation text"""
        if not v or len(v.strip()) == 0:
            raise ValueError('Text cannot be empty')
        if len(v) > 2000:
            raise ValueError('Text too long (max 2000 characters)')
        
        # Basic sanitization
        sanitized = v.strip()
        sanitized = ''.join(char for char in sanitized if ord(char) >= 32)
        
        return sanitized

class MapsQuery(BaseModel):
    query: str
    
    @validator('query')
    def validate_query(cls, v):
        """Validate and sanitize maps query"""
        if not v or len(v.strip()) == 0:
            raise ValueError('Query cannot be empty')
        if len(v) > 500:
            raise ValueError('Query too long (max 500 characters)')
        
        # Basic sanitization
        sanitized = v.strip()
        sanitized = ''.join(char for char in sanitized if ord(char) >= 32)
        
        return sanitized

class WeatherQuery(BaseModel):
    query: str
    
    @validator('query')
    def validate_query(cls, v):
        """Validate and sanitize weather query"""
        if not v or len(v.strip()) == 0:
            raise ValueError('Query cannot be empty')
        if len(v) > 500:
            raise ValueError('Query too long (max 500 characters)')
        
        # Basic sanitization
        sanitized = v.strip()
        sanitized = ''.join(char for char in sanitized if ord(char) >= 32)
        
        return sanitized

class QueryResponse(BaseModel):
    response: str
    processing_time: str
    service_used: Optional[str] = None

class TranslationResponse(BaseModel):
    translation: str
    source_language: str
    target_language: str
    service_used: str

class HealthResponse(BaseModel):
    status: str
    details: dict

class RootResponse(BaseModel):
    message: str
    endpoints: dict
    documentation: str 