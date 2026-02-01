"""
Example Plugin: Highlight Detector
This plugin demonstrates how to create a ClipShot plugin
"""
from ..plugin_manager import PluginBase, PluginMetadata
import logging

logger = logging.getLogger(__name__)


class HighlightDetectorPlugin(PluginBase):
    """
    Example plugin that analyzes clips for highlights
    This is a demonstration plugin showing the plugin structure
    """
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="highlight_detector",
            display_name="Highlight Detector",
            version="0.1.0",
            author="ClipShot Team",
            description="Detects potential highlights in gaming clips using AI analysis",
            plugin_type="python",
            dependencies=["opencv-python", "numpy"],
            config_schema={
                "sensitivity": {
                    "type": "float",
                    "default": 0.7,
                    "min": 0.0,
                    "max": 1.0,
                    "description": "Detection sensitivity (0.0 - 1.0)"
                },
                "min_duration": {
                    "type": "int",
                    "default": 5,
                    "min": 1,
                    "description": "Minimum highlight duration in seconds"
                }
            }
        )
    
    def initialize(self, config):
        """Initialize the plugin with configuration"""
        super().initialize(config)
        
        self.sensitivity = config.get("sensitivity", 0.7)
        self.min_duration = config.get("min_duration", 5)
        
        logger.info(f"HighlightDetector initialized: sensitivity={self.sensitivity}, min_duration={self.min_duration}")
    
    def on_clip_captured(self, clip_data):
        """
        Called when a clip is captured
        Analyzes the clip for potential highlights
        """
        logger.info(f"Analyzing clip for highlights: {clip_data.get('title', 'Untitled')}")
        
        # In a real implementation, this would:
        # 1. Load the video file
        # 2. Analyze frames for action/excitement
        # 3. Detect potential highlight moments
        # 4. Return timestamps and scores
        
        # For demonstration, we'll add fake highlight data
        if "metadata" not in clip_data:
            clip_data["metadata"] = {}
        
        clip_data["metadata"]["highlights"] = [
            {
                "timestamp": 15.5,
                "duration": 8.2,
                "score": 0.85,
                "type": "action"
            },
            {
                "timestamp": 45.3,
                "duration": 6.1,
                "score": 0.72,
                "type": "clutch"
            }
        ]
        
        clip_data["metadata"]["highlight_count"] = 2
        clip_data["metadata"]["analyzed_by"] = "highlight_detector"
        
        logger.info(f"Found {len(clip_data['metadata']['highlights'])} potential highlights")
        
        return clip_data
    
    def on_clip_processed(self, clip_data):
        """
        Called when a clip is processed
        Marks the clip analysis as complete
        """
        logger.info(f"Clip processing complete: {clip_data.get('title', 'Untitled')}")
        
        if "metadata" not in clip_data:
            clip_data["metadata"] = {}
        
        clip_data["metadata"]["highlight_detection_complete"] = True
        
        return clip_data
    
    def shutdown(self):
        """Cleanup when plugin is unloaded"""
        logger.info("HighlightDetector shutting down")
        super().shutdown()
