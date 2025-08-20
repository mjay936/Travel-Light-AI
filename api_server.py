import threading
import time
import logging
import hashlib
import json
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager
import asyncio

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import StreamingResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn

from travel_graph import build_conversation_graph

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global state for conversation graph
_conversation_graph: Optional[Any] = None
_graph_initialized = False

# Response cache for frequently requested queries
_response_cache: Dict[str, Dict[str, Any]] = {}
_cache_ttl = 300  # 5 minutes

# Request deduplication
_pending_requests: Dict[str, Any] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting Travel Light API Server...")
    logger.info("📍 Server will be available at: http://127.0.0.1:8787")
    logger.info("📚 API docs available at: http://127.0.0.1:8787/docs")
    
    # Initialize conversation graph
    global _conversation_graph, _graph_initialized
    try:
        logger.info("🔄 Initializing conversation graph...")
        start_time = time.time()
        _conversation_graph = build_conversation_graph()
        init_time = time.time() - start_time
        logger.info(f"✅ Conversation graph initialized in {init_time:.2f}s")
        _graph_initialized = True
    except Exception as e:
        logger.error(f"❌ Failed to initialize conversation graph: {e}")
        _graph_initialized = False
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Travel Light API Server...")

app = FastAPI(
    title="Travel Light API",
    description="AI-powered travel planning and exploration API",
    version="1.0.0",
    lifespan=lifespan
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Rate limiting (simple in-memory implementation)
_request_counts: Dict[str, List[float]] = {}
_RATE_LIMIT = 100  # requests per minute
_RATE_WINDOW = 60  # seconds

def _check_rate_limit(client_ip: str) -> bool:
    """Simple rate limiting implementation"""
    now = time.time()
    if client_ip not in _request_counts:
        _request_counts[client_ip] = []
    
    # Remove old requests outside the window
    _request_counts[client_ip] = [
        req_time for req_time in _request_counts[client_ip] 
        if now - req_time < _RATE_WINDOW
    ]
    
    # Check if under limit
    if len(_request_counts[client_ip]) >= _RATE_LIMIT:
        return False
    
    # Add current request
    _request_counts[client_ip].append(now)
    return True

def _get_client_ip(request: Request) -> str:
    """Extract client IP from request"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"

def _get_cache_key(messages: List[Dict[str, Any]]) -> str:
    """Generate cache key for messages"""
    # Create a hash of the messages for caching
    message_str = json.dumps(messages, sort_keys=True)
    return hashlib.md5(message_str.encode()).hexdigest()

def _get_cached_response(cache_key: str) -> Optional[Dict[str, Any]]:
    """Get cached response if available and not expired"""
    if cache_key in _response_cache:
        cached = _response_cache[cache_key]
        if time.time() - cached['timestamp'] < _cache_ttl:
            return cached['data']
        else:
            # Remove expired cache entry
            del _response_cache[cache_key]
    return None

def _set_cached_response(cache_key: str, data: Dict[str, Any]):
    """Cache response data with timestamp"""
    _response_cache[cache_key] = {
        'data': data,
        'timestamp': time.time()
    }

def _chunk_text(text: str, size: int = 40):
    """Efficient text chunking"""
    for i in range(0, len(text), size):
        yield text[i : i + size]

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "graph_initialized": _graph_initialized,
        "version": "1.0.0",
        "cache_stats": {
            "cache_size": len(_response_cache),
            "pending_requests": len(_pending_requests)
        }
    }

@app.post("/api/chat")
async def api_chat(request: Request):
    """Main chat endpoint with rate limiting, caching, and error handling"""
    # Rate limiting
    client_ip = _get_client_ip(request)
    if not _check_rate_limit(client_ip):
        logger.warning(f"Rate limit exceeded for {client_ip}")
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    # Check if graph is initialized
    if not _graph_initialized or _conversation_graph is None:
        logger.error("Conversation graph not initialized")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")
    
    try:
        # Parse request
        payload = await request.json()
        messages: List[Dict[str, Any]] = payload.get("messages", [])
        
        if not messages:
            raise HTTPException(status_code=400, detail="No messages provided")
        
        # Check cache first
        cache_key = _get_cache_key(messages)
        cached_response = _get_cached_response(cache_key)
        if cached_response:
            logger.info(f"Cache hit for {client_ip}")
            return StreamingResponse(
                _stream_cached_response(cached_response),
                media_type="text/plain",
                headers={"X-Cache": "HIT", "X-Processing-Time": "0.00"}
            )
        
        # Check if request is already being processed
        if cache_key in _pending_requests:
            logger.info(f"Request deduplication for {client_ip}")
            # Wait for the pending request to complete
            while cache_key in _pending_requests:
                await asyncio.sleep(0.1)
            
            # Check cache again after waiting
            cached_response = _get_cached_response(cache_key)
            if cached_response:
                return StreamingResponse(
                    _stream_cached_response(cached_response),
                    media_type="text/plain",
                    headers={"X-Cache": "HIT", "X-Processing-Time": "0.00"}
                )
        
        # Mark request as pending
        _pending_requests[cache_key] = True
        
        try:
            # Build and invoke the conversation graph
            start_time = time.time()
            graph_state = {"messages": messages}
            result = _conversation_graph.invoke(graph_state)
            processing_time = time.time() - start_time
            
            logger.info(f"Chat processed in {processing_time:.2f}s for {client_ip}")
            
            bot_messages = result.get("messages", [])

            # Get the last assistant message content
            assistant_text = ""
            if bot_messages:
                latest = bot_messages[-1]
                if hasattr(latest, "content"):
                    assistant_text = latest.content or ""
                elif isinstance(latest, dict):
                    assistant_text = latest.get("content", "") or ""
                else:
                    assistant_text = str(latest)

            # Cache the response
            _set_cached_response(cache_key, {"content": assistant_text, "processing_time": processing_time})

            def streamer():
                """Stream response with proper error handling"""
                try:
                    # Stream NDJSON-like lines prefixed with "data: "
                    for chunk in _chunk_text(assistant_text, size=40):
                        yield f"data: {{\"delta\": {chunk!r}, \"done\": false}}\n"
                    yield "data: {\"done\": true}\n"
                except Exception as e:
                    logger.error(f"Error in streaming: {e}")
                    yield f"data: {{\"error\": \"Streaming error\", \"done\": true}}\n"

            return StreamingResponse(
                streamer(), 
                media_type="text/plain",
                headers={
                    "Cache-Control": "public, max-age=300",
                    "X-Processing-Time": str(processing_time),
                    "X-Cache": "MISS"
                }
            )
            
        finally:
            # Remove from pending requests
            if cache_key in _pending_requests:
                del _pending_requests[cache_key]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

def _stream_cached_response(cached_data: Dict[str, Any]):
    """Stream cached response data"""
    content = cached_data.get("content", "")
    for chunk in _chunk_text(content, size=40):
        yield f"data: {{\"delta\": {chunk!r}, \"done\": false}}\n"
    yield "data: {\"done\": true}\n"

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return {"error": "Internal server error", "detail": str(exc)}

# Cache management endpoints
@app.post("/api/cache/clear")
async def clear_cache():
    """Clear response cache"""
    global _response_cache
    _response_cache.clear()
    return {"message": "Cache cleared", "timestamp": time.time()}

@app.get("/api/cache/stats")
async def get_cache_stats():
    """Get cache statistics"""
    return {
        "cache_size": len(_response_cache),
        "pending_requests": len(_pending_requests),
        "cache_ttl": _cache_ttl,
        "timestamp": time.time()
    }

def start_server_in_thread(host: str = "127.0.0.1", port: int = 8787):
    """Start server in background thread"""
    global _server_started
    if _server_started:
        return
    _server_started = True

    def run():
        try:
            uvicorn.run(
                app, 
                host=host, 
                port=port, 
                log_level="warning",
                access_log=False  # Disable access logs for performance
            )
        except Exception as e:
            logger.error(f"Server error: {e}")

    t = threading.Thread(target=run, daemon=True)
    t.start()
    logger.info(f"🚀 Server started in background thread on {host}:{port}")

if __name__ == "__main__":
    print("🚀 Starting Travel Light API Server...")
    print("📍 Server will be available at: http://127.0.0.1:8787")
    print("📚 API docs available at: http://127.0.0.1:8787/docs")
    print("💡 Press Ctrl+C to stop the server")
    
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8787, 
        log_level="info",
        access_log=True
    )


