"""
Local AI Runtime using ONNX Runtime.

Provides local model inference using ONNX Runtime for:
- Image classification
- Object detection
- Scene analysis
- Other vision tasks
"""

import asyncio
import time
import uuid
from pathlib import Path
from typing import Any, AsyncGenerator, Dict, List, Optional
import psutil
import numpy as np

try:
    import onnxruntime as ort
    ONNX_AVAILABLE = True
except ImportError:
    ONNX_AVAILABLE = False

from src.config import settings
from src.core.logging import get_logger
from src.ai.interface import (
    AIRuntime,
    InferenceRequest,
    InferenceResult,
    UsageStats,
    TimingStats,
    HealthStatus,
    ModelInfo,
)

logger = get_logger(__name__)


class ONNXRuntime(AIRuntime):
    """
    ONNX Runtime implementation.
    
    Provides local AI inference using ONNX Runtime.
    Supports CPU and GPU (CUDA) execution providers.
    """
    
    def __init__(self) -> None:
        """Initialize ONNX Runtime."""
        self.models: Dict[str, Any] = {}
        self.sessions: Dict[str, ort.InferenceSession] = {}
        self.models_dir = Path(settings.AI_MODELS_DIR)
        self._initialized = False
        
        if not ONNX_AVAILABLE:
            logger.warning("ONNX Runtime not available - AI features will be limited")
    
    async def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the runtime."""
        if not ONNX_AVAILABLE:
            logger.warning("Cannot initialize ONNX Runtime - library not installed")
            return
        
        logger.info("Initializing ONNX Runtime...")
        
        # Create models directory if it doesn't exist
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        # Check available execution providers
        available_providers = ort.get_available_providers()
        logger.info(f"Available ONNX execution providers: {available_providers}")
        
        # Prefer CUDA if available
        if "CUDAExecutionProvider" in available_providers:
            logger.info("GPU (CUDA) acceleration available")
        else:
            logger.info("Using CPU execution")
        
        self._initialized = True
        logger.info("ONNX Runtime initialized")
    
    async def shutdown(self) -> None:
        """Shutdown the runtime."""
        logger.info("Shutting down ONNX Runtime...")
        
        # Unload all models
        for model_id in list(self.sessions.keys()):
            await self.unload_model(model_id)
        
        self._initialized = False
        logger.info("ONNX Runtime shut down")
    
    async def load_model(
        self, 
        model_id: str, 
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Load an ONNX model into memory."""
        if not ONNX_AVAILABLE:
            raise RuntimeError("ONNX Runtime not available")
        
        if model_id in self.sessions:
            logger.warning(f"Model {model_id} already loaded")
            return {"status": "already_loaded"}
        
        # Construct model path
        model_path = self.models_dir / f"{model_id}.onnx"
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        logger.info(f"Loading ONNX model: {model_id}")
        
        # Determine execution providers
        providers = ['CPUExecutionProvider']
        if 'CUDAExecutionProvider' in ort.get_available_providers():
            providers.insert(0, 'CUDAExecutionProvider')
        
        # Create inference session
        session = ort.InferenceSession(
            str(model_path),
            providers=providers,
        )
        
        self.sessions[model_id] = session
        self.models[model_id] = {
            "id": model_id,
            "path": str(model_path),
            "loaded_at": time.time(),
        }
        
        logger.info(f"Model {model_id} loaded successfully")
        return {"status": "loaded", "providers": session.get_providers()}
    
    async def unload_model(self, model_id: str) -> None:
        """Unload a model from memory."""
        if model_id not in self.sessions:
            logger.warning(f"Model {model_id} not loaded")
            return
        
        logger.info(f"Unloading model: {model_id}")
        
        # Remove session and model info
        del self.sessions[model_id]
        del self.models[model_id]
        
        logger.info(f"Model {model_id} unloaded")
    
    async def list_models(
        self, 
        type: Optional[str] = None,
        capability: Optional[str] = None
    ) -> List[ModelInfo]:
        """List available ONNX models."""
        models: List[ModelInfo] = []
        
        # Scan models directory for .onnx files
        if self.models_dir.exists():
            for model_file in self.models_dir.glob("*.onnx"):
                model_id = model_file.stem
                is_loaded = model_id in self.sessions
                
                # Get file size
                size_mb = model_file.stat().st_size / (1024 * 1024)
                
                models.append(ModelInfo(
                    id=model_id,
                    name=model_id,
                    version="1.0.0",
                    type="onnx",
                    capabilities=["inference"],
                    loaded=is_loaded,
                    size_mb=round(size_mb, 2),
                ))
        
        return models
    
    async def infer(self, request: InferenceRequest) -> InferenceResult:
        """Run inference on a model."""
        if not ONNX_AVAILABLE:
            raise RuntimeError("ONNX Runtime not available")
        
        if request.model_id not in self.sessions:
            raise ValueError(f"Model {request.model_id} not loaded")
        
        start_time = time.time()
        task_id = str(uuid.uuid4())
        
        logger.info(f"Running inference on model {request.model_id} (task: {task_id})")
        
        # Get session
        session = self.sessions[request.model_id]
        
        # Prepare input (simplified - would need proper preprocessing)
        # This is a placeholder - actual implementation would depend on model requirements
        input_data = self._prepare_input(request.input, session)
        
        # Run inference
        inference_start = time.time()
        outputs = session.run(None, input_data)
        inference_time = (time.time() - inference_start) * 1000
        
        # Prepare result (simplified)
        result = self._prepare_output(outputs, request.output_schema)
        
        total_time = (time.time() - start_time) * 1000
        
        return InferenceResult(
            task_id=task_id,
            model_id=request.model_id,
            result=result,
            usage=UsageStats(
                compute_time_ms=inference_time,
            ),
            timing=TimingStats(
                inference_time_ms=inference_time,
                total_time_ms=total_time,
            ),
        )
    
    async def infer_stream(
        self, 
        request: InferenceRequest
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Run streaming inference (not implemented for ONNX)."""
        # ONNX doesn't support streaming, so we just yield the final result
        result = await self.infer(request)
        yield {
            "type": "complete",
            "data": result.result,
        }
    
    async def health(self) -> HealthStatus:
        """Get runtime health status."""
        # Get CPU and memory stats
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        memory_mb = memory.used / (1024 * 1024)
        
        # Check for GPU
        gpu_available = 'CUDAExecutionProvider' in ort.get_available_providers() if ONNX_AVAILABLE else False
        
        status = "healthy" if self._initialized else "unhealthy"
        if not ONNX_AVAILABLE:
            status = "degraded"
        
        return HealthStatus(
            status=status,
            loaded_models=len(self.sessions),
            gpu_available=gpu_available,
            cpu_percent=cpu_percent,
            memory_mb=memory_mb,
        )
    
    def _prepare_input(
        self, 
        input_data: Any, 
        session: ort.InferenceSession
    ) -> Dict[str, np.ndarray]:
        """
        Prepare input data for ONNX model.
        
        This is a simplified placeholder. Actual implementation would:
        - Load and preprocess images/videos
        - Resize to model input size
        - Normalize pixel values
        - Convert to proper numpy array format
        """
        # Get input shape from model
        input_name = session.get_inputs()[0].name
        input_shape = session.get_inputs()[0].shape
        
        # Create dummy input (replace with actual preprocessing)
        dummy_input = np.zeros(input_shape, dtype=np.float32)
        
        return {input_name: dummy_input}
    
    def _prepare_output(
        self, 
        outputs: List[np.ndarray], 
        output_schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Prepare model output according to schema.
        
        This is a simplified placeholder. Actual implementation would:
        - Parse model outputs
        - Apply post-processing
        - Format according to schema
        - Extract relevant information
        """
        # Simplified output formatting
        result: Dict[str, Any] = {
            "raw_output": [output.tolist() for output in outputs],
            "status": "success",
        }
        
        return result
