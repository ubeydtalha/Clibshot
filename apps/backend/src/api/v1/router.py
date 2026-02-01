"""
API v1 Main Router.

Includes all v1 route modules.
"""

from fastapi import APIRouter

from src.api.v1.routes import plugins, ai

api_router = APIRouter()

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
