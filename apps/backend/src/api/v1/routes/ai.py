"""
AI Runtime API Routes.

Endpoints for AI model management and inference:
- List available models
- Load/unload models
- Run inference
- Get runtime health
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status

from src.ai.interface import (
    InferenceRequest,
    InferenceResult,
    ModelInfo,
    HealthStatus,
)
from src.ai.onnx_runtime import ONNXRuntime

router = APIRouter()

# Global runtime instance (should be managed by app state in production)
_runtime: Optional[ONNXRuntime] = None


def get_ai_runtime() -> ONNXRuntime:
    """Get AI runtime instance."""
    global _runtime
    if _runtime is None:
        _runtime = ONNXRuntime()
    return _runtime


@router.get(
    "/health",
    response_model=HealthStatus,
    summary="Get AI runtime health",
    description="Get health status of the AI runtime including resource usage.",
)
async def get_health(
    runtime: ONNXRuntime = Depends(get_ai_runtime),
) -> HealthStatus:
    """Get AI runtime health status."""
    return await runtime.health()


@router.get(
    "/models",
    response_model=List[ModelInfo],
    summary="List AI models",
    description="Get a list of all available AI models.",
)
async def list_models(
    type: Optional[str] = None,
    capability: Optional[str] = None,
    runtime: ONNXRuntime = Depends(get_ai_runtime),
) -> List[ModelInfo]:
    """List available AI models."""
    return await runtime.list_models(type=type, capability=capability)


@router.post(
    "/models/{model_id}/load",
    summary="Load AI model",
    description="Load an AI model into memory for inference.",
)
async def load_model(
    model_id: str,
    runtime: ONNXRuntime = Depends(get_ai_runtime),
) -> dict:
    """Load an AI model."""
    try:
        result = await runtime.load_model(model_id)
        return result
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/models/{model_id}/unload",
    summary="Unload AI model",
    description="Unload an AI model from memory.",
)
async def unload_model(
    model_id: str,
    runtime: ONNXRuntime = Depends(get_ai_runtime),
) -> dict:
    """Unload an AI model."""
    await runtime.unload_model(model_id)
    return {"status": "unloaded", "model_id": model_id}


@router.post(
    "/infer",
    response_model=InferenceResult,
    summary="Run AI inference",
    description="Run inference on a loaded AI model.",
)
async def run_inference(
    request: InferenceRequest,
    runtime: ONNXRuntime = Depends(get_ai_runtime),
) -> InferenceResult:
    """Run AI inference."""
    try:
        result = await runtime.infer(request)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
