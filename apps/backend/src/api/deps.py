"""API dependencies for dependency injection."""

from typing import Generator
from fastapi import Request

from src.plugins.manager import PluginManager
from src.core.events import EventBus


def get_plugin_manager(request: Request) -> PluginManager:
    """Get plugin manager from app state."""
    return request.app.state.plugin_manager


def get_event_bus(request: Request) -> EventBus:
    """Get event bus from app state."""
    return request.app.state.event_bus
