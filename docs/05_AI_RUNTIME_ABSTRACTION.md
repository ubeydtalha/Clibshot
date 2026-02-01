# 🧠 AI RUNTIME ABSTRACTION — CLIPSHOT

> Local, Cloud ve Self-hosted AI modellerini tek arayüz altında birleştiren AI runtime mimarisi.

---

## 🎯 TASARIM PRENSİPLERİ

1. **Unified Interface** — Tek API, çoklu provider
2. **Hot-Swappable** — Runtime değişimi restart gerektirmez
3. **Schema-Validated** — Structured input/output, prompt injection koruması
4. **Async First** — Non-blocking, streaming support
5. **Resource Aware** — GPU/CPU/RAM yönetimi

---

## 🏗️ MİMARİ GENEL BAKIŞ

```
┌─────────────────────────────────────────────────────────────┐
│                    AI RUNTIME ABSTRACTION                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   Local Runtime │  │  Cloud Runtime  │  │ Self-Host    │ │
│  │   (llama.cpp)   │  │  (OpenAI/etc)   │  │ (vLLM/Ollama)│ │
│  └────────┬────────┘  └────────┬────────┘  └──────┬───────┘ │
│           │                    │                   │         │
│           └────────────────────┼───────────────────┘         │
│                                │                             │
│                    ┌───────────┴───────────┐                 │
│                    │   AIRuntime Interface │                 │
│                    └───────────┬───────────┘                 │
│                                │                             │
│  ┌─────────────────────────────┼─────────────────────────┐  │
│  │              Schema Validator & Sanitizer              │  │
│  └─────────────────────────────┼─────────────────────────┘  │
│                                │                             │
│  ┌─────────────────────────────┼─────────────────────────┐  │
│  │              Task Queue & Resource Manager             │  │
│  └─────────────────────────────┴─────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 AI RUNTIME INTERFACE

### TypeScript Interface

```typescript
// core/ai-runtime/interface.ts

export interface AIRuntime {
  // Lifecycle
  initialize(config: AIConfig): Promise<void>;
  shutdown(): Promise<void>;
  
  // Model Management
  loadModel(modelId: string, options?: LoadOptions): Promise<LoadedModel>;
  unloadModel(modelId: string): Promise<void>;
  listModels(filter?: ModelFilter): Promise<ModelInfo[]>;
  getModel(modelId: string): Promise<ModelInfo | null>;
  
  // Inference
  infer<T>(request: InferenceRequest): Promise<InferenceResult<T>>;
  inferStream<T>(request: InferenceRequest): AsyncGenerator<StreamChunk<T>>;
  
  // Task Management
  listTasks(): Promise<AITask[]>;
  getTask(taskId: string): Promise<AITask | null>;
  cancelTask(taskId: string): Promise<void>;
  
  // Health & Metrics
  health(): Promise<HealthStatus>;
  metrics(): Promise<RuntimeMetrics>;
}

export interface InferenceRequest {
  modelId: string;
  task: AITaskType;
  input: StructuredInput;
  outputSchema: JSONSchema;
  options?: InferenceOptions;
}

export type AITaskType = 
  | 'highlight_detection'
  | 'metadata_generation'
  | 'transcription'
  | 'caption_generation'
  | 'scene_analysis'
  | 'emotion_detection'
  | 'game_event_detection'
  | 'thumbnail_generation'
  | 'custom';

export interface StructuredInput {
  // Video/Image inputs
  media?: {
    type: 'video' | 'image' | 'audio';
    path?: string;
    base64?: string;
    url?: string;
    frames?: number[];  // Specific frames to analyze
  };
  
  // Text inputs
  text?: string;
  
  // Context
  context?: {
    game?: string;
    language?: string;
    previousResults?: unknown[];
    customData?: Record<string, unknown>;
  };
  
  // Task-specific parameters
  parameters?: Record<string, unknown>;
}

export interface InferenceResult<T> {
  taskId: string;
  modelId: string;
  result: T;
  usage: UsageStats;
  timing: TimingStats;
}

export interface StreamChunk<T> {
  type: 'partial' | 'complete' | 'error';
  data?: Partial<T>;
  progress?: number;
  error?: string;
}
```

### Python Implementation

```python
# src/ai/interface.py

from abc import ABC, abstractmethod
from typing import AsyncGenerator, Generic, TypeVar, Optional, List, Dict, Any
from pydantic import BaseModel
from enum import Enum

T = TypeVar('T')


class AITaskType(str, Enum):
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
    type: str  # video, image, audio
    path: Optional[str] = None
    base64: Optional[str] = None
    url: Optional[str] = None
    frames: Optional[List[int]] = None


class StructuredInput(BaseModel):
    media: Optional[MediaInput] = None
    text: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    parameters: Optional[Dict[str, Any]] = None


class InferenceRequest(BaseModel):
    model_id: str
    task: AITaskType
    input: StructuredInput
    output_schema: Dict[str, Any]
    options: Optional[Dict[str, Any]] = None


class UsageStats(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    compute_time_ms: float = 0


class TimingStats(BaseModel):
    queue_time_ms: float = 0
    inference_time_ms: float = 0
    total_time_ms: float = 0


class InferenceResult(BaseModel, Generic[T]):
    task_id: str
    model_id: str
    result: T
    usage: UsageStats
    timing: TimingStats


class HealthStatus(BaseModel):
    status: str  # healthy, degraded, unhealthy
    loaded_models: int
    gpu_available: bool
    gpu_memory_used_mb: Optional[float] = None
    gpu_memory_total_mb: Optional[float] = None
    cpu_percent: float
    memory_mb: float


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
    ) -> List[Dict[str, Any]]:
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
```

---

## 🖥️ LOCAL RUNTIME (llama.cpp / ONNX)

```python
# src/ai/local.py

import asyncio
from pathlib import Path
from typing import AsyncGenerator, Dict, Any, List, Optional
import json

from llama_cpp import Llama
import onnxruntime as ort

from .interface import (
    AIRuntime, 
    InferenceRequest, 
    InferenceResult,
    HealthStatus,
    AITaskType,
)
from src.core.logging import get_logger

logger = get_logger(__name__)


class LocalAIRuntime(AIRuntime):
    """Local AI runtime using llama.cpp and ONNX."""
    
    def __init__(self):
        self.models: Dict[str, Any] = {}
        self.model_configs: Dict[str, Dict[str, Any]] = {}
        self.models_dir: Path = Path.home() / ".clipshot" / "models"
        self._lock = asyncio.Lock()
    
    async def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize local runtime."""
        self.models_dir = Path(config.get("models_dir", self.models_dir))
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        # Scan for available models
        await self._scan_models()
        
        logger.info("Local AI runtime initialized")
    
    async def shutdown(self) -> None:
        """Shutdown and unload all models."""
        for model_id in list(self.models.keys()):
            await self.unload_model(model_id)
        logger.info("Local AI runtime shutdown")
    
    async def _scan_models(self) -> None:
        """Scan models directory for available models."""
        for model_dir in self.models_dir.iterdir():
            if model_dir.is_dir():
                manifest_path = model_dir / "manifest.json"
                if manifest_path.exists():
                    with open(manifest_path) as f:
                        self.model_configs[model_dir.name] = json.load(f)
    
    async def load_model(
        self, 
        model_id: str, 
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Load a model into memory."""
        async with self._lock:
            if model_id in self.models:
                return {"status": "already_loaded", "model_id": model_id}
            
            config = self.model_configs.get(model_id)
            if not config:
                raise ValueError(f"Model '{model_id}' not found")
            
            model_path = self.models_dir / model_id / config["file"]
            
            if config["type"] == "gguf":
                # Load llama.cpp model
                model = Llama(
                    model_path=str(model_path),
                    n_ctx=config.get("context_length", 4096),
                    n_gpu_layers=config.get("gpu_layers", -1),
                    verbose=False,
                )
            elif config["type"] == "onnx":
                # Load ONNX model
                providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
                model = ort.InferenceSession(str(model_path), providers=providers)
            else:
                raise ValueError(f"Unsupported model type: {config['type']}")
            
            self.models[model_id] = model
            logger.info(f"Model loaded: {model_id}")
            
            return {
                "status": "loaded",
                "model_id": model_id,
                "type": config["type"],
            }
    
    async def unload_model(self, model_id: str) -> None:
        """Unload a model from memory."""
        async with self._lock:
            if model_id in self.models:
                del self.models[model_id]
                logger.info(f"Model unloaded: {model_id}")
    
    async def list_models(
        self, 
        type: Optional[str] = None,
        capability: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List available models."""
        models = []
        for model_id, config in self.model_configs.items():
            if type and config.get("type") != type:
                continue
            if capability and capability not in config.get("capabilities", []):
                continue
            
            models.append({
                "id": model_id,
                "name": config.get("name", model_id),
                "type": "local",
                "provider": config.get("provider", "unknown"),
                "capabilities": config.get("capabilities", []),
                "loaded": model_id in self.models,
                "size_mb": config.get("size_mb", 0),
                "requirements": config.get("requirements", {}),
            })
        
        return models
    
    async def infer(self, request: InferenceRequest) -> InferenceResult:
        """Run inference."""
        import time
        start_time = time.time()
        
        model = self.models.get(request.model_id)
        if not model:
            raise ValueError(f"Model '{request.model_id}' not loaded")
        
        # Build prompt based on task type
        prompt = self._build_prompt(request)
        
        # Run inference
        if isinstance(model, Llama):
            result = await self._infer_llama(model, prompt, request)
        else:
            result = await self._infer_onnx(model, request)
        
        # Validate output against schema
        validated_result = self._validate_output(result, request.output_schema)
        
        end_time = time.time()
        
        return InferenceResult(
            task_id=f"task_{int(time.time() * 1000)}",
            model_id=request.model_id,
            result=validated_result,
            usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            timing={"inference_time_ms": (end_time - start_time) * 1000},
        )
    
    def _build_prompt(self, request: InferenceRequest) -> str:
        """Build prompt from structured input."""
        task_prompts = {
            AITaskType.HIGHLIGHT_DETECTION: self._highlight_detection_prompt,
            AITaskType.METADATA_GENERATION: self._metadata_generation_prompt,
            AITaskType.SCENE_ANALYSIS: self._scene_analysis_prompt,
        }
        
        builder = task_prompts.get(request.task, self._generic_prompt)
        return builder(request.input)
    
    def _highlight_detection_prompt(self, input: StructuredInput) -> str:
        """Build highlight detection prompt."""
        game = input.context.get("game", "unknown") if input.context else "unknown"
        return f"""Analyze this {game} gameplay and identify highlight moments.

Output as JSON:
{{
  "highlights": [
    {{
      "timestamp_start": <float>,
      "timestamp_end": <float>,
      "type": "<kill|death|objective|funny|skill>",
      "confidence": <0.0-1.0>,
      "description": "<brief description>"
    }}
  ]
}}"""
    
    def _metadata_generation_prompt(self, input: StructuredInput) -> str:
        """Build metadata generation prompt."""
        language = input.context.get("language", "en") if input.context else "en"
        return f"""Generate engaging metadata for this gaming clip.
Language: {language}

Output as JSON:
{{
  "title": "<catchy title, max 60 chars>",
  "description": "<engaging description, max 200 chars>",
  "tags": ["<tag1>", "<tag2>", ...],
  "hashtags": ["#<hashtag1>", "#<hashtag2>", ...]
}}"""
    
    async def _infer_llama(
        self, 
        model: Llama, 
        prompt: str, 
        request: InferenceRequest
    ) -> Dict[str, Any]:
        """Run llama.cpp inference."""
        # Run in thread pool to not block
        loop = asyncio.get_event_loop()
        
        def _run():
            response = model(
                prompt,
                max_tokens=request.options.get("max_tokens", 1024) if request.options else 1024,
                temperature=request.options.get("temperature", 0.7) if request.options else 0.7,
                stop=["```", "\n\n\n"],
            )
            return response["choices"][0]["text"]
        
        text = await loop.run_in_executor(None, _run)
        
        # Parse JSON from response
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to extract JSON from text
            import re
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            raise ValueError("Failed to parse model output as JSON")
    
    def _validate_output(
        self, 
        result: Dict[str, Any], 
        schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate output against JSON schema."""
        import jsonschema
        jsonschema.validate(result, schema)
        return result
    
    async def infer_stream(
        self, 
        request: InferenceRequest
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Run streaming inference."""
        model = self.models.get(request.model_id)
        if not model:
            raise ValueError(f"Model '{request.model_id}' not loaded")
        
        prompt = self._build_prompt(request)
        
        # Stream tokens
        for output in model(prompt, max_tokens=1024, stream=True):
            token = output["choices"][0]["text"]
            yield {"type": "partial", "data": token}
        
        yield {"type": "complete"}
    
    async def health(self) -> HealthStatus:
        """Get runtime health status."""
        import psutil
        
        gpu_available = False
        gpu_memory_used = None
        gpu_memory_total = None
        
        try:
            import torch
            if torch.cuda.is_available():
                gpu_available = True
                gpu_memory_used = torch.cuda.memory_allocated() / 1024 / 1024
                gpu_memory_total = torch.cuda.get_device_properties(0).total_memory / 1024 / 1024
        except ImportError:
            pass
        
        return HealthStatus(
            status="healthy" if self.models else "idle",
            loaded_models=len(self.models),
            gpu_available=gpu_available,
            gpu_memory_used_mb=gpu_memory_used,
            gpu_memory_total_mb=gpu_memory_total,
            cpu_percent=psutil.cpu_percent(),
            memory_mb=psutil.Process().memory_info().rss / 1024 / 1024,
        )
```

---

## ☁️ CLOUD RUNTIME (OpenAI / Anthropic)

```python
# src/ai/cloud.py

from typing import AsyncGenerator, Dict, Any, List, Optional
import httpx
import json

from .interface import (
    AIRuntime, 
    InferenceRequest, 
    InferenceResult,
    HealthStatus,
)
from src.core.config import settings
from src.core.logging import get_logger

logger = get_logger(__name__)


class CloudAIRuntime(AIRuntime):
    """Cloud AI runtime for OpenAI, Anthropic, etc."""
    
    def __init__(self):
        self.providers: Dict[str, CloudProvider] = {}
        self.default_provider: str = "openai"
    
    async def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize cloud providers."""
        # OpenAI
        if api_key := config.get("openai_api_key"):
            self.providers["openai"] = OpenAIProvider(api_key)
        
        # Anthropic
        if api_key := config.get("anthropic_api_key"):
            self.providers["anthropic"] = AnthropicProvider(api_key)
        
        # Google AI
        if api_key := config.get("google_api_key"):
            self.providers["google"] = GoogleAIProvider(api_key)
        
        self.default_provider = config.get("default_provider", "openai")
        logger.info(f"Cloud AI runtime initialized with providers: {list(self.providers.keys())}")
    
    async def shutdown(self) -> None:
        """Shutdown cloud runtime."""
        for provider in self.providers.values():
            await provider.close()
    
    async def load_model(
        self, 
        model_id: str, 
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Cloud models are always available, just validate."""
        provider_id, model_name = self._parse_model_id(model_id)
        
        if provider_id not in self.providers:
            raise ValueError(f"Provider '{provider_id}' not configured")
        
        return {"status": "ready", "model_id": model_id}
    
    async def unload_model(self, model_id: str) -> None:
        """No-op for cloud models."""
        pass
    
    async def list_models(
        self, 
        type: Optional[str] = None,
        capability: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List available cloud models."""
        models = []
        
        for provider_id, provider in self.providers.items():
            for model in await provider.list_models():
                if type and model.get("type") != type:
                    continue
                if capability and capability not in model.get("capabilities", []):
                    continue
                
                models.append({
                    "id": f"{provider_id}/{model['id']}",
                    "name": model["name"],
                    "type": "cloud",
                    "provider": provider_id,
                    "capabilities": model.get("capabilities", []),
                    "loaded": True,  # Always available
                })
        
        return models
    
    def _parse_model_id(self, model_id: str) -> tuple[str, str]:
        """Parse provider/model from model_id."""
        if "/" in model_id:
            return model_id.split("/", 1)
        return self.default_provider, model_id
    
    async def infer(self, request: InferenceRequest) -> InferenceResult:
        """Run cloud inference."""
        provider_id, model_name = self._parse_model_id(request.model_id)
        provider = self.providers.get(provider_id)
        
        if not provider:
            raise ValueError(f"Provider '{provider_id}' not configured")
        
        return await provider.infer(model_name, request)
    
    async def infer_stream(
        self, 
        request: InferenceRequest
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Run streaming cloud inference."""
        provider_id, model_name = self._parse_model_id(request.model_id)
        provider = self.providers.get(provider_id)
        
        if not provider:
            raise ValueError(f"Provider '{provider_id}' not configured")
        
        async for chunk in provider.infer_stream(model_name, request):
            yield chunk
    
    async def health(self) -> HealthStatus:
        """Get cloud runtime health."""
        healthy_providers = 0
        for provider in self.providers.values():
            if await provider.health_check():
                healthy_providers += 1
        
        return HealthStatus(
            status="healthy" if healthy_providers > 0 else "unhealthy",
            loaded_models=healthy_providers,
            gpu_available=False,
            cpu_percent=0,
            memory_mb=0,
        )


class OpenAIProvider:
    """OpenAI API provider."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.AsyncClient(
            base_url="https://api.openai.com/v1",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=60.0,
        )
    
    async def close(self):
        await self.client.aclose()
    
    async def list_models(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "gpt-4o",
                "name": "GPT-4o",
                "capabilities": ["metadata_generation", "scene_analysis"],
            },
            {
                "id": "gpt-4o-mini",
                "name": "GPT-4o Mini",
                "capabilities": ["metadata_generation"],
            },
            {
                "id": "whisper-1",
                "name": "Whisper",
                "capabilities": ["transcription"],
            },
        ]
    
    async def infer(self, model: str, request: InferenceRequest) -> InferenceResult:
        import time
        start_time = time.time()
        
        messages = self._build_messages(request)
        
        response = await self.client.post("/chat/completions", json={
            "model": model,
            "messages": messages,
            "response_format": {"type": "json_object"},
            "max_tokens": request.options.get("max_tokens", 1024) if request.options else 1024,
        })
        response.raise_for_status()
        data = response.json()
        
        result = json.loads(data["choices"][0]["message"]["content"])
        
        return InferenceResult(
            task_id=f"task_{int(time.time() * 1000)}",
            model_id=f"openai/{model}",
            result=result,
            usage={
                "prompt_tokens": data["usage"]["prompt_tokens"],
                "completion_tokens": data["usage"]["completion_tokens"],
                "total_tokens": data["usage"]["total_tokens"],
            },
            timing={"inference_time_ms": (time.time() - start_time) * 1000},
        )
    
    def _build_messages(self, request: InferenceRequest) -> List[Dict[str, str]]:
        """Build OpenAI messages from request."""
        system_prompt = f"""You are an AI assistant for a gaming clip analysis tool.
Your task is: {request.task.value}
Respond in JSON format matching this schema: {json.dumps(request.output_schema)}"""
        
        user_content = []
        
        if request.input.text:
            user_content.append({"type": "text", "text": request.input.text})
        
        if request.input.media and request.input.media.base64:
            user_content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{request.input.media.base64}"}
            })
        
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content or "Analyze the provided content."},
        ]
    
    async def health_check(self) -> bool:
        try:
            response = await self.client.get("/models")
            return response.status_code == 200
        except:
            return False
```

---

## 🏠 SELF-HOSTED RUNTIME (Ollama / vLLM)

```python
# src/ai/self_host.py

from typing import AsyncGenerator, Dict, Any, List, Optional
import httpx
import json

from .interface import (
    AIRuntime, 
    InferenceRequest, 
    InferenceResult,
    HealthStatus,
)
from src.core.logging import get_logger

logger = get_logger(__name__)


class SelfHostedAIRuntime(AIRuntime):
    """Self-hosted AI runtime for Ollama, vLLM, LocalAI, etc."""
    
    def __init__(self):
        self.servers: Dict[str, SelfHostServer] = {}
    
    async def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize self-hosted servers."""
        for server_config in config.get("servers", []):
            server = SelfHostServer(
                name=server_config["name"],
                url=server_config["url"],
                type=server_config.get("type", "ollama"),
            )
            await server.connect()
            self.servers[server_config["name"]] = server
        
        logger.info(f"Self-hosted runtime initialized with servers: {list(self.servers.keys())}")
    
    async def shutdown(self) -> None:
        """Shutdown all server connections."""
        for server in self.servers.values():
            await server.close()
    
    async def load_model(
        self, 
        model_id: str, 
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Load model on self-hosted server."""
        server_name, model_name = self._parse_model_id(model_id)
        server = self.servers.get(server_name)
        
        if not server:
            raise ValueError(f"Server '{server_name}' not configured")
        
        return await server.load_model(model_name, options)
    
    async def unload_model(self, model_id: str) -> None:
        """Unload model from self-hosted server."""
        server_name, model_name = self._parse_model_id(model_id)
        server = self.servers.get(server_name)
        
        if server:
            await server.unload_model(model_name)
    
    async def list_models(
        self, 
        type: Optional[str] = None,
        capability: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List models from all servers."""
        models = []
        for server_name, server in self.servers.items():
            for model in await server.list_models():
                models.append({
                    "id": f"{server_name}/{model['name']}",
                    "name": model["name"],
                    "type": "self-host",
                    "provider": server.type,
                    "server": server_name,
                    "loaded": model.get("loaded", False),
                })
        return models
    
    def _parse_model_id(self, model_id: str) -> tuple[str, str]:
        """Parse server/model from model_id."""
        if "/" in model_id:
            return model_id.split("/", 1)
        # Use first available server
        return list(self.servers.keys())[0], model_id
    
    async def infer(self, request: InferenceRequest) -> InferenceResult:
        """Run inference on self-hosted server."""
        server_name, model_name = self._parse_model_id(request.model_id)
        server = self.servers.get(server_name)
        
        if not server:
            raise ValueError(f"Server '{server_name}' not configured")
        
        return await server.infer(model_name, request)
    
    async def infer_stream(
        self, 
        request: InferenceRequest
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Run streaming inference on self-hosted server."""
        server_name, model_name = self._parse_model_id(request.model_id)
        server = self.servers.get(server_name)
        
        if not server:
            raise ValueError(f"Server '{server_name}' not configured")
        
        async for chunk in server.infer_stream(model_name, request):
            yield chunk
    
    async def health(self) -> HealthStatus:
        """Get runtime health."""
        healthy = 0
        for server in self.servers.values():
            if await server.health_check():
                healthy += 1
        
        return HealthStatus(
            status="healthy" if healthy == len(self.servers) else "degraded",
            loaded_models=healthy,
            gpu_available=False,
            cpu_percent=0,
            memory_mb=0,
        )


class SelfHostServer:
    """Single self-hosted server connection."""
    
    def __init__(self, name: str, url: str, type: str = "ollama"):
        self.name = name
        self.url = url.rstrip("/")
        self.type = type
        self.client: Optional[httpx.AsyncClient] = None
    
    async def connect(self):
        self.client = httpx.AsyncClient(base_url=self.url, timeout=120.0)
    
    async def close(self):
        if self.client:
            await self.client.aclose()
    
    async def list_models(self) -> List[Dict[str, Any]]:
        if self.type == "ollama":
            response = await self.client.get("/api/tags")
            data = response.json()
            return [{"name": m["name"], "loaded": True} for m in data.get("models", [])]
        elif self.type == "vllm":
            response = await self.client.get("/v1/models")
            data = response.json()
            return [{"name": m["id"], "loaded": True} for m in data.get("data", [])]
        return []
    
    async def load_model(self, model: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if self.type == "ollama":
            # Ollama auto-loads on first request, but we can pre-pull
            response = await self.client.post("/api/pull", json={"name": model})
            return {"status": "loaded", "model": model}
        return {"status": "ready", "model": model}
    
    async def infer(self, model: str, request: InferenceRequest) -> InferenceResult:
        import time
        start_time = time.time()
        
        if self.type == "ollama":
            response = await self.client.post("/api/generate", json={
                "model": model,
                "prompt": self._build_prompt(request),
                "format": "json",
                "stream": False,
            })
            data = response.json()
            result = json.loads(data["response"])
        else:
            # vLLM compatible
            response = await self.client.post("/v1/completions", json={
                "model": model,
                "prompt": self._build_prompt(request),
                "max_tokens": 1024,
            })
            data = response.json()
            result = json.loads(data["choices"][0]["text"])
        
        return InferenceResult(
            task_id=f"task_{int(time.time() * 1000)}",
            model_id=f"{self.name}/{model}",
            result=result,
            usage={},
            timing={"inference_time_ms": (time.time() - start_time) * 1000},
        )
    
    def _build_prompt(self, request: InferenceRequest) -> str:
        return f"""Task: {request.task.value}
Input: {json.dumps(request.input.dict())}
Output JSON Schema: {json.dumps(request.output_schema)}

Respond with valid JSON only:"""
    
    async def health_check(self) -> bool:
        try:
            response = await self.client.get("/api/tags" if self.type == "ollama" else "/health")
            return response.status_code == 200
        except:
            return False
```

---

## 🔧 AI MODEL MANIFEST

```json
{
  "id": "llama-3.2-11b-vision",
  "name": "Llama 3.2 11B Vision",
  "description": "Vision-language model for gaming clip analysis",
  "type": "gguf",
  "provider": "meta",
  "version": "3.2",
  
  "file": "llama-3.2-11b-vision-instruct-Q4_K_M.gguf",
  "size_mb": 6400,
  
  "capabilities": [
    "highlight_detection",
    "scene_analysis",
    "metadata_generation",
    "emotion_detection"
  ],
  
  "requirements": {
    "vram_gb": 8,
    "ram_gb": 16,
    "disk_gb": 7
  },
  
  "quantizations": {
    "Q4_K_M": {"size_mb": 6400, "vram_gb": 6},
    "Q5_K_M": {"size_mb": 7500, "vram_gb": 8},
    "Q8_0": {"size_mb": 12000, "vram_gb": 12}
  },
  
  "config": {
    "context_length": 8192,
    "gpu_layers": 35
  },
  
  "download": {
    "url": "https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct-GGUF",
    "checksum": "sha256:abc123..."
  }
}
```

---

## 🎯 Bu Mimarinin Avantajları

1. **Unified API** — Tek interface, çoklu backend
2. **Hot-Swap** — Runtime değişimi sorunsuz
3. **Schema Validation** — Güvenli, yapılandırılmış I/O
4. **Resource Management** — GPU/CPU aware
5. **Streaming Support** — Gerçek zamanlı yanıtlar
6. **Offline Capable** — Lokal modeller internet gerektirmez
