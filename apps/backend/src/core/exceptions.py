"""Custom exceptions for ClipShot Backend."""


class ClipShotError(Exception):
    """Base exception for ClipShot."""
    
    def __init__(self, message: str, code: str = "CLIPSHOT_ERROR") -> None:
        self.message = message
        self.code = code
        super().__init__(self.message)


class PluginError(ClipShotError):
    """Plugin-related errors."""
    
    def __init__(self, message: str) -> None:
        super().__init__(message, code="PLUGIN_ERROR")


class PluginNotFoundError(PluginError):
    """Plugin not found."""
    
    def __init__(self, plugin_id: str) -> None:
        super().__init__(f"Plugin not found: {plugin_id}")


class PluginLoadError(PluginError):
    """Plugin failed to load."""
    
    def __init__(self, plugin_id: str, reason: str) -> None:
        super().__init__(f"Failed to load plugin {plugin_id}: {reason}")


class PluginAlreadyLoadedError(PluginError):
    """Plugin is already loaded."""
    
    def __init__(self, plugin_id: str) -> None:
        super().__init__(f"Plugin already loaded: {plugin_id}")


class AIRuntimeError(ClipShotError):
    """AI runtime errors."""
    
    def __init__(self, message: str) -> None:
        super().__init__(message, code="AI_RUNTIME_ERROR")


class ModelNotFoundError(AIRuntimeError):
    """AI model not found."""
    
    def __init__(self, model_id: str) -> None:
        super().__init__(f"Model not found: {model_id}")


class InferenceError(AIRuntimeError):
    """Inference failed."""
    
    def __init__(self, reason: str) -> None:
        super().__init__(f"Inference failed: {reason}")


class DatabaseError(ClipShotError):
    """Database errors."""
    
    def __init__(self, message: str) -> None:
        super().__init__(message, code="DATABASE_ERROR")
