"""
API v1 Main Router.

Includes all v1 route modules.
"""

from datetime import datetime
from fastapi import APIRouter

from src.api.v1.routes import plugins, ai

api_router = APIRouter()

# Health check endpoint
@api_router.get("/v1/health", tags=["System"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "version": "0.1.0",
        "service": "clipshot-backend",
        "timestamp": datetime.utcnow().isoformat()
    }

# Plugin routes
api_router.include_router(
    plugins.router,
    prefix="/v1/plugins",
    tags=["Plugins"],
)

# AI routes
api_router.include_router(
    ai.router,
    prefix="/v1/ai",
    tags=["AI Runtime"],
)
