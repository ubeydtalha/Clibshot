"""
AI Runtime Abstract Interface.

Defines the base interface that all AI runtimes must implement.
Supports multiple backends (ONNX, TensorFlow Lite, etc.).
"""

from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Dict, List, Optional
from pydantic import BaseModel
from enum import Enum


class AITaskType(str, Enum):
    """AI task types."""
    
    HIGHLIGHT_DETECTION = "highlight_detection"
    METADATA_GENERATION = "metadata_generation"
    TRANSCRIPTION = "transcription"
    CAPTION_GENERATION = "caption_generation"
    SCENE_ANALYSIS = "scene_analysis"
    EMOTION_DETECTION = "emotion_detection"
    GAME_EVENT_DETECTION = "game_event_detection"
    THUMBNAIL_GENERATION = "thumbnail_generation"
    CUSTOM = "custom"


class MediaInput(BaseModel):
    """Media input for AI inference."""
    
    type: str  # video, image, audio
    path: Optional[str] = None
    base64: Optional[str] = None
    url: Optional[str] = None
    frames: Optional[List[int]] = None


class StructuredInput(BaseModel):
    """Structured input for AI inference."""
    
    media: Optional[MediaInput] = None
    text: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    parameters: Optional[Dict[str, Any]] = None


class InferenceRequest(BaseModel):
    """AI inference request."""
    
    model_config = {"protected_namespaces": ()}
    
    model_id: str
    task: AITaskType
    input: StructuredInput
    output_schema: Dict[str, Any]
    options: Optional[Dict[str, Any]] = None


class UsageStats(BaseModel):
    """Resource usage statistics."""
    
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    compute_time_ms: float = 0


class TimingStats(BaseModel):
    """Timing statistics."""
    
    queue_time_ms: float = 0
    inference_time_ms: float = 0
    total_time_ms: float = 0


class InferenceResult(BaseModel):
    """AI inference result."""
    
    model_config = {"protected_namespaces": ()}
    
    task_id: str
    model_id: str
    result: Any
    usage: UsageStats
    timing: TimingStats


class HealthStatus(BaseModel):
    """Runtime health status."""
    
    status: str  # healthy, degraded, unhealthy
    loaded_models: int
    gpu_available: bool
    gpu_memory_used_mb: Optional[float] = None
    gpu_memory_total_mb: Optional[float] = None
    cpu_percent: float
    memory_mb: float


class ModelInfo(BaseModel):
    """AI model information."""
    
    id: str
    name: str
    version: str
    type: str
    capabilities: List[str]
    loaded: bool
    size_mb: Optional[float] = None


class AIRuntime(ABC):
    """Abstract AI Runtime interface."""
    
    @abstractmethod
    async def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the runtime."""
        pass
    
    @abstractmethod
    async def shutdown(self) -> None:
        """Shutdown the runtime."""
        pass
    
    @abstractmethod
    async def load_model(
        self, 
        model_id: str, 
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Load a model into memory."""
        pass
    
    @abstractmethod
    async def unload_model(self, model_id: str) -> None:
        """Unload a model from memory."""
        pass
    
    @abstractmethod
    async def list_models(
        self, 
        type: Optional[str] = None,
        capability: Optional[str] = None
    ) -> List[ModelInfo]:
        """List available models."""
        pass
    
    @abstractmethod
    async def infer(self, request: InferenceRequest) -> InferenceResult:
        """Run inference."""
        pass
    
    @abstractmethod
    async def infer_stream(
        self, 
        request: InferenceRequest
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Run streaming inference."""
        pass
    
    @abstractmethod
    async def health(self) -> HealthStatus:
        """Get runtime health status."""
        pass
