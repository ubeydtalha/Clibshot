"""
ClipShot Plugin SDK for Python

This SDK provides the base classes and utilities for developing ClipShot plugins.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Callable, List
from dataclasses import dataclass
from datetime import datetime
import asyncio
import logging


@dataclass
class PluginInfo:
    """Plugin metadata information."""
    id: str
    name: str
    version: str
    author: str
    description: str


@dataclass
class Clip:
    """Represents a captured clip."""
    id: str
    title: str
    game: Optional[str]
    duration: int
    width: int
    height: int
    fps: int
    file_path: str
    metadata: Dict[str, Any]
    created_at: datetime


@dataclass
class Game:
    """Represents a detected game."""
    id: str
    name: str
    process_name: str
    window_title: str
    detected_at: datetime


class PluginContext:
    """Context provided to plugins during initialization."""
    
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        self._config = config
        self._logger = logger
        self._apis: Dict[str, Any] = {}
    
    async def get_config(self) -> Dict[str, Any]:
        """Get plugin configuration."""
        return self._config
    
    def get_logger(self) -> logging.Logger:
        """Get plugin logger."""
        return self._logger
    
    async def get_api(self, api_class: type) -> Any:
        """Get a core API instance."""
        api_name = api_class.__name__
        if api_name not in self._apis:
            # In real implementation, this would fetch from the plugin manager
            raise NotImplementedError(f"API {api_name} not available")
        return self._apis[api_name]
    
    def register_api(self, api_class: type, instance: Any):
        """Register an API instance (internal use)."""
        self._apis[api_class.__name__] = instance


class Plugin(ABC):
    """
    Base class for all ClipShot plugins.
    
    Plugin developers should inherit from this class and implement
    the required lifecycle hooks.
    
    Example:
        ```python
        from clipshot_sdk import Plugin, Clip, PluginContext
        
        class MyPlugin(Plugin):
            id = "com.example.my-plugin"
            name = "My Plugin"
            version = "1.0.0"
            
            async def init(self, context: PluginContext):
                self.config = await context.get_config()
                self.logger = context.get_logger()
                self.logger.info("Plugin initialized!")
            
            async def on_clip_captured(self, clip: Clip):
                self.logger.info(f"Clip captured: {clip.id}")
        ```
    """
    
    # Plugin metadata (should be overridden)
    id: str = ""
    name: str = ""
    version: str = "1.0.0"
    
    def __init__(self):
        self.config: Optional[Dict[str, Any]] = None
        self.logger: Optional[logging.Logger] = None
        self._context: Optional[PluginContext] = None
    
    @abstractmethod
    async def init(self, context: PluginContext) -> None:
        """
        Initialize the plugin.
        
        Called when the plugin is loaded. Use this to:
        - Read configuration
        - Initialize resources
        - Setup state
        
        Args:
            context: Plugin context with config and APIs
        """
        pass
    
    async def shutdown(self) -> None:
        """
        Shutdown the plugin.
        
        Called when the plugin is being unloaded. Use this to:
        - Release resources
        - Save state
        - Clean up
        """
        pass
    
    async def on_clip_captured(self, clip: Clip) -> None:
        """
        Called when a clip is captured.
        
        Args:
            clip: The captured clip
        """
        pass
    
    async def on_game_detected(self, game: Game) -> None:
        """
        Called when a game is detected.
        
        Args:
            game: The detected game
        """
        pass
    
    async def on_config_changed(self, new_config: Dict[str, Any]) -> None:
        """
        Called when plugin configuration changes.
        
        Args:
            new_config: The new configuration
        """
        self.config = new_config


def api_route(path: str, methods: List[str] = None):
    """
    Decorator to register a custom API endpoint.
    
    Example:
        ```python
        @api_route("/my-endpoint", methods=["POST"])
        async def my_endpoint(self, request: dict) -> dict:
            return {"result": "success"}
        ```
    
    Args:
        path: The endpoint path
        methods: HTTP methods (default: ["GET"])
    """
    if methods is None:
        methods = ["GET"]
    
    def decorator(func: Callable):
        func._api_route = True
        func._api_path = path
        func._api_methods = methods
        return func
    
    return decorator


# Export all public APIs
__all__ = [
    "Plugin",
    "PluginInfo",
    "PluginContext",
    "Clip",
    "Game",
    "api_route",
]

__version__ = "1.0.0"
