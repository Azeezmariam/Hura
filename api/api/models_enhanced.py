from pydantic import BaseModel
from typing import Dict, List, Optional

# ===== Base Models =====
class Query(BaseModel):
    text: str

class TranslationRequest(BaseModel):
    text: str

class MapsQuery(BaseModel):
    query: str

class WeatherQuery(BaseModel):
    query: str

# ===== Response Models =====
class QueryResponse(BaseModel):
    response: str
    processing_time: str
    service_used: str

class TranslationResponse(BaseModel):
    translation: str
    source_language: str
    target_language: str
    service_used: str

class HealthResponse(BaseModel):
    status: str
    details: Dict

class RootResponse(BaseModel):
    message: str
    endpoints: Dict[str, str]
    documentation: str

# ===== Menu Models =====
class MenuOption(BaseModel):
    id: str
    title: str
    description: str
    endpoint: str
    method: str
    example: Dict

class MenuResponse(BaseModel):
    title: str
    description: str
    options: List[MenuOption]
    features_status: Dict[str, bool] 