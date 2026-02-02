"""
My Plugin for ClipShot

Replace this with your plugin description.
"""

from clipshot_sdk import Plugin, PluginContext, Clip, Game, api_route
from typing import Dict, Any


class MyPlugin(Plugin):
    """
    Your plugin implementation.
    
    Customize this class to add your plugin functionality.
    """
    
    id = "com.example.my-plugin"  # CHANGE THIS
    name = "My Plugin"             # CHANGE THIS
    version = "1.0.0"
    
    async def init(self, context: PluginContext) -> None:
        """
        Initialize your plugin.
        
        This is called when the plugin is loaded.
        """
        self.config = await context.get_config()
        self.logger = context.get_logger()
        self._context = context
        
        self.logger.info(f"{self.name} v{self.version} initialized!")
        
        # TODO: Initialize your plugin resources here
    
    async def shutdown(self) -> None:
        """
        Shutdown your plugin.
        
        Clean up resources here.
        """
        self.logger.info(f"{self.name} shutting down")
        
        # TODO: Clean up your plugin resources here
    
    async def on_clip_captured(self, clip: Clip) -> None:
        """
        Called when a clip is captured.
        
        Args:
            clip: The captured clip data
        """
        self.logger.info(f"Clip captured: {clip.title}")
        
        # TODO: Add your clip processing logic here
    
    async def on_game_detected(self, game: Game) -> None:
        """
        Called when a game is detected.
        
        Args:
            game: The detected game data
        """
        self.logger.info(f"Game detected: {game.name}")
        
        # TODO: Add your game detection logic here
    
    @api_route("/status", methods=["GET"])
    async def get_status(self) -> Dict[str, Any]:
        """
        Example custom API endpoint.
        
        Returns plugin status information.
        """
        return {
            "status": "healthy",
            "version": self.version,
            "enabled": self.config.get("enabled", True),
        }
    
    # TODO: Add more custom API endpoints as needed


# Export the plugin class
__plugin__ = MyPlugin
