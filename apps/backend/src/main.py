"""
ClipShot Backend — FastAPI Application

Main entry point for the FastAPI application with:
- CORS middleware for Tauri frontend
- API versioning (/api/v1)
- Health check endpoint
- Error handling middleware
- Logging configuration
- Plugin manager lifecycle
"""

from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

from src.config import settings
from src.core.logging import setup_logging, get_logger
from src.core.events import EventBus
from src.core.exceptions import ClipShotError
from src.plugins.manager import PluginManager

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:
    """Application lifespan manager for startup and shutdown tasks."""
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.VERSION}")
    
    # Initialize event bus
    event_bus = EventBus()
    app.state.event_bus = event_bus
    
    # TODO: Initialize database
    # await init_db()
    
    # Load plugins
    plugin_manager = PluginManager()
    await plugin_manager.discover_and_load()
    app.state.plugin_manager = plugin_manager
    
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")
    
    # Shutdown plugins
    await plugin_manager.shutdown_all()
    
    # Close event bus
    await event_bus.close()
    
    logger.info("Application shutdown complete")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    
    # Setup logging first
    setup_logging()
    
    app = FastAPI(
        title=settings.APP_NAME,
        description="""
## 🎮 ClipShot Backend API

Modüler gaming AI platformu için RESTful API.

### Özellikler
- 📹 Ekran/Oyun kaydı
- 🤖 AI highlight tespiti ve metadata üretimi
- 🧩 Plugin sistemi
- 🏪 Marketplace

### Dokümantasyon
- [Swagger UI](/docs)
- [ReDoc](/redoc)
- [OpenAPI JSON](/openapi.json)
        """,
        version=settings.VERSION,
        openapi_url="/openapi.json",
        docs_url=None,  # Custom docs endpoint
        redoc_url=None,  # Custom redoc endpoint
        lifespan=lifespan,
        debug=settings.DEBUG,
    )
    
    # CORS middleware for Tauri frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Exception handlers
    @app.exception_handler(ClipShotError)
    async def clipshot_exception_handler(request: Request, exc: ClipShotError) -> JSONResponse:
        """Handle ClipShot custom exceptions."""
        logger.error(f"ClipShot error: {exc.code} - {exc.message}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": exc.code,
                "message": exc.message,
            },
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Handle unexpected exceptions."""
        logger.exception(f"Unexpected error: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
            },
        )
    
    # Health check endpoint
    @app.get("/health", tags=["System"])
    async def health_check() -> Dict[str, Any]:
        """
        Health check endpoint.
        
        Returns application health status including:
        - Application version
        - API status
        - Plugin manager status (when implemented)
        - Database status (when implemented)
        """
        return {
            "status": "healthy",
            "version": settings.VERSION,
            "app_name": settings.APP_NAME,
        }
    
    # Root endpoint
    @app.get("/", tags=["System"])
    async def root() -> Dict[str, str]:
        """Root endpoint with API information."""
        return {
            "app": settings.APP_NAME,
            "version": settings.VERSION,
            "docs": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json",
        }
    
    # Custom documentation endpoints
    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui() -> Any:
        """Custom Swagger UI endpoint."""
        return get_swagger_ui_html(
            openapi_url="/openapi.json",
            title=f"{settings.APP_NAME} - API Docs",
        )
    
    @app.get("/redoc", include_in_schema=False)
    async def custom_redoc() -> Any:
        """Custom ReDoc endpoint."""
        return get_redoc_html(
            openapi_url="/openapi.json",
            title=f"{settings.APP_NAME} - ReDoc",
        )
    
    # TODO: Include API routers
    from src.api.v1.router import api_router
    app.include_router(api_router, prefix="/api")
    
    return app


# Application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
