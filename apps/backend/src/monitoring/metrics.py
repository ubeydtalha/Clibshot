"""
Performance metrics collection and monitoring.

Collects CPU, memory, GPU, and I/O metrics for performance analysis.
"""

import asyncio
import time
import psutil
import statistics
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque

from ..core.logging import get_logger
from ..core.events import EventBus

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
            p50=sorted_values[int(n * 0.5)] if n > 0 else 0,
            p95=sorted_values[int(n * 0.95)] if n > 1 else sorted_values[0],
            p99=sorted_values[int(n * 0.99)] if n > 1 else sorted_values[0],
            count=n,
            window_seconds=window_seconds,
        )
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """Get all current metrics."""
        metrics = {}
        for name in self.samples.keys():
            stats = self.get_stats(name, window_seconds=10)
            if stats:
                metrics[name] = {
                    "current": stats.avg,
                    "min": stats.min,
                    "max": stats.max,
                    "p95": stats.p95,
                }
        return metrics
    
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
        cpu_percent = psutil.cpu_percent(interval=0.1)
        self.record("system.cpu.percent", cpu_percent)
        
        # Memory
        memory = psutil.virtual_memory()
        self.record("system.memory.percent", memory.percent)
        self.record("system.memory.used_mb", memory.used / 1024 / 1024)
        self.record("system.memory.available_mb", memory.available / 1024 / 1024)
        
        # Disk I/O
        try:
            disk_io = psutil.disk_io_counters()
            if disk_io:
                self.record("system.disk.read_mb", disk_io.read_bytes / 1024 / 1024)
                self.record("system.disk.write_mb", disk_io.write_bytes / 1024 / 1024)
        except Exception:
            pass
        
        # Network I/O
        try:
            net_io = psutil.net_io_counters()
            if net_io:
                self.record("system.network.sent_mb", net_io.bytes_sent / 1024 / 1024)
                self.record("system.network.recv_mb", net_io.bytes_recv / 1024 / 1024)
        except Exception:
            pass
        
        # Process-specific
        try:
            process = psutil.Process()
            self.record("app.cpu.percent", process.cpu_percent())
            self.record("app.memory.mb", process.memory_info().rss / 1024 / 1024)
            self.record("app.threads", process.num_threads())
        except Exception:
            pass
    
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
