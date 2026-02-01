# ⚙️ BACKEND ARCHITECTURE — CLIPSHOT

> FastAPI tabanlı, modüler, OpenAPI-first backend mimarisi.

---

## 🎯 TASARIM PRENSİPLERİ

1. **Clean Architecture** — Dependency Inversion, Layer Separation
2. **Plugin-First** — Her özellik bir plugin endpoint'i
3. **OpenAPI-First** — Tüm endpoint'ler otomatik dokümante
4. **Async Everything** — Blocking operation yok
5. **Config-Driven** — Hardcoded değer yok

---

## 📁 DOSYA YAPISI

```
apps/backend/
├── src/
│   ├── __init__.py
│   ├── main.py                  # Application entry
│   ├── config.py                # Settings
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py              # Dependency injection
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py        # Main v1 router
│   │       └── routes/
│   │           ├── __init__.py
│   │           ├── plugins.py
│   │           ├── capture.py
│   │           ├── clips.py
│   │           ├── ai.py
│   │           ├── metadata.py
│   │           ├── config.py
│   │           ├── marketplace.py
│   │           └── system.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── events.py
│   │   ├── exceptions.py
│   │   └── logging.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── clip.py
│   │   ├── plugin.py
│   │   └── config.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── clip.py
│   │   ├── plugin.py
│   │   ├── capture.py
│   │   ├── ai.py
│   │   └── config.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── capture.py
│   │   ├── clip.py
│   │   ├── ai_runtime.py
│   │   ├── metadata.py
│   │   └── marketplace.py
│   │
│   ├── plugins/
│   │   ├── __init__.py
│   │   ├── loader.py
│   │   ├── sandbox.py
│   │   ├── permissions.py
│   │   ├── validator.py
│   │   ├── conflict.py
│   │   └── watchdog.py
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── interface.py
│   │   ├── local.py
│   │   ├── cloud.py
│   │   └── self_host.py
│   │
│   └── db/
│       ├── __init__.py
│       ├── session.py
│       └── base.py
│
├── tests/
├── alembic/
└── pyproject.toml
```

---

## 🚀 MAIN APPLICATION

```python
# src/main.py

"""
ClipShot Backend — FastAPI Application
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

from src.config import settings
from src.api.v1.router import api_router
from src.core.events import EventBus
from src.core.logging import setup_logging
from src.plugins.loader import PluginLoader
from src.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    setup_logging()
    await init_db()
    
    # Load plugins
    plugin_loader = PluginLoader()
    await plugin_loader.discover_and_load()
    app.state.plugin_loader = plugin_loader
    
    # Initialize event bus
    event_bus = EventBus()
    app.state.event_bus = event_bus
    
    yield
    
    # Shutdown
    await plugin_loader.shutdown_all()
    await event_bus.close()


def create_app() -> FastAPI:
    """Create FastAPI application."""
    
    app = FastAPI(
        title="ClipShot API",
        description="""
## 🎮 ClipShot Backend API

Modüler gaming AI platformu için RESTful API.

### Özellikler
- 📹 Ekran/Oyun kaydı
- 🤖 AI highlight tespiti ve metadata üretimi
- 🧩 Plugin sistemi
- 🏪 Marketplace

### Dokümantasyon
- [Swagger UI](/docs)
- [ReDoc](/redoc)
- [OpenAPI JSON](/openapi.json)
        """,
        version=settings.VERSION,
        openapi_url="/openapi.json",
        docs_url=None,  # Custom docs
        redoc_url=None,  # Custom redoc
        lifespan=lifespan,
    )
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(api_router, prefix="/api")
    
    # Custom docs endpoints
    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui():
        return get_swagger_ui_html(
            openapi_url="/openapi.json",
            title=f"{settings.APP_NAME} - API Docs",
            swagger_favicon_url="/static/favicon.ico"
        )
    
    @app.get("/redoc", include_in_schema=False)
    async def custom_redoc():
        return get_redoc_html(
            openapi_url="/openapi.json",
            title=f"{settings.APP_NAME} - ReDoc"
        )
    
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
```

---

## ⚙️ CONFIGURATION

```python
# src/config.py

"""
Application configuration with environment variable support.
"""

from functools import lru_cache
from pathlib import Path
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="CLIPSHOT_",
        case_sensitive=False,
    )
    
    # Application
    APP_NAME: str = "ClipShot"
    VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # Server
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./clipshot.db"
    
    # Paths
    DATA_DIR: Path = Field(default_factory=lambda: Path.home() / ".clipshot")
    PLUGINS_DIR: Path = Field(default_factory=lambda: Path.home() / ".clipshot" / "plugins")
    CLIPS_DIR: Path = Field(default_factory=lambda: Path.home() / ".clipshot" / "clips")
    TEMP_DIR: Path = Field(default_factory=lambda: Path.home() / ".clipshot" / "temp")
    
    # AI
    AI_MODELS_DIR: Path = Field(default_factory=lambda: Path.home() / ".clipshot" / "models")
    DEFAULT_AI_PROVIDER: str = "local"
    
    # Security
    SECRET_KEY: str = "change-me-in-production"
    PLUGIN_SANDBOX_ENABLED: bool = True
    
    # Performance
    MAX_WORKERS: int = 4
    PLUGIN_TIMEOUT: int = 30
    
    def ensure_dirs(self):
        """Create required directories."""
        for path in [self.DATA_DIR, self.PLUGINS_DIR, self.CLIPS_DIR, 
                     self.TEMP_DIR, self.AI_MODELS_DIR]:
            path.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    settings = Settings()
    settings.ensure_dirs()
    return settings


settings = get_settings()
```

---

## 🛣️ API ROUTER

```python
# src/api/v1/router.py

"""
API v1 Main Router
"""

from fastapi import APIRouter

from src.api.v1.routes import (
    plugins,
    capture,
    clips,
    ai,
    metadata,
    config,
    marketplace,
    system,
)

api_router = APIRouter()

# System routes
api_router.include_router(
    system.router,
    prefix="/v1/system",
    tags=["System"]
)

# Plugin routes
api_router.include_router(
    plugins.router,
    prefix="/v1/plugins",
    tags=["Plugins"]
)

# Capture routes
api_router.include_router(
    capture.router,
    prefix="/v1/capture",
    tags=["Capture"]
)

# Clips routes
api_router.include_router(
    clips.router,
    prefix="/v1/clips",
    tags=["Clips"]
)

# AI routes
api_router.include_router(
    ai.router,
    prefix="/v1/ai",
    tags=["AI"]
)

# Metadata routes
api_router.include_router(
    metadata.router,
    prefix="/v1/metadata",
    tags=["Metadata"]
)

# Config routes
api_router.include_router(
    config.router,
    prefix="/v1/config",
    tags=["Configuration"]
)

# Marketplace routes
api_router.include_router(
    marketplace.router,
    prefix="/v1/marketplace",
    tags=["Marketplace"]
)
```

---

## 📝 ROUTE EXAMPLES

### Plugins Router

```python
# src/api/v1/routes/plugins.py

"""
Plugin Management Routes
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel

from src.api.deps import get_plugin_loader, get_current_user
from src.schemas.plugin import (
    PluginInfo,
    PluginConfig,
    PluginPermissions,
    PluginInstallRequest,
    PluginHealth,
)
from src.plugins.loader import PluginLoader

router = APIRouter()


@router.get(
    "/",
    response_model=List[PluginInfo],
    summary="List all plugins",
    description="Get a list of all installed plugins with their current status.",
)
async def list_plugins(
    type: Optional[str] = Query(None, description="Filter by plugin type"),
    category: Optional[str] = Query(None, description="Filter by category"),
    enabled: Optional[bool] = Query(None, description="Filter by enabled status"),
    loader: PluginLoader = Depends(get_plugin_loader),
) -> List[PluginInfo]:
    """List all installed plugins."""
    plugins = await loader.list_plugins(type=type, category=category, enabled=enabled)
    return [PluginInfo.from_plugin(p) for p in plugins]


@router.get(
    "/{plugin_id}",
    response_model=PluginInfo,
    summary="Get plugin details",
    description="Get detailed information about a specific plugin.",
)
async def get_plugin(
    plugin_id: str,
    loader: PluginLoader = Depends(get_plugin_loader),
) -> PluginInfo:
    """Get plugin details by ID."""
    plugin = await loader.get_plugin(plugin_id)
    if not plugin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plugin '{plugin_id}' not found"
        )
    return PluginInfo.from_plugin(plugin)


@router.post(
    "/{plugin_id}/install",
    response_model=PluginInfo,
    summary="Install plugin",
    description="Install a plugin from GitHub or local path.",
    status_code=status.HTTP_201_CREATED,
)
async def install_plugin(
    plugin_id: str,
    request: PluginInstallRequest,
    loader: PluginLoader = Depends(get_plugin_loader),
) -> PluginInfo:
    """Install a plugin."""
    try:
        plugin = await loader.install(
            plugin_id=plugin_id,
            source=request.source,
            version=request.version,
        )
        return PluginInfo.from_plugin(plugin)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete(
    "/{plugin_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Uninstall plugin",
    description="Remove a plugin from the system.",
)
async def uninstall_plugin(
    plugin_id: str,
    loader: PluginLoader = Depends(get_plugin_loader),
):
    """Uninstall a plugin."""
    success = await loader.uninstall(plugin_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plugin '{plugin_id}' not found"
        )


@router.get(
    "/{plugin_id}/config",
    response_model=PluginConfig,
    summary="Get plugin configuration",
    description="Get the current configuration for a plugin.",
)
async def get_plugin_config(
    plugin_id: str,
    loader: PluginLoader = Depends(get_plugin_loader),
) -> PluginConfig:
    """Get plugin configuration."""
    config = await loader.get_plugin_config(plugin_id)
    return config


@router.put(
    "/{plugin_id}/config",
    response_model=PluginConfig,
    summary="Update plugin configuration",
    description="Update the configuration for a plugin.",
)
async def update_plugin_config(
    plugin_id: str,
    config: dict,
    loader: PluginLoader = Depends(get_plugin_loader),
) -> PluginConfig:
    """Update plugin configuration."""
    updated = await loader.update_plugin_config(plugin_id, config)
    return updated


@router.get(
    "/{plugin_id}/permissions",
    response_model=PluginPermissions,
    summary="Get plugin permissions",
    description="Get the permission settings for a plugin.",
)
async def get_plugin_permissions(
    plugin_id: str,
    loader: PluginLoader = Depends(get_plugin_loader),
) -> PluginPermissions:
    """Get plugin permissions."""
    return await loader.get_plugin_permissions(plugin_id)


@router.put(
    "/{plugin_id}/permissions",
    response_model=PluginPermissions,
    summary="Update plugin permissions",
    description="Update permission toggles for a plugin.",
)
async def update_plugin_permissions(
    plugin_id: str,
    permissions: PluginPermissions,
    loader: PluginLoader = Depends(get_plugin_loader),
) -> PluginPermissions:
    """Update plugin permissions."""
    return await loader.update_plugin_permissions(plugin_id, permissions)


@router.get(
    "/{plugin_id}/health",
    response_model=PluginHealth,
    summary="Get plugin health",
    description="Check the health status of a plugin.",
)
async def get_plugin_health(
    plugin_id: str,
    loader: PluginLoader = Depends(get_plugin_loader),
) -> PluginHealth:
    """Get plugin health status."""
    return await loader.check_plugin_health(plugin_id)


@router.post(
    "/{plugin_id}/enable",
    response_model=PluginInfo,
    summary="Enable plugin",
)
async def enable_plugin(
    plugin_id: str,
    loader: PluginLoader = Depends(get_plugin_loader),
) -> PluginInfo:
    """Enable a plugin."""
    plugin = await loader.enable_plugin(plugin_id)
    return PluginInfo.from_plugin(plugin)


@router.post(
    "/{plugin_id}/disable",
    response_model=PluginInfo,
    summary="Disable plugin",
)
async def disable_plugin(
    plugin_id: str,
    loader: PluginLoader = Depends(get_plugin_loader),
) -> PluginInfo:
    """Disable a plugin."""
    plugin = await loader.disable_plugin(plugin_id)
    return PluginInfo.from_plugin(plugin)
```

### AI Router

```python
# src/api/v1/routes/ai.py

"""
AI Runtime Routes
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sse_starlette.sse import EventSourceResponse

from src.api.deps import get_ai_runtime
from src.schemas.ai import (
    AIModel,
    AIModelList,
    InferenceRequest,
    InferenceResponse,
    AITask,
    AIHealth,
)
from src.ai.interface import AIRuntime

router = APIRouter()


@router.get(
    "/models",
    response_model=AIModelList,
    summary="List AI models",
    description="Get all available AI models (local, cloud, self-hosted).",
)
async def list_models(
    type: Optional[str] = None,
    capability: Optional[str] = None,
    runtime: AIRuntime = Depends(get_ai_runtime),
) -> AIModelList:
    """List available AI models."""
    models = await runtime.list_models(type=type, capability=capability)
    return AIModelList(models=models)


@router.post(
    "/models/{model_id}/load",
    response_model=AIModel,
    summary="Load AI model",
    description="Load an AI model into memory for inference.",
)
async def load_model(
    model_id: str,
    background_tasks: BackgroundTasks,
    runtime: AIRuntime = Depends(get_ai_runtime),
) -> AIModel:
    """Load an AI model."""
    model = await runtime.load_model(model_id)
    return model


@router.post(
    "/models/{model_id}/unload",
    summary="Unload AI model",
    description="Unload an AI model from memory.",
)
async def unload_model(
    model_id: str,
    runtime: AIRuntime = Depends(get_ai_runtime),
):
    """Unload an AI model."""
    await runtime.unload_model(model_id)
    return {"status": "unloaded"}


@router.post(
    "/infer",
    response_model=InferenceResponse,
    summary="Run inference",
    description="Run AI inference with structured input and output schemas.",
)
async def infer(
    request: InferenceRequest,
    runtime: AIRuntime = Depends(get_ai_runtime),
) -> InferenceResponse:
    """Run AI inference."""
    result = await runtime.infer(request)
    return result


@router.post(
    "/infer/stream",
    summary="Stream inference",
    description="Run AI inference with streaming response.",
)
async def infer_stream(
    request: InferenceRequest,
    runtime: AIRuntime = Depends(get_ai_runtime),
):
    """Run streaming AI inference."""
    async def generate():
        async for chunk in runtime.infer_stream(request):
            yield {"data": chunk}
    
    return EventSourceResponse(generate())


@router.get(
    "/tasks",
    response_model=List[AITask],
    summary="List AI tasks",
    description="Get all running AI tasks.",
)
async def list_tasks(
    runtime: AIRuntime = Depends(get_ai_runtime),
) -> List[AITask]:
    """List running AI tasks."""
    return await runtime.list_tasks()


@router.get(
    "/tasks/{task_id}",
    response_model=AITask,
    summary="Get AI task",
    description="Get details of a specific AI task.",
)
async def get_task(
    task_id: str,
    runtime: AIRuntime = Depends(get_ai_runtime),
) -> AITask:
    """Get AI task details."""
    task = await runtime.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete(
    "/tasks/{task_id}",
    summary="Cancel AI task",
)
async def cancel_task(
    task_id: str,
    runtime: AIRuntime = Depends(get_ai_runtime),
):
    """Cancel an AI task."""
    await runtime.cancel_task(task_id)
    return {"status": "cancelled"}


@router.get(
    "/health",
    response_model=AIHealth,
    summary="AI health check",
    description="Check AI runtime health and resource usage.",
)
async def health(
    runtime: AIRuntime = Depends(get_ai_runtime),
) -> AIHealth:
    """Get AI runtime health."""
    return await runtime.health()
```

### System Router

```python
# src/api/v1/routes/system.py

"""
System Routes — Health, Metrics, Events
"""

from typing import Optional
from fastapi import APIRouter, Depends, Request
from sse_starlette.sse import EventSourceResponse

from src.api.deps import get_event_bus
from src.core.events import EventBus
from src.schemas.system import (
    HealthResponse,
    MetricsResponse,
    OpenAPISpec,
)

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="System health check",
    description="Check overall system health including all components.",
)
async def health_check(request: Request) -> HealthResponse:
    """System health check."""
    plugin_loader = request.app.state.plugin_loader
    
    return HealthResponse(
        status="healthy",
        version=request.app.version,
        plugins={
            "total": len(plugin_loader.plugins),
            "active": len([p for p in plugin_loader.plugins.values() if p.is_running]),
        },
        database="connected",
        ai_runtime="ready",
    )


@router.get(
    "/metrics",
    response_model=MetricsResponse,
    summary="System metrics",
    description="Get performance metrics for the system and plugins.",
)
async def get_metrics(request: Request) -> MetricsResponse:
    """Get system metrics."""
    plugin_loader = request.app.state.plugin_loader
    
    plugin_metrics = {}
    for plugin_id, plugin in plugin_loader.plugins.items():
        plugin_metrics[plugin_id] = await plugin.get_metrics()
    
    return MetricsResponse(
        cpu_percent=await get_cpu_usage(),
        memory_mb=await get_memory_usage(),
        gpu_percent=await get_gpu_usage(),
        plugins=plugin_metrics,
    )


@router.get(
    "/events",
    summary="Event stream",
    description="Server-Sent Events stream for real-time updates.",
)
async def event_stream(
    event_type: Optional[str] = None,
    event_bus: EventBus = Depends(get_event_bus),
):
    """Subscribe to event stream."""
    async def generate():
        async for event in event_bus.subscribe(event_type):
            yield {
                "event": event.type,
                "data": event.data,
                "id": event.id,
            }
    
    return EventSourceResponse(generate())


@router.get(
    "/openapi",
    response_model=OpenAPISpec,
    summary="Get OpenAPI specification",
    description="Get full OpenAPI specification including plugin endpoints.",
)
async def get_openapi(request: Request) -> dict:
    """Get complete OpenAPI spec."""
    return request.app.openapi()
```

---

## 📊 SCHEMAS

```python
# src/schemas/plugin.py

"""
Plugin Pydantic Schemas
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
from pydantic import BaseModel, Field


class PluginType(str, Enum):
    CORE = "core"
    OPTIONAL = "optional"
    AI = "ai"
    UI = "ui"
    SYSTEM = "system"


class PluginStatus(str, Enum):
    INSTALLED = "installed"
    VALIDATED = "validated"
    APPROVED = "approved"
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"


class PermissionLevel(str, Enum):
    NONE = "none"
    LIMITED = "limited"
    OPTIONAL = "optional"
    REQUIRED = "required"


class PermissionEntry(BaseModel):
    """Single permission entry."""
    level: PermissionLevel
    granted: bool = False
    reason: Optional[Dict[str, str]] = None


class PluginPermissions(BaseModel):
    """Plugin permissions."""
    screen: PermissionEntry
    microphone: PermissionEntry
    filesystem: PermissionEntry
    network: PermissionEntry
    gpu: PermissionEntry
    system: PermissionEntry


class PluginAuthor(BaseModel):
    """Plugin author info."""
    name: str
    email: Optional[str] = None
    url: Optional[str] = None


class PluginInfo(BaseModel):
    """Plugin information."""
    id: str = Field(..., description="Unique plugin identifier")
    name: str = Field(..., description="Display name")
    version: str = Field(..., description="Semantic version")
    type: PluginType = Field(..., description="Plugin type")
    category: str = Field(..., description="Plugin category")
    description: Dict[str, str] = Field(..., description="Localized descriptions")
    author: PluginAuthor
    status: PluginStatus
    enabled: bool = True
    permissions: PluginPermissions
    
    installed_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
    
    @classmethod
    def from_plugin(cls, plugin) -> "PluginInfo":
        """Create from plugin instance."""
        return cls(
            id=plugin.id,
            name=plugin.manifest.name,
            version=plugin.manifest.version,
            type=plugin.manifest.type,
            category=plugin.manifest.category,
            description=plugin.manifest.description,
            author=PluginAuthor(**plugin.manifest.author),
            status=plugin.status,
            enabled=plugin.enabled,
            permissions=plugin.permissions,
            installed_at=plugin.installed_at,
            updated_at=plugin.updated_at,
        )


class PluginConfig(BaseModel):
    """Plugin configuration."""
    plugin_id: str
    config: Dict[str, Any]
    schema_: Optional[Dict[str, Any]] = Field(None, alias="schema")


class PluginInstallRequest(BaseModel):
    """Plugin install request."""
    source: str = Field(..., description="GitHub URL or local path")
    version: Optional[str] = Field(None, description="Specific version to install")


class PluginHealth(BaseModel):
    """Plugin health status."""
    plugin_id: str
    status: str = Field(..., description="healthy, degraded, or unhealthy")
    uptime_seconds: float
    cpu_percent: float
    memory_mb: float
    last_error: Optional[str] = None
    last_activity: datetime
```

---

## 🦀 NATIVE PLUGIN LOADER

Native plugin'ler (Rust, C, C++) için özel loader mekanizması:

```python
# src/plugins/native_loader.py

"""
Native Plugin Loader — Rust, C, C++ plugin support
"""

import importlib
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional, Protocol
from dataclasses import dataclass
from enum import Enum

from src.core.logging import get_logger
from src.core.events import EventBus

logger = get_logger(__name__)

# Supported ABI versions
SUPPORTED_ABI_VERSIONS = [1]


class NativeLanguage(str, Enum):
    RUST = "rust"
    C = "c"
    CPP = "cpp"


class FFIBridge(str, Enum):
    PYO3 = "pyo3"       # Rust → Python
    CFFI = "cffi"       # C → Python
    PYBIND11 = "pybind11"  # C++ → Python


@dataclass
class NativePluginInfo:
    """Native plugin information."""
    id: str
    name: str
    version: str
    language: NativeLanguage
    abi_version: int
    module: Any


class NativePluginProtocol(Protocol):
    """Protocol for native plugins."""
    
    def init(self, config: str) -> None: ...
    def shutdown(self) -> None: ...


class NativePluginLoader:
    """Loader for native (Rust/C/C++) plugins."""
    
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.loaded_plugins: Dict[str, NativePluginInfo] = {}
    
    async def load(self, manifest: dict, plugin_path: Path) -> NativePluginInfo:
        """Load a native plugin from manifest."""
        native_config = manifest.get("native", {})
        
        if not native_config:
            raise ValueError("Not a native plugin (missing 'native' section)")
        
        # 1. ABI version check
        abi_version = native_config.get("abi_version", 0)
        if abi_version not in SUPPORTED_ABI_VERSIONS:
            raise ValueError(
                f"Unsupported ABI version: {abi_version}. "
                f"Supported: {SUPPORTED_ABI_VERSIONS}"
            )
        
        # 2. Verify binary hash
        await self._verify_binary(native_config, plugin_path)
        
        # 3. Load module based on FFI bridge
        ffi_config = native_config.get("ffi", {})
        bridge = FFIBridge(ffi_config.get("bridge", "pyo3"))
        module_name = ffi_config.get("module_name")
        
        if bridge == FFIBridge.PYO3:
            module = await self._load_pyo3_module(module_name, plugin_path)
        elif bridge == FFIBridge.CFFI:
            module = await self._load_cffi_module(native_config, plugin_path)
        elif bridge == FFIBridge.PYBIND11:
            module = await self._load_pybind11_module(module_name, plugin_path)
        else:
            raise ValueError(f"Unknown FFI bridge: {bridge}")
        
        # 4. Verify ABI from module
        if hasattr(module, "get_abi_version"):
            actual_abi = module.get_abi_version()
            if actual_abi != abi_version:
                raise ValueError(
                    f"ABI mismatch: manifest={abi_version}, module={actual_abi}"
                )
        
        # 5. Create plugin info
        plugin_info = NativePluginInfo(
            id=manifest["id"],
            name=manifest["name"],
            version=manifest.get("version", "0.0.0"),
            language=NativeLanguage(native_config["language"]),
            abi_version=abi_version,
            module=module,
        )
        
        self.loaded_plugins[plugin_info.id] = plugin_info
        
        logger.info(f"Loaded native plugin: {plugin_info.id} ({plugin_info.language})")
        
        await self.event_bus.emit("plugin:native_loaded", {
            "id": plugin_info.id,
            "language": plugin_info.language.value,
        })
        
        return plugin_info
    
    async def _verify_binary(self, native_config: dict, plugin_path: Path) -> None:
        """Verify binary hash for security."""
        import platform
        
        # Determine platform key
        system = platform.system().lower()
        machine = platform.machine().lower()
        
        if system == "windows":
            platform_key = f"windows-{'x64' if machine in ('amd64', 'x86_64') else 'x86'}"
        else:
            platform_key = f"{system}-{'x64' if machine in ('amd64', 'x86_64') else machine}"
        
        binaries = native_config.get("binaries", {})
        binary_info = binaries.get(platform_key)
        
        if not binary_info:
            raise ValueError(f"No binary for platform: {platform_key}")
        
        binary_path = plugin_path / binary_info["path"]
        expected_hash = binary_info.get("sha256")
        
        if expected_hash:
            actual_hash = await self._compute_hash(binary_path)
            if actual_hash != expected_hash:
                raise ValueError(
                    f"Binary hash mismatch for {binary_path}: "
                    f"expected={expected_hash[:16]}..., actual={actual_hash[:16]}..."
                )
    
    async def _compute_hash(self, path: Path) -> str:
        """Compute SHA256 hash of file."""
        import aiofiles
        
        sha256 = hashlib.sha256()
        async with aiofiles.open(path, "rb") as f:
            while chunk := await f.read(65536):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    async def _load_pyo3_module(self, module_name: str, plugin_path: Path) -> Any:
        """Load PyO3 (Rust) module."""
        import sys
        
        # Add plugin path to sys.path temporarily
        plugin_lib_path = plugin_path / "lib"
        sys.path.insert(0, str(plugin_lib_path))
        
        try:
            module = importlib.import_module(module_name)
            return module
        finally:
            sys.path.remove(str(plugin_lib_path))
    
    async def _load_cffi_module(self, native_config: dict, plugin_path: Path) -> Any:
        """Load cffi (C) module."""
        from cffi import FFI
        import platform
        
        ffi = FFI()
        
        # Get binary path
        system = platform.system().lower()
        machine = platform.machine().lower()
        platform_key = f"windows-{'x64' if machine in ('amd64', 'x86_64') else 'x86'}"
        
        binary_info = native_config["binaries"][platform_key]
        lib_path = plugin_path / binary_info["path"]
        
        return ffi.dlopen(str(lib_path))
    
    async def _load_pybind11_module(self, module_name: str, plugin_path: Path) -> Any:
        """Load pybind11 (C++) module."""
        return await self._load_pyo3_module(module_name, plugin_path)
    
    async def unload(self, plugin_id: str) -> None:
        """Unload a native plugin."""
        if plugin_id not in self.loaded_plugins:
            return
        
        plugin_info = self.loaded_plugins[plugin_id]
        
        # Call shutdown if available
        if hasattr(plugin_info.module, "shutdown"):
            plugin_info.module.shutdown()
        
        del self.loaded_plugins[plugin_id]
        
        logger.info(f"Unloaded native plugin: {plugin_id}")
    
    def is_native_plugin(self, manifest: dict) -> bool:
        """Check if manifest is for a native plugin."""
        return "native" in manifest


# Integration with main PluginLoader
class PluginLoaderWithNativeSupport:
    """Extended plugin loader with native support."""
    
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.native_loader = NativePluginLoader(event_bus)
        self.python_plugins: Dict[str, Any] = {}
        self.native_plugins: Dict[str, NativePluginInfo] = {}
    
    async def load_plugin(self, manifest: dict, plugin_path: Path) -> Any:
        """Load plugin (Python or Native)."""
        if self.native_loader.is_native_plugin(manifest):
            return await self.native_loader.load(manifest, plugin_path)
        else:
            return await self._load_python_plugin(manifest, plugin_path)
    
    async def _load_python_plugin(self, manifest: dict, plugin_path: Path) -> Any:
        """Load standard Python plugin."""
        # ... existing Python plugin loading logic
        pass
```

---

## 🔧 DEPENDENCY INJECTION

```python
# src/api/deps.py

"""
FastAPI Dependencies
"""

from typing import Generator, Optional
from fastapi import Depends, Request, HTTPException, status

from src.plugins.loader import PluginLoader
from src.ai.interface import AIRuntime
from src.core.events import EventBus
from src.db.session import get_session


async def get_plugin_loader(request: Request) -> PluginLoader:
    """Get plugin loader from app state."""
    return request.app.state.plugin_loader


async def get_ai_runtime(request: Request) -> AIRuntime:
    """Get AI runtime from app state."""
    return request.app.state.ai_runtime


async def get_event_bus(request: Request) -> EventBus:
    """Get event bus from app state."""
    return request.app.state.event_bus


async def get_db():
    """Get database session."""
    async with get_session() as session:
        yield session


async def verify_plugin_access(
    plugin_id: str,
    loader: PluginLoader = Depends(get_plugin_loader),
):
    """Verify plugin exists and is accessible."""
    plugin = await loader.get_plugin(plugin_id)
    if not plugin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plugin '{plugin_id}' not found"
        )
    return plugin
```

---

## 📖 OPENAPI ENHANCEMENTs

### Custom OpenAPI Generation

```python
# src/core/openapi.py

"""
Custom OpenAPI schema generation
"""

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def custom_openapi(app: FastAPI):
    """Generate custom OpenAPI schema with plugin endpoints."""
    
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Add custom extensions
    openapi_schema["info"]["x-logo"] = {
        "url": "https://clipshot.io/logo.png"
    }
    
    # Add server info
    openapi_schema["servers"] = [
        {"url": "http://localhost:8000", "description": "Development"},
        {"url": "https://api.clipshot.io", "description": "Production"},
    ]
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "apiKey": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key"
        }
    }
    
    # Add tags with descriptions
    openapi_schema["tags"] = [
        {"name": "System", "description": "System health and metrics"},
        {"name": "Plugins", "description": "Plugin management"},
        {"name": "Capture", "description": "Screen/game capture"},
        {"name": "Clips", "description": "Clip management"},
        {"name": "AI", "description": "AI inference and models"},
        {"name": "Metadata", "description": "AI-generated metadata"},
        {"name": "Configuration", "description": "App configuration"},
        {"name": "Marketplace", "description": "Plugin marketplace"},
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema
```

---

## 🧪 TESTING

```python
# tests/conftest.py

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from src.main import create_app
from src.db.base import Base


@pytest.fixture
async def app():
    """Create test application."""
    app = create_app()
    yield app


@pytest.fixture
async def client(app):
    """Create test client."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
async def db_session():
    """Create test database session."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSession(engine) as session:
        yield session
```

```python
# tests/test_plugins.py

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_plugins(client: AsyncClient):
    response = await client.get("/api/v1/plugins/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_plugin_not_found(client: AsyncClient):
    response = await client.get("/api/v1/plugins/nonexistent")
    assert response.status_code == 404
```

---

## 🎯 Bu Mimarinin Avantajları

1. **Modülerlik** — Her route modülü bağımsız
2. **Dokümantasyon** — Otomatik OpenAPI/Swagger
3. **Type Safety** — Pydantic ile tam tip kontrolü
4. **Testability** — Kolay test edilebilir yapı
5. **Scalability** — Yatay ölçeklenebilir
6. **Extensibility** — Plugin endpoint'leri dinamik eklenir
