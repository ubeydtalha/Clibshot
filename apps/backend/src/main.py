from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import sys
import traceback
from datetime import datetime
import os

# Configure logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/clipshot.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

# Import database and create tables
from .database import engine, Base
from .models import Plugin, PluginConfiguration, Clip

# Import routers
from .routes import plugins, clips

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("ClipShot Backend starting...")
    logger.info(f"Environment: {'production' if not app.debug else 'development'}")
    logger.info(f"CORS origins configured: {app.middleware}")
    
    # Create database tables
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
    
    # Initialize plugin manager
    from .plugin_manager import get_plugin_manager
    pm = get_plugin_manager()
    logger.info("Plugin manager initialized")
    
    yield
    # Shutdown
    logger.info("ClipShot Backend shutting down...")
    logger.info("Cleaning up resources...")

app = FastAPI(
    title="ClipShot API",
    description="Modular Gaming Clip Platform Backend",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    logger.info(f"-> {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        duration = (datetime.now() - start_time).total_seconds() * 1000
        logger.info(f"<- {request.method} {request.url.path} - {response.status_code} ({duration:.2f}ms)")
        return response
    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds() * 1000
        logger.error(f"ERROR {request.method} {request.url.path} - ({duration:.2f}ms): {str(e)}")
        logger.error(traceback.format_exc())
        raise

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception handler caught: {type(exc).__name__}")
    logger.error(f"Request: {request.method} {request.url}")
    logger.error(f"Exception: {str(exc)}")
    logger.error(traceback.format_exc())
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "type": type(exc).__name__,
            "timestamp": datetime.now().isoformat()
        }
    )

# CORS middleware for Tauri
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "tauri://localhost",
        "http://localhost:5173",
        "http://localhost:1420",  # Tauri dev server alternate port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(plugins.router, prefix="/api/v1")
app.include_router(clips.router, prefix="/api/v1")

# Health check
@app.get("/api/v1/health")
async def health_check():
    logger.debug("Health check requested")
    return {
        "status": "ok",
        "service": "clipshot-backend",
        "version": "0.1.0",
        "timestamp": datetime.now().isoformat()
    }

# Root
@app.get("/")
async def root():
    return {
        "message": "ClipShot Backend API",
        "docs": "/api/docs",
        "health": "/api/v1/health"
    }

# AI endpoint (placeholder)
@app.get("/api/v1/ai/models")
async def list_ai_models():
    return {
        "models": [],
        "count": 0,
        "message": "AI runtime coming soon!"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
