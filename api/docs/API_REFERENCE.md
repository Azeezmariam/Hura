# API Reference

## Overview

The Hura Tourism Chatbot API provides intelligent tourism assistance for visitors to Kigali, Rwanda. Built with FastAPI, it offers RAG-powered question answering and high-quality translation services.

**Base URL**: `https://lola9-hura-chatbot.hf.space`

## Authentication

Currently, no authentication is required. Rate limiting is applied at 60 requests per minute per IP address.

## Endpoints

### 1. Root Endpoint

**GET** `/`

Returns API information and available endpoints.

**Response:**

```json
{
  "message": "Welcome to Hura Tourism Chatbot API! (CPU Optimized)",
  "endpoints": {
    "ask_question": "POST /ask",
    "health_check": "GET /health",
    "translate_en2rw": "POST /translate/en2rw",
    "translate_rw2en": "POST /translate/rw2en"
  },
  "documentation": "/docs"
}
```

### 2. Health Check

**GET** `/health`

Returns system health status and model information.

**Response:**

```json
{
  "status": "healthy",
  "details": {
    "model_loaded": true,
    "persistent_storage": "/data",
    "storage_usage": "90.07 MB",
    "features": {
      "rag": true,
      "translation": true,
      "maps": false,
      "weather": false
    }
  }
}
```

### 3. Ask Questions

**POST** `/ask`

Ask tourism-related questions about Kigali and Rwanda.

**Request Body:**

```json
{
  "text": "Tell me about Kigali Genocide Memorial"
}
```

**Response:**

```json
{
  "response": "The Kigali Genocide Memorial is a memorial located in Kigali, Rwanda...",
  "processing_time": "38.66 seconds"
}
```

**Example Questions:**

- "Tell me about Kigali"
- "What are the best restaurants in Kigali?"
- "How safe is Kigali for tourists?"
- "What is the Kigali Genocide Memorial?"
- "Tell me about Rwandan culture"

### 4. English to Kinyarwanda Translation

**POST** `/translate/en2rw`

Translate English text to Kinyarwanda.

**Request Body:**

```json
{
  "text": "Hello, how are you?"
}
```

**Response:**

```json
{
  "translation": "Muraho, urumva umeze ute?"
}
```

### 5. Kinyarwanda to English Translation

**POST** `/translate/rw2en`

Translate Kinyarwanda text to English.

**Request Body:**

```json
{
  "text": "Muraho, amakuru?"
}
```

**Response:**

```json
{
  "translation": "Hey, news?"
}
```

## Data Models

### Query Model

```python
class Query(BaseModel):
    text: str
```

### Translation Request Model

```python
class TranslationRequest(BaseModel):
    text: str
```

### Query Response Model

```python
class QueryResponse(BaseModel):
    response: str
    processing_time: str
```

### Translation Response Model

```python
class TranslationResponse(BaseModel):
    translation: str
```

### Health Response Model

```python
class HealthResponse(BaseModel):
    status: str
    details: Dict
```

## Error Responses

### 400 Bad Request

```json
{
  "detail": "Invalid input data"
}
```

### 429 Too Many Requests

```json
{
  "detail": "Rate limit exceeded. Try again in 60 seconds."
}
```

### 500 Internal Server Error

```json
{
  "detail": "Error processing your request"
}
```

### 503 Service Unavailable

```json
{
  "detail": "Service initializing, try again in 30 seconds"
}
```

## Rate Limiting

- **Limit**: 60 requests per minute per IP
- **Headers**: Rate limit information is included in response headers
- **Exceeded**: Returns 429 status code with retry information

## Performance

### Response Times

- **Health Check**: < 1 second
- **Translation**: 5-15 seconds
- **Tourism Questions**: 30-60 seconds

### Factors Affecting Performance

- Model loading time (cold starts)
- Query complexity
- Server load
- Network latency

## Usage Examples

### cURL Examples

```bash
# Health check
curl -X GET "https://lola9-hura-chatbot.hf.space/health"

# Ask a question
curl -X POST "https://lola9-hura-chatbot.hf.space/ask" \
     -H "Content-Type: application/json" \
     -d '{"text": "Tell me about Kigali"}'

# Translate English to Kinyarwanda
curl -X POST "https://lola9-hura-chatbot.hf.space/translate/en2rw" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello, how are you?"}'

# Translate Kinyarwanda to English
curl -X POST "https://lola9-hura-chatbot.hf.space/translate/rw2en" \
     -H "Content-Type: application/json" \
     -d '{"text": "Muraho, amakuru?"}'
```

### Python Examples

```python
import requests

# Base URL
BASE_URL = "https://lola9-hura-chatbot.hf.space"

# Health check
response = requests.get(f"{BASE_URL}/health")
print(response.json())

# Ask a question
question_data = {"text": "Tell me about Kigali Genocide Memorial"}
response = requests.post(f"{BASE_URL}/ask", json=question_data)
print(response.json()["response"])

# Translate
translation_data = {"text": "Hello, how are you?"}
response = requests.post(f"{BASE_URL}/translate/en2rw", json=translation_data)
print(response.json()["translation"])
```

### JavaScript Examples

```javascript
const BASE_URL = "https://lola9-hura-chatbot.hf.space";

// Health check
fetch(`${BASE_URL}/health`)
  .then((response) => response.json())
  .then((data) => console.log(data));

// Ask a question
fetch(`${BASE_URL}/ask`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ text: "Tell me about Kigali" }),
})
  .then((response) => response.json())
  .then((data) => console.log(data.response));

// Translate
fetch(`${BASE_URL}/translate/en2rw`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ text: "Hello, how are you?" }),
})
  .then((response) => response.json())
  .then((data) => console.log(data.translation));
```

## Best Practices

1. **Handle Timeouts**: Set appropriate timeouts (60+ seconds for questions)
2. **Rate Limiting**: Implement exponential backoff for rate limit errors
3. **Error Handling**: Always check response status codes
4. **Caching**: Cache responses when appropriate
5. **User Feedback**: Show loading indicators for long-running requests

## Troubleshooting

### Common Issues

1. **Timeout Errors**: Increase timeout values for question endpoints
2. **Rate Limiting**: Implement retry logic with exponential backoff
3. **Model Loading**: Wait 30-60 seconds after deployment before testing
4. **Network Issues**: Check internet connectivity and firewall settings

### Debug Information

Enable debug logging by checking the `/health` endpoint for system status and model loading information.

## Support

- **Documentation**: Check this API reference
- **Issues**: Create an issue on GitHub
- **Live Demo**: [https://lola9-hura-chatbot.hf.space](https://lola9-hura-chatbot.hf.space)
