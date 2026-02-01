"""
Hello World Plugin - Python Example

This is a simple example plugin that demonstrates how to use the ClipShot Python SDK.
"""

from clipshot_sdk import Plugin, PluginContext, Clip, Game, api_route
from typing import Dict, Any
import json
from pathlib import Path


class HelloWorldPlugin(Plugin):
    """
    A simple example plugin that logs messages when events occur.
    
    This plugin demonstrates:
    - Basic plugin structure
    - Lifecycle hooks (init, shutdown)
    - Event hooks (on_clip_captured, on_game_detected)
    - Custom API endpoints
    - Configuration management
    """
    
    id = "com.clipshot.hello-world-py"
    name = "Hello World Python"
    version = "1.0.0"
    
    def __init__(self):
        super().__init__()
        self.clip_count = 0
        self.game_count = 0
        self.state_file: Path = None
    
    async def init(self, context: PluginContext) -> None:
        """
        Initialize the plugin.
        
        Load configuration and setup resources.
        """
        self.config = await context.get_config()
        self.logger = context.get_logger()
        self._context = context
        
        # Get message from config
        message = self.config.get("message", "Hello from ClipShot!")
        log_level = self.config.get("logLevel", "info")
        
        self.logger.info(f"🎮 {message}")
        self.logger.info(f"📝 Log level: {log_level}")
        self.logger.info("✅ Hello World plugin initialized successfully!")
        
        # Load state
        await self._load_state()
    
    async def shutdown(self) -> None:
        """
        Shutdown the plugin.
        
        Save state and clean up resources.
        """
        self.logger.info("💾 Saving plugin state...")
        await self._save_state()
        
        self.logger.info(f"📊 Total clips captured: {self.clip_count}")
        self.logger.info(f"🎮 Total games detected: {self.game_count}")
        self.logger.info("👋 Hello World plugin shutting down. Goodbye!")
    
    async def on_clip_captured(self, clip: Clip) -> None:
        """
        Called when a clip is captured.
        
        Args:
            clip: The captured clip
        """
        self.clip_count += 1
        
        self.logger.info(f"🎬 Clip captured: {clip.title}")
        self.logger.info(f"   ID: {clip.id}")
        self.logger.info(f"   Game: {clip.game or 'Unknown'}")
        self.logger.info(f"   Duration: {clip.duration}s")
        self.logger.info(f"   Resolution: {clip.width}x{clip.height} @ {clip.fps}fps")
        self.logger.info(f"   Total clips so far: {self.clip_count}")
    
    async def on_game_detected(self, game: Game) -> None:
        """
        Called when a game is detected.
        
        Args:
            game: The detected game
        """
        self.game_count += 1
        
        self.logger.info(f"🎮 Game detected: {game.name}")
        self.logger.info(f"   ID: {game.id}")
        self.logger.info(f"   Process: {game.process_name}")
        self.logger.info(f"   Window: {game.window_title}")
        self.logger.info(f"   Total games detected: {self.game_count}")
    
    async def on_config_changed(self, new_config: Dict[str, Any]) -> None:
        """
        Called when plugin configuration changes.
        
        Args:
            new_config: The new configuration
        """
        await super().on_config_changed(new_config)
        
        self.logger.info("⚙️  Configuration updated!")
        self.logger.info(f"   New message: {new_config.get('message', 'N/A')}")
        self.logger.info(f"   New log level: {new_config.get('logLevel', 'N/A')}")
    
    @api_route("/status", methods=["GET"])
    async def get_status(self) -> Dict[str, Any]:
        """
        Get plugin status.
        
        Returns:
            Dictionary with plugin status information
        """
        return {
            "status": "healthy",
            "version": self.version,
            "clip_count": self.clip_count,
            "game_count": self.game_count,
            "config": {
                "enabled": self.config.get("enabled", True),
                "message": self.config.get("message", "N/A"),
                "logLevel": self.config.get("logLevel", "info"),
            }
        }
    
    @api_route("/stats", methods=["GET"])
    async def get_stats(self) -> Dict[str, Any]:
        """
        Get plugin statistics.
        
        Returns:
            Dictionary with plugin statistics
        """
        return {
            "clips_captured": self.clip_count,
            "games_detected": self.game_count,
        }
    
    @api_route("/reset", methods=["POST"])
    async def reset_counters(self) -> Dict[str, Any]:
        """
        Reset all counters.
        
        Returns:
            Success message
        """
        old_clip_count = self.clip_count
        old_game_count = self.game_count
        
        self.clip_count = 0
        self.game_count = 0
        
        self.logger.info("🔄 Counters reset!")
        
        return {
            "success": True,
            "message": "Counters reset successfully",
            "previous": {
                "clip_count": old_clip_count,
                "game_count": old_game_count,
            }
        }
    
    async def _load_state(self) -> None:
        """Load plugin state from disk."""
        # In a real implementation, this would use context.get_plugin_data_path()
        # For now, we'll skip actual file I/O
        self.logger.debug("📂 State loading skipped (demo mode)")
    
    async def _save_state(self) -> None:
        """Save plugin state to disk."""
        state = {
            "clip_count": self.clip_count,
            "game_count": self.game_count,
        }
        # In a real implementation, this would save to disk
        self.logger.debug(f"💾 State saving skipped (demo mode): {state}")


# Export the plugin class
__plugin__ = HelloWorldPlugin
