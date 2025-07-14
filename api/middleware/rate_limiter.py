import time
import logging
from collections import defaultdict, deque
from fastapi import Request, HTTPException
from typing import Dict, Deque

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, Deque[float]] = defaultdict(lambda: deque())
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if request is allowed based on rate limit"""
        now = time.time()
        client_requests = self.requests[client_id]
        
        # Remove requests older than 1 minute
        while client_requests and now - client_requests[0] > 60:
            client_requests.popleft()
        
        # Check if under limit
        if len(client_requests) < self.requests_per_minute:
            client_requests.append(now)
            return True
        
        return False
    
    def get_client_id(self, request: Request) -> str:
        """Get client identifier from request"""
        # Use X-Forwarded-For if available (for proxy setups)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        # Fall back to client host
        return request.client.host if request.client else "unknown"

def rate_limit_middleware(rate_limiter: RateLimiter):
    """FastAPI middleware for rate limiting"""
    async def middleware(request: Request, call_next):
        client_id = rate_limiter.get_client_id(request)
        
        if not rate_limiter.is_allowed(client_id):
            logger.warning(f"Rate limit exceeded for client: {client_id}")
            raise HTTPException(
                status_code=429, 
                detail="Too many requests. Please try again later."
            )
        
        response = await call_next(request)
        return response
    
    return middleware 