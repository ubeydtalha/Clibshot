# ⚡ PERFORMANCE & MCP — CLIPSHOT

> Performans hedefleri, optimizasyonlar ve AI-kontrollü API (MCP) mimarisi.

---

## 🎯 PERFORMANS HEDEFLERİ

| Metrik | Hedef | Kritik |
|--------|-------|--------|
| UI Frame Time | <16ms (60fps) | <33ms (30fps) |
| Clip Trigger Latency | <50ms | <100ms |
| AI Inference (Local) | <200ms | <500ms |
| AI Inference (Cloud) | <1s | <3s |
| App Cold Start | <3s | <5s |
| Memory Usage | <512MB | <1GB |
| CPU Idle | <2% | <5% |
| GPU Capture Overhead | <5% | <10% |

---

## 🏗️ PERFORMANS MİMARİSİ

```
┌─────────────────────────────────────────────────────────────────┐
│                    PERFORMANCE MONITORING                        │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Metrics Collector                      │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐         │  │
│  │  │   CPU   │ │ Memory  │ │   GPU   │ │   I/O   │         │  │
│  │  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘         │  │
│  │       │           │           │           │               │  │
│  │       └───────────┴───────────┴───────────┘               │  │
│  │                           │                               │  │
│  │                    ┌──────▼──────┐                        │  │
│  │                    │  Aggregator │                        │  │
│  │                    └──────┬──────┘                        │  │
│  │                           │                               │  │
│  │  ┌────────────────────────┼────────────────────────────┐  │  │
│  │  │                        ▼                            │  │  │
│  │  │  ┌───────────┐  ┌──────────┐  ┌───────────────┐    │  │  │
│  │  │  │ Threshold │  │ Alerting │  │ Auto-Optimize │    │  │  │
│  │  │  │  Monitor  │  │  System  │  │    Engine     │    │  │  │
│  │  │  └───────────┘  └──────────┘  └───────────────┘    │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 METRICS COLLECTOR

```python
# src/core/metrics.py

import asyncio
import time
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque
import psutil
import statistics

from src.core.logging import get_logger
from src.core.events import EventBus

logger = get_logger(__name__)


@dataclass
class MetricSample:
    """Single metric sample."""
    name: str
    value: float
    timestamp: datetime
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricStats:
    """Statistics for a metric over a time window."""
    name: str
    min: float
    max: float
    avg: float
    p50: float
    p95: float
    p99: float
    count: int
    window_seconds: int


class MetricsCollector:
    """Collects and aggregates performance metrics."""
    
    # Retention: 1 minute of samples at 1 sample/second
    MAX_SAMPLES = 60
    
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.samples: Dict[str, deque] = {}
        self.thresholds: Dict[str, float] = {}
        self.running = False
        self._task: Optional[asyncio.Task] = None
    
    async def start(self) -> None:
        """Start metrics collection."""
        self.running = True
        self._task = asyncio.create_task(self._collect_loop())
        logger.info("Metrics collector started")
    
    async def stop(self) -> None:
        """Stop metrics collection."""
        self.running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
    
    def record(
        self, 
        name: str, 
        value: float, 
        tags: Optional[Dict[str, str]] = None
    ) -> None:
        """Record a metric sample."""
        sample = MetricSample(
            name=name,
            value=value,
            timestamp=datetime.now(),
            tags=tags or {},
        )
        
        if name not in self.samples:
            self.samples[name] = deque(maxlen=self.MAX_SAMPLES)
        
        self.samples[name].append(sample)
        
        # Check thresholds
        if name in self.thresholds and value > self.thresholds[name]:
            asyncio.create_task(self._emit_threshold_breach(name, value))
    
    def set_threshold(self, name: str, value: float) -> None:
        """Set a threshold for alerting."""
        self.thresholds[name] = value
    
    def get_stats(self, name: str, window_seconds: int = 60) -> Optional[MetricStats]:
        """Get statistics for a metric."""
        if name not in self.samples:
            return None
        
        cutoff = datetime.now() - timedelta(seconds=window_seconds)
        values = [
            s.value for s in self.samples[name]
            if s.timestamp > cutoff
        ]
        
        if not values:
            return None
        
        sorted_values = sorted(values)
        n = len(sorted_values)
        
        return MetricStats(
            name=name,
            min=min(values),
            max=max(values),
            avg=statistics.mean(values),
            p50=sorted_values[int(n * 0.5)],
            p95=sorted_values[int(n * 0.95)] if n > 1 else sorted_values[0],
            p99=sorted_values[int(n * 0.99)] if n > 1 else sorted_values[0],
            count=n,
            window_seconds=window_seconds,
        )
    
    async def _collect_loop(self) -> None:
        """Periodically collect system metrics."""
        while self.running:
            try:
                await self._collect_system_metrics()
            except Exception as e:
                logger.error(f"Error collecting metrics: {e}")
            
            await asyncio.sleep(1)
    
    async def _collect_system_metrics(self) -> None:
        """Collect system-wide metrics."""
        # CPU
        cpu_percent = psutil.cpu_percent()
        self.record("system.cpu.percent", cpu_percent)
        
        # Memory
        memory = psutil.virtual_memory()
        self.record("system.memory.percent", memory.percent)
        self.record("system.memory.used_mb", memory.used / 1024 / 1024)
        
        # Process-specific
        process = psutil.Process()
        self.record("app.cpu.percent", process.cpu_percent())
        self.record("app.memory.mb", process.memory_info().rss / 1024 / 1024)
        self.record("app.threads", process.num_threads())
    
    async def _emit_threshold_breach(self, name: str, value: float) -> None:
        """Emit event when threshold is breached."""
        await self.event_bus.emit("metrics:threshold_breach", {
            "metric": name,
            "value": value,
            "threshold": self.thresholds[name],
        })


class Timer:
    """Context manager for timing operations."""
    
    def __init__(
        self, 
        metrics: MetricsCollector, 
        name: str,
        tags: Optional[Dict[str, str]] = None
    ):
        self.metrics = metrics
        self.name = name
        self.tags = tags
        self.start_time: Optional[float] = None
    
    def __enter__(self) -> "Timer":
        self.start_time = time.perf_counter()
        return self
    
    def __exit__(self, *args) -> None:
        if self.start_time:
            duration_ms = (time.perf_counter() - self.start_time) * 1000
            self.metrics.record(self.name, duration_ms, self.tags)
    
    async def __aenter__(self) -> "Timer":
        self.start_time = time.perf_counter()
        return self
    
    async def __aexit__(self, *args) -> None:
        if self.start_time:
            duration_ms = (time.perf_counter() - self.start_time) * 1000
            self.metrics.record(self.name, duration_ms, self.tags)


def timed(metrics: MetricsCollector, name: str):
    """Decorator for timing functions."""
    def decorator(func: Callable):
        async def async_wrapper(*args, **kwargs):
            async with Timer(metrics, name):
                return await func(*args, **kwargs)
        
        def sync_wrapper(*args, **kwargs):
            with Timer(metrics, name):
                return func(*args, **kwargs)
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    
    return decorator
```

---

## ⚡ AUTO-OPTIMIZER

```python
# src/core/optimizer.py

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio

from src.core.metrics import MetricsCollector, MetricStats
from src.core.events import EventBus
from src.core.logging import get_logger

logger = get_logger(__name__)


class OptimizationLevel(str, Enum):
    QUALITY = "quality"      # Best quality, higher resource usage
    BALANCED = "balanced"    # Balance between quality and performance
    PERFORMANCE = "performance"  # Optimize for speed, lower quality


@dataclass
class OptimizationRule:
    """Rule for automatic optimization."""
    metric: str
    threshold: float
    action: str
    cooldown_seconds: int = 60
    last_triggered: Optional[float] = None


class AutoOptimizer:
    """Automatically adjusts settings based on performance."""
    
    RULES: List[OptimizationRule] = [
        # High CPU - reduce capture quality
        OptimizationRule(
            metric="app.cpu.percent",
            threshold=80,
            action="reduce_capture_quality",
            cooldown_seconds=30,
        ),
        # High memory - clear caches
        OptimizationRule(
            metric="app.memory.mb",
            threshold=800,
            action="clear_caches",
            cooldown_seconds=60,
        ),
        # High frame time - reduce UI complexity
        OptimizationRule(
            metric="ui.frame_time_ms",
            threshold=33,  # Below 30fps
            action="reduce_ui_effects",
            cooldown_seconds=30,
        ),
        # High AI latency - switch to lighter model
        OptimizationRule(
            metric="ai.inference_ms",
            threshold=500,
            action="use_lighter_model",
            cooldown_seconds=120,
        ),
    ]
    
    def __init__(
        self, 
        metrics: MetricsCollector, 
        event_bus: EventBus,
        level: OptimizationLevel = OptimizationLevel.BALANCED
    ):
        self.metrics = metrics
        self.event_bus = event_bus
        self.level = level
        self.running = False
        self._task: Optional[asyncio.Task] = None
    
    async def start(self) -> None:
        """Start auto-optimization."""
        self.running = True
        self._task = asyncio.create_task(self._optimization_loop())
        logger.info(f"Auto-optimizer started (level: {self.level.value})")
    
    async def stop(self) -> None:
        """Stop auto-optimization."""
        self.running = False
        if self._task:
            self._task.cancel()
    
    def set_level(self, level: OptimizationLevel) -> None:
        """Set optimization level."""
        self.level = level
        logger.info(f"Optimization level set to: {level.value}")
    
    async def _optimization_loop(self) -> None:
        """Check metrics and apply optimizations."""
        import time
        
        while self.running:
            now = time.time()
            
            for rule in self.RULES:
                # Check cooldown
                if rule.last_triggered and (now - rule.last_triggered) < rule.cooldown_seconds:
                    continue
                
                # Get metric stats
                stats = self.metrics.get_stats(rule.metric, 10)  # Last 10 seconds
                if not stats:
                    continue
                
                # Check threshold (adjust based on level)
                threshold = self._adjust_threshold(rule.threshold)
                
                if stats.p95 > threshold:
                    await self._apply_optimization(rule)
                    rule.last_triggered = now
            
            await asyncio.sleep(5)  # Check every 5 seconds
    
    def _adjust_threshold(self, base_threshold: float) -> float:
        """Adjust threshold based on optimization level."""
        if self.level == OptimizationLevel.QUALITY:
            return base_threshold * 1.2  # More tolerant
        elif self.level == OptimizationLevel.PERFORMANCE:
            return base_threshold * 0.8  # Less tolerant
        return base_threshold
    
    async def _apply_optimization(self, rule: OptimizationRule) -> None:
        """Apply an optimization action."""
        logger.warning(f"Applying optimization: {rule.action} (triggered by {rule.metric})")
        
        if rule.action == "reduce_capture_quality":
            await self._reduce_capture_quality()
        elif rule.action == "clear_caches":
            await self._clear_caches()
        elif rule.action == "reduce_ui_effects":
            await self._reduce_ui_effects()
        elif rule.action == "use_lighter_model":
            await self._use_lighter_model()
        
        await self.event_bus.emit("optimization:applied", {
            "action": rule.action,
            "metric": rule.metric,
        })
    
    async def _reduce_capture_quality(self) -> None:
        """Reduce capture quality to save resources."""
        from src.capture.manager import CaptureManager
        manager = CaptureManager()
        
        # Reduce resolution or framerate
        current_settings = await manager.get_settings()
        if current_settings.fps > 30:
            await manager.update_settings(fps=30)
        elif current_settings.resolution > 720:
            await manager.update_settings(resolution=720)
    
    async def _clear_caches(self) -> None:
        """Clear various caches to free memory."""
        import gc
        gc.collect()
        
        # Clear clip thumbnails cache
        # Clear AI model cache
        # etc.
    
    async def _reduce_ui_effects(self) -> None:
        """Reduce UI effects for better performance."""
        await self.event_bus.emit("ui:reduce_effects", {
            "animations": False,
            "shadows": False,
            "blur": False,
        })
    
    async def _use_lighter_model(self) -> None:
        """Switch to a lighter AI model."""
        from src.ai.manager import AIManager
        manager = AIManager()
        
        # Switch to smaller/faster model
        await manager.load_model("fast-highlight-detector")
```

---

## 🤖 MCP (Model Context Protocol) API

```python
# src/api/mcp.py

"""
Model Context Protocol (MCP) - AI-kontrollü API.
Bu API, AI asistanlarının ClipShot'ı doğrudan kontrol etmesini sağlar.

MCP Specification: https://modelcontextprotocol.io/
"""

from typing import Dict, List, Any, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/mcp", tags=["mcp"])


# ============================================================================
# MCP PROTOCOL TYPES
# ============================================================================

class MCPTool(BaseModel):
    """MCP Tool definition."""
    name: str = Field(..., description="Unique tool identifier")
    description: str = Field(..., description="What this tool does")
    inputSchema: Dict[str, Any] = Field(..., description="JSON Schema for inputs")


class MCPResource(BaseModel):
    """MCP Resource definition."""
    uri: str = Field(..., description="Resource URI")
    name: str = Field(..., description="Human-readable name")
    description: str = Field(..., description="Resource description")
    mimeType: Optional[str] = Field(None, description="Content MIME type")


class MCPToolCall(BaseModel):
    """MCP Tool call request."""
    name: str
    arguments: Dict[str, Any]


class MCPToolResult(BaseModel):
    """MCP Tool call result."""
    content: List[Dict[str, Any]]
    isError: bool = False


# ============================================================================
# MCP TOOLS REGISTRY
# ============================================================================

MCP_TOOLS: List[MCPTool] = [
    # Capture Tools
    MCPTool(
        name="clipshot.capture.start",
        description="Start screen/game capture",
        inputSchema={
            "type": "object",
            "properties": {
                "source": {"type": "string", "enum": ["screen", "window", "game"]},
                "window_title": {"type": "string", "description": "Window title (for window capture)"},
            },
            "required": ["source"],
        },
    ),
    MCPTool(
        name="clipshot.capture.stop",
        description="Stop current capture",
        inputSchema={"type": "object", "properties": {}},
    ),
    MCPTool(
        name="clipshot.capture.status",
        description="Get current capture status",
        inputSchema={"type": "object", "properties": {}},
    ),
    
    # Clip Tools
    MCPTool(
        name="clipshot.clip.create",
        description="Create a clip from the last N seconds",
        inputSchema={
            "type": "object",
            "properties": {
                "duration_seconds": {"type": "number", "minimum": 5, "maximum": 300},
                "title": {"type": "string"},
                "tags": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["duration_seconds"],
        },
    ),
    MCPTool(
        name="clipshot.clip.list",
        description="List saved clips",
        inputSchema={
            "type": "object",
            "properties": {
                "limit": {"type": "number", "default": 10},
                "game": {"type": "string"},
            },
        },
    ),
    MCPTool(
        name="clipshot.clip.delete",
        description="Delete a clip",
        inputSchema={
            "type": "object",
            "properties": {
                "clip_id": {"type": "string"},
            },
            "required": ["clip_id"],
        },
    ),
    
    # AI Tools
    MCPTool(
        name="clipshot.ai.analyze",
        description="Analyze a clip with AI to detect highlights",
        inputSchema={
            "type": "object",
            "properties": {
                "clip_id": {"type": "string"},
                "analysis_type": {
                    "type": "string",
                    "enum": ["highlights", "metadata", "transcribe"],
                },
            },
            "required": ["clip_id", "analysis_type"],
        },
    ),
    MCPTool(
        name="clipshot.ai.generate_metadata",
        description="Generate title, description, tags for a clip",
        inputSchema={
            "type": "object",
            "properties": {
                "clip_id": {"type": "string"},
                "language": {"type": "string", "default": "en"},
            },
            "required": ["clip_id"],
        },
    ),
    
    # Settings Tools
    MCPTool(
        name="clipshot.settings.get",
        description="Get current settings",
        inputSchema={
            "type": "object",
            "properties": {
                "category": {"type": "string", "enum": ["capture", "ai", "ui", "plugins"]},
            },
        },
    ),
    MCPTool(
        name="clipshot.settings.update",
        description="Update settings",
        inputSchema={
            "type": "object",
            "properties": {
                "category": {"type": "string"},
                "settings": {"type": "object"},
            },
            "required": ["category", "settings"],
        },
    ),
    
    # Plugin Tools
    MCPTool(
        name="clipshot.plugins.list",
        description="List installed plugins",
        inputSchema={"type": "object", "properties": {}},
    ),
    MCPTool(
        name="clipshot.plugins.enable",
        description="Enable a plugin",
        inputSchema={
            "type": "object",
            "properties": {
                "plugin_id": {"type": "string"},
            },
            "required": ["plugin_id"],
        },
    ),
    MCPTool(
        name="clipshot.plugins.disable",
        description="Disable a plugin",
        inputSchema={
            "type": "object",
            "properties": {
                "plugin_id": {"type": "string"},
            },
            "required": ["plugin_id"],
        },
    ),
    
    # Export Tools
    MCPTool(
        name="clipshot.export.start",
        description="Export a clip to a specific format/platform",
        inputSchema={
            "type": "object",
            "properties": {
                "clip_id": {"type": "string"},
                "format": {"type": "string", "enum": ["mp4", "webm", "gif"]},
                "quality": {"type": "string", "enum": ["high", "medium", "low"]},
                "platform": {"type": "string", "enum": ["youtube", "twitter", "discord", "local"]},
            },
            "required": ["clip_id", "format"],
        },
    ),
]


MCP_RESOURCES: List[MCPResource] = [
    MCPResource(
        uri="clipshot://clips",
        name="Clips",
        description="All saved video clips",
        mimeType="application/json",
    ),
    MCPResource(
        uri="clipshot://settings",
        name="Settings",
        description="Application settings",
        mimeType="application/json",
    ),
    MCPResource(
        uri="clipshot://plugins",
        name="Plugins",
        description="Installed plugins",
        mimeType="application/json",
    ),
    MCPResource(
        uri="clipshot://status",
        name="Status",
        description="Current capture and system status",
        mimeType="application/json",
    ),
]


# ============================================================================
# MCP ENDPOINTS
# ============================================================================

@router.get("/tools")
async def list_tools() -> List[MCPTool]:
    """List all available MCP tools."""
    return MCP_TOOLS


@router.get("/resources")
async def list_resources() -> List[MCPResource]:
    """List all available MCP resources."""
    return MCP_RESOURCES


@router.post("/tools/call")
async def call_tool(call: MCPToolCall) -> MCPToolResult:
    """Execute an MCP tool call."""
    handler = TOOL_HANDLERS.get(call.name)
    if not handler:
        raise HTTPException(status_code=404, detail=f"Tool not found: {call.name}")
    
    try:
        result = await handler(call.arguments)
        return MCPToolResult(
            content=[{"type": "text", "text": str(result)}],
            isError=False,
        )
    except Exception as e:
        return MCPToolResult(
            content=[{"type": "text", "text": f"Error: {str(e)}"}],
            isError=True,
        )


@router.get("/resources/{resource_uri:path}")
async def read_resource(resource_uri: str) -> Dict[str, Any]:
    """Read an MCP resource."""
    handler = RESOURCE_HANDLERS.get(resource_uri)
    if not handler:
        raise HTTPException(status_code=404, detail=f"Resource not found: {resource_uri}")
    
    return await handler()


# ============================================================================
# TOOL HANDLERS
# ============================================================================

async def handle_capture_start(args: Dict[str, Any]) -> str:
    """Start capture."""
    from src.capture.manager import CaptureManager
    manager = CaptureManager()
    
    source = args.get("source", "screen")
    window_title = args.get("window_title")
    
    await manager.start(source=source, window_title=window_title)
    return f"Capture started: {source}"


async def handle_capture_stop(args: Dict[str, Any]) -> str:
    """Stop capture."""
    from src.capture.manager import CaptureManager
    manager = CaptureManager()
    await manager.stop()
    return "Capture stopped"


async def handle_capture_status(args: Dict[str, Any]) -> Dict[str, Any]:
    """Get capture status."""
    from src.capture.manager import CaptureManager
    manager = CaptureManager()
    return await manager.get_status()


async def handle_clip_create(args: Dict[str, Any]) -> Dict[str, Any]:
    """Create a clip."""
    from src.clips.manager import ClipManager
    manager = ClipManager()
    
    clip = await manager.create_clip(
        duration_seconds=args["duration_seconds"],
        title=args.get("title"),
        tags=args.get("tags", []),
    )
    
    return {"clip_id": clip.id, "path": str(clip.path)}


async def handle_clip_list(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """List clips."""
    from src.clips.manager import ClipManager
    manager = ClipManager()
    
    clips = await manager.list_clips(
        limit=args.get("limit", 10),
        game=args.get("game"),
    )
    
    return [c.to_dict() for c in clips]


async def handle_ai_analyze(args: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze clip with AI."""
    from src.ai.manager import AIManager
    manager = AIManager()
    
    result = await manager.analyze(
        clip_id=args["clip_id"],
        analysis_type=args["analysis_type"],
    )
    
    return result


async def handle_ai_generate_metadata(args: Dict[str, Any]) -> Dict[str, Any]:
    """Generate metadata with AI."""
    from src.ai.manager import AIManager
    manager = AIManager()
    
    metadata = await manager.generate_metadata(
        clip_id=args["clip_id"],
        language=args.get("language", "en"),
    )
    
    return metadata


async def handle_settings_get(args: Dict[str, Any]) -> Dict[str, Any]:
    """Get settings."""
    from src.core.config import config_manager
    
    category = args.get("category")
    if category:
        return config_manager.get_category(category)
    return config_manager.get_all()


async def handle_settings_update(args: Dict[str, Any]) -> str:
    """Update settings."""
    from src.core.config import config_manager
    
    category = args["category"]
    settings = args["settings"]
    
    await config_manager.update(category, settings)
    return f"Settings updated: {category}"


async def handle_plugins_list(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """List plugins."""
    from src.plugins.manager import PluginManager
    manager = PluginManager()
    
    plugins = await manager.list_installed()
    return [p.to_dict() for p in plugins]


async def handle_plugins_enable(args: Dict[str, Any]) -> str:
    """Enable plugin."""
    from src.plugins.manager import PluginManager
    manager = PluginManager()
    
    await manager.enable(args["plugin_id"])
    return f"Plugin enabled: {args['plugin_id']}"


async def handle_plugins_disable(args: Dict[str, Any]) -> str:
    """Disable plugin."""
    from src.plugins.manager import PluginManager
    manager = PluginManager()
    
    await manager.disable(args["plugin_id"])
    return f"Plugin disabled: {args['plugin_id']}"


async def handle_export_start(args: Dict[str, Any]) -> Dict[str, Any]:
    """Start export."""
    from src.export.manager import ExportManager
    manager = ExportManager()
    
    job = await manager.start_export(
        clip_id=args["clip_id"],
        format=args["format"],
        quality=args.get("quality", "high"),
        platform=args.get("platform", "local"),
    )
    
    return {"job_id": job.id, "status": job.status}


# Tool handlers registry
TOOL_HANDLERS = {
    "clipshot.capture.start": handle_capture_start,
    "clipshot.capture.stop": handle_capture_stop,
    "clipshot.capture.status": handle_capture_status,
    "clipshot.clip.create": handle_clip_create,
    "clipshot.clip.list": handle_clip_list,
    "clipshot.ai.analyze": handle_ai_analyze,
    "clipshot.ai.generate_metadata": handle_ai_generate_metadata,
    "clipshot.settings.get": handle_settings_get,
    "clipshot.settings.update": handle_settings_update,
    "clipshot.plugins.list": handle_plugins_list,
    "clipshot.plugins.enable": handle_plugins_enable,
    "clipshot.plugins.disable": handle_plugins_disable,
    "clipshot.export.start": handle_export_start,
}


# Resource handlers registry
async def get_clips_resource() -> Dict[str, Any]:
    from src.clips.manager import ClipManager
    manager = ClipManager()
    clips = await manager.list_clips(limit=50)
    return {"clips": [c.to_dict() for c in clips]}


async def get_settings_resource() -> Dict[str, Any]:
    from src.core.config import config_manager
    return config_manager.get_all()


async def get_plugins_resource() -> Dict[str, Any]:
    from src.plugins.manager import PluginManager
    manager = PluginManager()
    plugins = await manager.list_installed()
    return {"plugins": [p.to_dict() for p in plugins]}


async def get_status_resource() -> Dict[str, Any]:
    from src.capture.manager import CaptureManager
    from src.core.metrics import metrics
    
    capture_manager = CaptureManager()
    
    return {
        "capture": await capture_manager.get_status(),
        "metrics": {
            "cpu": metrics.get_stats("app.cpu.percent"),
            "memory": metrics.get_stats("app.memory.mb"),
        },
    }


RESOURCE_HANDLERS = {
    "clipshot://clips": get_clips_resource,
    "clipshot://settings": get_settings_resource,
    "clipshot://plugins": get_plugins_resource,
    "clipshot://status": get_status_resource,
}
```

---

## 🎮 FRONTEND PERFORMANCE

```typescript
// apps/desktop/src/performance/index.ts

/**
 * Frontend performance utilities.
 */

import { useEffect, useRef, useCallback } from 'react';

// ============================================================================
// FRAME TIME MONITORING
// ============================================================================

class FrameTimeMonitor {
  private samples: number[] = [];
  private lastFrameTime = 0;
  private running = false;
  private rafId: number | null = null;
  
  start() {
    if (this.running) return;
    this.running = true;
    this.lastFrameTime = performance.now();
    this.tick();
  }
  
  stop() {
    this.running = false;
    if (this.rafId) {
      cancelAnimationFrame(this.rafId);
    }
  }
  
  private tick = () => {
    if (!this.running) return;
    
    const now = performance.now();
    const frameTime = now - this.lastFrameTime;
    this.lastFrameTime = now;
    
    // Store last 60 samples
    this.samples.push(frameTime);
    if (this.samples.length > 60) {
      this.samples.shift();
    }
    
    // Report to main process every second
    if (this.samples.length === 60) {
      this.report();
    }
    
    this.rafId = requestAnimationFrame(this.tick);
  };
  
  private report() {
    const avg = this.samples.reduce((a, b) => a + b, 0) / this.samples.length;
    const max = Math.max(...this.samples);
    
    window.clipshot.metrics.record('ui.frame_time_ms', avg);
    window.clipshot.metrics.record('ui.frame_time_max_ms', max);
    
    // Warn if performance is bad
    if (avg > 33) {
      console.warn(`Low FPS: ${(1000 / avg).toFixed(1)} fps (${avg.toFixed(1)}ms)`);
    }
  }
  
  getStats() {
    if (this.samples.length === 0) return null;
    
    const sorted = [...this.samples].sort((a, b) => a - b);
    const n = sorted.length;
    
    return {
      avg: this.samples.reduce((a, b) => a + b, 0) / n,
      min: sorted[0],
      max: sorted[n - 1],
      p50: sorted[Math.floor(n * 0.5)],
      p95: sorted[Math.floor(n * 0.95)],
      fps: 1000 / (this.samples.reduce((a, b) => a + b, 0) / n),
    };
  }
}

export const frameTimeMonitor = new FrameTimeMonitor();


// ============================================================================
// LAZY LOADING
// ============================================================================

/**
 * Lazy load a component with retry logic.
 */
export function lazyWithRetry<T extends React.ComponentType<any>>(
  importFn: () => Promise<{ default: T }>,
  retries = 3
): React.LazyExoticComponent<T> {
  return React.lazy(() =>
    importFn().catch((error) => {
      if (retries <= 0) throw error;
      return new Promise((resolve) => setTimeout(resolve, 1000))
        .then(() => lazyWithRetry(importFn, retries - 1));
    })
  );
}


// ============================================================================
// VIRTUALIZATION
// ============================================================================

interface VirtualListOptions {
  itemCount: number;
  itemHeight: number;
  containerHeight: number;
  overscan?: number;
}

export function useVirtualList(options: VirtualListOptions) {
  const { itemCount, itemHeight, containerHeight, overscan = 3 } = options;
  
  const [scrollTop, setScrollTop] = React.useState(0);
  
  const totalHeight = itemCount * itemHeight;
  
  const startIndex = Math.max(0, Math.floor(scrollTop / itemHeight) - overscan);
  const endIndex = Math.min(
    itemCount - 1,
    Math.ceil((scrollTop + containerHeight) / itemHeight) + overscan
  );
  
  const visibleItems = [];
  for (let i = startIndex; i <= endIndex; i++) {
    visibleItems.push({
      index: i,
      style: {
        position: 'absolute' as const,
        top: i * itemHeight,
        height: itemHeight,
        width: '100%',
      },
    });
  }
  
  const handleScroll = useCallback((e: React.UIEvent<HTMLDivElement>) => {
    setScrollTop(e.currentTarget.scrollTop);
  }, []);
  
  return {
    totalHeight,
    visibleItems,
    handleScroll,
    containerStyle: {
      height: containerHeight,
      overflow: 'auto' as const,
      position: 'relative' as const,
    },
    innerStyle: {
      height: totalHeight,
      position: 'relative' as const,
    },
  };
}


// ============================================================================
// DEBOUNCE & THROTTLE
// ============================================================================

export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = React.useState(value);
  
  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);
  
  return debouncedValue;
}

export function useThrottle<T>(value: T, interval: number): T {
  const [throttledValue, setThrottledValue] = React.useState(value);
  const lastUpdated = useRef(Date.now());
  
  useEffect(() => {
    const now = Date.now();
    
    if (now >= lastUpdated.current + interval) {
      lastUpdated.current = now;
      setThrottledValue(value);
    } else {
      const timer = setTimeout(() => {
        lastUpdated.current = Date.now();
        setThrottledValue(value);
      }, interval - (now - lastUpdated.current));
      
      return () => clearTimeout(timer);
    }
  }, [value, interval]);
  
  return throttledValue;
}


// ============================================================================
// MEMORY OPTIMIZATION
// ============================================================================

/**
 * Hook to release heavy resources when component unmounts.
 */
export function useCleanup(cleanup: () => void) {
  const cleanupRef = useRef(cleanup);
  cleanupRef.current = cleanup;
  
  useEffect(() => {
    return () => cleanupRef.current();
  }, []);
}

/**
 * Hook to track memory usage.
 */
export function useMemoryPressure(callback: () => void, threshold = 0.8) {
  useEffect(() => {
    // @ts-ignore - Non-standard API
    if (!performance.measureUserAgentSpecificMemory) return;
    
    const checkMemory = async () => {
      try {
        // @ts-ignore
        const result = await performance.measureUserAgentSpecificMemory();
        const usedMB = result.bytes / 1024 / 1024;
        
        // Estimate threshold (assume 4GB limit)
        if (usedMB > 4096 * threshold) {
          callback();
        }
      } catch {
        // API not available
      }
    };
    
    const interval = setInterval(checkMemory, 10000);
    return () => clearInterval(interval);
  }, [callback, threshold]);
}
```

---

## 📊 PERFORMANCE DASHBOARD

```typescript
// apps/desktop/src/pages/DevPanel/Performance.tsx

import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { Activity, Cpu, MemoryStick, Zap } from 'lucide-react';

export const PerformanceDashboard: React.FC = () => {
  const { data: metrics } = useQuery({
    queryKey: ['performance', 'metrics'],
    queryFn: () => window.clipshot.metrics.getAll(),
    refetchInterval: 1000, // Refresh every second
  });

  return (
    <div className="p-6 space-y-6">
      <h2 className="text-xl font-bold flex items-center gap-2">
        <Activity className="w-5 h-5" />
        Performance Monitor
      </h2>

      {/* Metrics Grid */}
      <div className="grid grid-cols-4 gap-4">
        <MetricCard
          icon={<Cpu className="w-5 h-5" />}
          label="CPU"
          value={`${metrics?.cpu?.avg?.toFixed(1)}%`}
          status={getStatus(metrics?.cpu?.avg, 50, 80)}
        />
        <MetricCard
          icon={<MemoryStick className="w-5 h-5" />}
          label="Memory"
          value={`${metrics?.memory?.avg?.toFixed(0)} MB`}
          status={getStatus(metrics?.memory?.avg, 512, 800)}
        />
        <MetricCard
          icon={<Zap className="w-5 h-5" />}
          label="Frame Time"
          value={`${metrics?.frameTime?.avg?.toFixed(1)} ms`}
          status={getStatus(metrics?.frameTime?.avg, 16, 33)}
        />
        <MetricCard
          icon={<Activity className="w-5 h-5" />}
          label="FPS"
          value={`${(1000 / (metrics?.frameTime?.avg || 16)).toFixed(0)}`}
          status={getStatus(60 - (1000 / (metrics?.frameTime?.avg || 16)), 0, 30)}
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-2 gap-6">
        <div className="bg-card rounded-lg p-4 border border-border">
          <h3 className="font-medium mb-4">CPU Usage</h3>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={metrics?.cpuHistory || []}>
              <XAxis dataKey="time" />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Line 
                type="monotone" 
                dataKey="value" 
                stroke="#3b82f6" 
                strokeWidth={2}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-card rounded-lg p-4 border border-border">
          <h3 className="font-medium mb-4">Memory Usage</h3>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={metrics?.memoryHistory || []}>
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Line 
                type="monotone" 
                dataKey="value" 
                stroke="#10b981" 
                strokeWidth={2}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

function getStatus(value: number | undefined, warn: number, error: number): 'good' | 'warn' | 'error' {
  if (!value) return 'good';
  if (value >= error) return 'error';
  if (value >= warn) return 'warn';
  return 'good';
}

interface MetricCardProps {
  icon: React.ReactNode;
  label: string;
  value: string;
  status: 'good' | 'warn' | 'error';
}

const MetricCard: React.FC<MetricCardProps> = ({ icon, label, value, status }) => {
  const statusColors = {
    good: 'text-green-500',
    warn: 'text-yellow-500',
    error: 'text-red-500',
  };

  return (
    <div className="bg-card rounded-lg p-4 border border-border">
      <div className="flex items-center justify-between mb-2">
        <span className="text-muted-foreground">{icon}</span>
        <span className={`w-2 h-2 rounded-full ${statusColors[status].replace('text-', 'bg-')}`} />
      </div>
      <div className={`text-2xl font-bold ${statusColors[status]}`}>{value}</div>
      <div className="text-sm text-muted-foreground">{label}</div>
    </div>
  );
};
```

---

## 🎯 Bu Mimarinin Avantajları

1. **Proactive Monitoring** — Sorunlar oluşmadan tespit
2. **Auto-Optimization** — Otomatik performans ayarları
3. **MCP Ready** — AI asistanları tarafından kontrol edilebilir
4. **Real-time Metrics** — Anlık performans görünürlüğü
5. **Threshold Alerts** — Kritik durumlar için uyarı
6. **Frame Time Focus** — 60fps hedefi takibi
