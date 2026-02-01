"""
Plugin Manager - Core plugin management system
"""
import os
import sys
import importlib
import importlib.util
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Type
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class PluginStatus(Enum):
    """Plugin status enumeration"""
    LOADED = "loaded"
    UNLOADED = "unloaded"
    ERROR = "error"
    DISABLED = "disabled"


@dataclass
class PluginMetadata:
    """Plugin metadata structure"""
    name: str
    display_name: str
    version: str
    author: Optional[str] = None
    description: Optional[str] = None
    plugin_type: str = "python"
    dependencies: List[str] = None
    config_schema: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


class PluginBase:
    """Base class that all plugins must inherit from"""
    
    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.enabled: bool = True
    
    @property
    def metadata(self) -> PluginMetadata:
        """Return plugin metadata - must be implemented by plugin"""
        raise NotImplementedError("Plugin must implement metadata property")
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize plugin with configuration"""
        self.config = config
        logger.info(f"Plugin {self.metadata.name} initialized with config: {config}")
    
    def shutdown(self) -> None:
        """Cleanup when plugin is unloaded"""
        logger.info(f"Plugin {self.metadata.name} shutting down")
    
    def on_clip_captured(self, clip_data: Dict[str, Any]) -> Dict[str, Any]:
        """Called when a clip is captured"""
        return clip_data
    
    def on_clip_processed(self, clip_data: Dict[str, Any]) -> Dict[str, Any]:
        """Called when a clip is processed"""
        return clip_data


class PluginManager:
    """
    Plugin Manager - Handles plugin discovery, loading, and lifecycle
    """
    
    def __init__(self, plugin_dirs: Optional[List[str]] = None):
        """
        Initialize Plugin Manager
        
        Args:
            plugin_dirs: List of directories to search for plugins
        """
        self.plugins: Dict[str, PluginBase] = {}
        self.plugin_status: Dict[str, PluginStatus] = {}
        self.plugin_errors: Dict[str, str] = {}
        
        # Default plugin directories
        if plugin_dirs is None:
            plugin_dirs = [
                os.path.join(os.path.dirname(__file__), "plugins"),
                os.path.expanduser("~/.clipshot/plugins"),
            ]
        
        self.plugin_dirs = [Path(d) for d in plugin_dirs]
        
        # Create plugin directories if they don't exist
        for plugin_dir in self.plugin_dirs:
            plugin_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Plugin Manager initialized with directories: {self.plugin_dirs}")
    
    def discover_plugins(self) -> List[str]:
        """
        Discover available plugins in plugin directories
        
        Returns:
            List of discovered plugin names
        """
        discovered = []
        
        for plugin_dir in self.plugin_dirs:
            if not plugin_dir.exists():
                logger.warning(f"Plugin directory does not exist: {plugin_dir}")
                continue
            
            # Look for Python files or plugin directories
            for item in plugin_dir.iterdir():
                if item.is_file() and item.suffix == ".py" and item.stem != "__init__":
                    # Python file plugin
                    discovered.append(item.stem)
                    logger.debug(f"Discovered plugin file: {item}")
                
                elif item.is_dir() and (item / "__init__.py").exists():
                    # Python package plugin
                    discovered.append(item.name)
                    logger.debug(f"Discovered plugin package: {item}")
        
        logger.info(f"Discovered {len(discovered)} plugins: {discovered}")
        return discovered
    
    def load_plugin(self, plugin_name: str, config: Optional[Dict[str, Any]] = None) -> bool:
        """
        Load a plugin by name
        
        Args:
            plugin_name: Name of the plugin to load
            config: Optional configuration dictionary
        
        Returns:
            True if plugin loaded successfully, False otherwise
        """
        if plugin_name in self.plugins:
            logger.warning(f"Plugin {plugin_name} is already loaded")
            return True
        
        try:
            # Find plugin file
            plugin_path = self._find_plugin_path(plugin_name)
            if not plugin_path:
                raise FileNotFoundError(f"Plugin {plugin_name} not found in plugin directories")
            
            # Load the module
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            if spec is None or spec.loader is None:
                raise ImportError(f"Failed to create module spec for {plugin_name}")
            
            module = importlib.util.module_from_spec(spec)
            sys.modules[plugin_name] = module
            spec.loader.exec_module(module)
            
            # Find plugin class (must inherit from PluginBase)
            plugin_class = self._find_plugin_class(module)
            if not plugin_class:
                raise TypeError(f"No valid plugin class found in {plugin_name}")
            
            # Instantiate plugin
            plugin_instance = plugin_class()
            
            # Initialize with config
            if config is None:
                config = {}
            plugin_instance.initialize(config)
            
            # Store plugin
            self.plugins[plugin_name] = plugin_instance
            self.plugin_status[plugin_name] = PluginStatus.LOADED
            
            logger.info(f"Successfully loaded plugin: {plugin_name}")
            return True
        
        except Exception as e:
            error_msg = f"Failed to load plugin {plugin_name}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            self.plugin_status[plugin_name] = PluginStatus.ERROR
            self.plugin_errors[plugin_name] = str(e)
            return False
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """
        Unload a plugin
        
        Args:
            plugin_name: Name of the plugin to unload
        
        Returns:
            True if plugin unloaded successfully, False otherwise
        """
        if plugin_name not in self.plugins:
            logger.warning(f"Plugin {plugin_name} is not loaded")
            return False
        
        try:
            plugin = self.plugins[plugin_name]
            plugin.shutdown()
            
            del self.plugins[plugin_name]
            self.plugin_status[plugin_name] = PluginStatus.UNLOADED
            
            # Remove from sys.modules
            if plugin_name in sys.modules:
                del sys.modules[plugin_name]
            
            logger.info(f"Successfully unloaded plugin: {plugin_name}")
            return True
        
        except Exception as e:
            error_msg = f"Failed to unload plugin {plugin_name}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            self.plugin_errors[plugin_name] = str(e)
            return False
    
    def reload_plugin(self, plugin_name: str, config: Optional[Dict[str, Any]] = None) -> bool:
        """
        Reload a plugin (unload then load)
        
        Args:
            plugin_name: Name of the plugin to reload
            config: Optional configuration dictionary
        
        Returns:
            True if plugin reloaded successfully, False otherwise
        """
        if plugin_name in self.plugins:
            self.unload_plugin(plugin_name)
        
        return self.load_plugin(plugin_name, config)
    
    def get_plugin(self, plugin_name: str) -> Optional[PluginBase]:
        """Get a loaded plugin instance"""
        return self.plugins.get(plugin_name)
    
    def get_all_plugins(self) -> Dict[str, PluginBase]:
        """Get all loaded plugins"""
        return self.plugins.copy()
    
    def get_plugin_status(self, plugin_name: str) -> Optional[PluginStatus]:
        """Get plugin status"""
        return self.plugin_status.get(plugin_name)
    
    def get_plugin_error(self, plugin_name: str) -> Optional[str]:
        """Get plugin error message if any"""
        return self.plugin_errors.get(plugin_name)
    
    def trigger_event(self, event_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Trigger an event on all loaded plugins
        
        Args:
            event_name: Name of the event (e.g., 'on_clip_captured')
            data: Event data
        
        Returns:
            Modified data after all plugins processed it
        """
        result_data = data.copy()
        
        for plugin_name, plugin in self.plugins.items():
            if not plugin.enabled:
                continue
            
            try:
                handler = getattr(plugin, event_name, None)
                if handler and callable(handler):
                    result_data = handler(result_data) or result_data
                    logger.debug(f"Plugin {plugin_name} handled event {event_name}")
            
            except Exception as e:
                logger.error(f"Plugin {plugin_name} failed to handle event {event_name}: {str(e)}", exc_info=True)
        
        return result_data
    
    def _find_plugin_path(self, plugin_name: str) -> Optional[Path]:
        """Find the path to a plugin file"""
        for plugin_dir in self.plugin_dirs:
            # Check for Python file
            file_path = plugin_dir / f"{plugin_name}.py"
            if file_path.exists():
                return file_path
            
            # Check for package
            package_path = plugin_dir / plugin_name / "__init__.py"
            if package_path.exists():
                return package_path
        
        return None
    
    def _find_plugin_class(self, module) -> Optional[Type[PluginBase]]:
        """Find a plugin class in a module"""
        for item_name in dir(module):
            item = getattr(module, item_name)
            
            # Check if it's a class and inherits from PluginBase
            if (isinstance(item, type) and 
                issubclass(item, PluginBase) and 
                item is not PluginBase):
                return item
        
        return None


# Global plugin manager instance
plugin_manager: Optional[PluginManager] = None


def get_plugin_manager() -> PluginManager:
    """Get the global plugin manager instance"""
    global plugin_manager
    
    if plugin_manager is None:
        plugin_manager = PluginManager()
    
    return plugin_manager
