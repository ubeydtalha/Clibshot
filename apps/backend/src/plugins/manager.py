"""
Plugin Manager for ClipShot Backend.

Manages plugin lifecycle:
- Discovery and loading
- Dependency resolution
- Hot reload support
- Plugin registry (in-memory + Redis cache)
"""

import asyncio
import json
import importlib.util
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from datetime import datetime

from src.config import settings
from src.core.logging import get_logger
from src.core.exceptions import (
    PluginError,
    PluginNotFoundError,
    PluginLoadError,
    PluginAlreadyLoadedError,
)
from src.schemas.plugin import (
    PluginManifest,
    PluginInfo,
    PluginStatus,
    PluginType,
    PluginCategory,
)

logger = get_logger(__name__)


class Plugin:
    """Plugin instance wrapper."""
    
    def __init__(self, manifest: PluginManifest, path: Path) -> None:
        self.manifest = manifest
        self.path = path
        self.module: Optional[Any] = None
        self.status = PluginStatus.INSTALLED
        self.enabled = False
        self.installed_at = datetime.now().isoformat()
        self.loaded_at: Optional[str] = None
        self.error: Optional[str] = None
    
    @property
    def id(self) -> str:
        """Get plugin ID."""
        return self.manifest.id
    
    async def init(self) -> None:
        """Initialize plugin."""
        if self.module and hasattr(self.module, "init"):
            try:
                if asyncio.iscoroutinefunction(self.module.init):
                    await self.module.init()
                else:
                    self.module.init()
                logger.info(f"Plugin {self.id} initialized")
            except Exception as e:
                logger.error(f"Error initializing plugin {self.id}: {e}")
                raise
    
    async def shutdown(self) -> None:
        """Shutdown plugin."""
        if self.module and hasattr(self.module, "shutdown"):
            try:
                if asyncio.iscoroutinefunction(self.module.shutdown):
                    await self.module.shutdown()
                else:
                    self.module.shutdown()
                logger.info(f"Plugin {self.id} shutdown")
            except Exception as e:
                logger.error(f"Error shutting down plugin {self.id}: {e}")


class PluginManager:
    """
    Plugin Manager for ClipShot.
    
    Responsibilities:
    - Plugin discovery and loading
    - Lifecycle management (init, shutdown)
    - Dependency resolution
    - Hot reload support
    - Plugin registry (in-memory)
    """
    
    def __init__(self, plugins_dir: Optional[Path] = None) -> None:
        """Initialize plugin manager."""
        self.plugins_dir = plugins_dir or Path(settings.PLUGINS_DIR)
        self._plugins: Dict[str, Plugin] = {}
        self._loaded: Set[str] = set()
        self._loading_lock = asyncio.Lock()
        logger.info(f"Plugin manager initialized with directory: {self.plugins_dir}")
    
    async def discover_and_load(self) -> None:
        """Discover and load all plugins in plugins directory."""
        logger.info("Starting plugin discovery...")
        
        if not self.plugins_dir.exists():
            logger.warning(f"Plugins directory does not exist: {self.plugins_dir}")
            self.plugins_dir.mkdir(parents=True, exist_ok=True)
            return
        
        # Discover plugins
        discovered = await self._discover_plugins()
        logger.info(f"Discovered {len(discovered)} plugins")
        
        # Load plugins with dependency resolution
        load_order = self._resolve_dependencies(discovered)
        
        for plugin_id in load_order:
            try:
                await self.load_plugin(plugin_id)
            except Exception as e:
                logger.error(f"Failed to load plugin {plugin_id}: {e}")
    
    async def _discover_plugins(self) -> Dict[str, Path]:
        """
        Discover all plugins in plugins directory.
        
        Returns:
            Dict mapping plugin_id to plugin path
        """
        discovered: Dict[str, Path] = {}
        
        # Check each subdirectory for manifest.json
        for plugin_dir in self.plugins_dir.iterdir():
            if not plugin_dir.is_dir():
                continue
            
            manifest_path = plugin_dir / "manifest.json"
            if not manifest_path.exists():
                logger.debug(f"No manifest found in {plugin_dir.name}")
                continue
            
            try:
                with open(manifest_path, "r", encoding="utf-8") as f:
                    manifest_data = json.load(f)
                
                manifest = PluginManifest(**manifest_data)
                discovered[manifest.id] = plugin_dir
                
                # Store in registry
                plugin = Plugin(manifest=manifest, path=plugin_dir)
                self._plugins[manifest.id] = plugin
                
                logger.debug(f"Discovered plugin: {manifest.id} ({manifest.name})")
                
            except Exception as e:
                logger.error(f"Error reading manifest from {plugin_dir.name}: {e}")
        
        return discovered
    
    def _resolve_dependencies(self, plugins: Dict[str, Path]) -> List[str]:
        """
        Resolve plugin dependencies and return load order.
        
        Args:
            plugins: Dict of plugin_id to path
        
        Returns:
            List of plugin IDs in load order
        """
        # Simple topological sort based on 'requires' field
        load_order: List[str] = []
        loaded: Set[str] = set()
        
        def visit(plugin_id: str) -> None:
            if plugin_id in loaded:
                return
            
            plugin = self._plugins.get(plugin_id)
            if not plugin:
                logger.warning(f"Plugin {plugin_id} not found during dependency resolution")
                return
            
            # Visit dependencies first
            for required_id in plugin.manifest.requires:
                # Extract plugin ID from API requirement (e.g., "core.events.api.v1" -> "core.events")
                dep_plugin_id = ".".join(required_id.split(".")[:2])
                if dep_plugin_id in plugins:
                    visit(dep_plugin_id)
            
            load_order.append(plugin_id)
            loaded.add(plugin_id)
        
        # Visit all plugins
        for plugin_id in plugins:
            visit(plugin_id)
        
        return load_order
    
    async def load_plugin(self, plugin_id: str) -> Plugin:
        """
        Load a plugin by ID.
        
        Args:
            plugin_id: Plugin identifier
        
        Returns:
            Loaded Plugin instance
        
        Raises:
            PluginNotFoundError: Plugin not found
            PluginLoadError: Failed to load plugin
            PluginAlreadyLoadedError: Plugin already loaded
        """
        async with self._loading_lock:
            # Check if plugin exists
            if plugin_id not in self._plugins:
                raise PluginNotFoundError(plugin_id)
            
            plugin = self._plugins[plugin_id]
            
            # Check if already loaded
            if plugin_id in self._loaded:
                raise PluginAlreadyLoadedError(plugin_id)
            
            try:
                logger.info(f"Loading plugin: {plugin_id}")
                
                # Get entry point
                entry_point = plugin.manifest.entry.get("backend")
                if not entry_point:
                    logger.warning(f"No backend entry point for plugin {plugin_id}")
                    plugin.status = PluginStatus.LOADED
                    plugin.enabled = True
                    plugin.loaded_at = datetime.now().isoformat()
                    self._loaded.add(plugin_id)
                    return plugin
                
                # Construct full path to entry point
                entry_path = plugin.path / entry_point
                if not entry_path.exists():
                    raise PluginLoadError(plugin_id, f"Entry point not found: {entry_point}")
                
                # Load Python module
                module_name = f"clipshot_plugin_{plugin_id.replace('.', '_')}"
                spec = importlib.util.spec_from_file_location(module_name, entry_path)
                
                if spec is None or spec.loader is None:
                    raise PluginLoadError(plugin_id, "Failed to create module spec")
                
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                
                plugin.module = module
                
                # Initialize plugin
                await plugin.init()
                
                # Update status
                plugin.status = PluginStatus.ACTIVE
                plugin.enabled = True
                plugin.loaded_at = datetime.now().isoformat()
                self._loaded.add(plugin_id)
                
                logger.info(f"Plugin {plugin_id} loaded successfully")
                return plugin
                
            except Exception as e:
                error_msg = str(e)
                logger.error(f"Failed to load plugin {plugin_id}: {error_msg}")
                plugin.status = PluginStatus.ERROR
                plugin.error = error_msg
                raise PluginLoadError(plugin_id, error_msg)
    
    async def unload_plugin(self, plugin_id: str) -> None:
        """
        Unload a plugin by ID.
        
        Args:
            plugin_id: Plugin identifier
        
        Raises:
            PluginNotFoundError: Plugin not found
        """
        async with self._loading_lock:
            if plugin_id not in self._plugins:
                raise PluginNotFoundError(plugin_id)
            
            plugin = self._plugins[plugin_id]
            
            if plugin_id not in self._loaded:
                logger.warning(f"Plugin {plugin_id} is not loaded")
                return
            
            try:
                logger.info(f"Unloading plugin: {plugin_id}")
                
                # Shutdown plugin
                await plugin.shutdown()
                
                # Remove from loaded set
                self._loaded.discard(plugin_id)
                
                # Update status
                plugin.status = PluginStatus.INSTALLED
                plugin.enabled = False
                plugin.module = None
                
                logger.info(f"Plugin {plugin_id} unloaded successfully")
                
            except Exception as e:
                logger.error(f"Error unloading plugin {plugin_id}: {e}")
                raise
    
    async def reload_plugin(self, plugin_id: str) -> Plugin:
        """
        Reload a plugin (unload and load again).
        
        Args:
            plugin_id: Plugin identifier
        
        Returns:
            Reloaded Plugin instance
        """
        if plugin_id in self._loaded:
            await self.unload_plugin(plugin_id)
        return await self.load_plugin(plugin_id)
    
    def get_plugin(self, plugin_id: str) -> Optional[Plugin]:
        """
        Get a plugin by ID.
        
        Args:
            plugin_id: Plugin identifier
        
        Returns:
            Plugin instance or None
        """
        return self._plugins.get(plugin_id)
    
    def list_plugins(
        self,
        type: Optional[PluginType] = None,
        category: Optional[PluginCategory] = None,
        enabled: Optional[bool] = None,
    ) -> List[Plugin]:
        """
        List all plugins with optional filters.
        
        Args:
            type: Filter by plugin type
            category: Filter by plugin category
            enabled: Filter by enabled status
        
        Returns:
            List of Plugin instances
        """
        plugins = list(self._plugins.values())
        
        if type is not None:
            plugins = [p for p in plugins if p.manifest.type == type]
        
        if category is not None:
            plugins = [p for p in plugins if p.manifest.category == category]
        
        if enabled is not None:
            plugins = [p for p in plugins if p.enabled == enabled]
        
        return plugins
    
    async def shutdown_all(self) -> None:
        """Shutdown all loaded plugins."""
        logger.info("Shutting down all plugins...")
        
        # Shutdown in reverse load order
        for plugin_id in reversed(list(self._loaded)):
            try:
                await self.unload_plugin(plugin_id)
            except Exception as e:
                logger.error(f"Error shutting down plugin {plugin_id}: {e}")
        
        logger.info("All plugins shut down")
