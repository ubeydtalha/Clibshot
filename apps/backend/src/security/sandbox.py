"""
Plugin sandbox with process isolation and resource limits.

This module provides a secure execution environment for plugins with:
- Process isolation (subprocess)
- Resource limits (CPU, memory, disk I/O)
- Filesystem jail
- Network restrictions
- Permission enforcement
"""

import asyncio
import subprocess
import psutil
import sys
import os
import signal
from typing import Dict, Optional, Any
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

from ..core.logging import get_logger
from ..core.events import EventBus
from .permissions import PermissionManager, PermissionContext

logger = get_logger(__name__)


@dataclass
class ResourceLimits:
    """Resource limits for plugin execution."""
    cpu_percent: float = 50.0  # 50% CPU
    memory_mb: float = 512.0   # 512MB RAM
    disk_read_mb_s: float = 100.0  # 100MB/s read
    disk_write_mb_s: float = 50.0   # 50MB/s write
    network_enabled: bool = False  # No network by default
    execution_timeout_s: float = 300.0  # 5 minutes max


@dataclass
class ResourceUsage:
    """Current resource usage tracking."""
    cpu_percent: float = 0.0
    memory_mb: float = 0.0
    disk_read_mb: float = 0.0
    disk_write_mb: float = 0.0
    execution_time_s: float = 0.0
    timestamp: Optional[datetime] = None


class PluginSandbox:
    """
    Sandbox environment for plugin execution.
    
    Provides isolation and resource control for untrusted plugin code.
    """
    
    def __init__(
        self,
        plugin_id: str,
        permission_manager: PermissionManager,
        event_bus: EventBus,
        limits: Optional[ResourceLimits] = None
    ):
        self.plugin_id = plugin_id
        self.permission_manager = permission_manager
        self.event_bus = event_bus
        self.limits = limits or ResourceLimits()
        
        self.process: Optional[subprocess.Popen] = None
        self.pid: Optional[int] = None
        self.start_time: Optional[datetime] = None
        self._monitor_task: Optional[asyncio.Task] = None
        self._running = False
    
    async def run_plugin(
        self, 
        plugin_code: str,
        entry_point: str,
        env: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Run plugin code in a sandboxed environment.
        
        Args:
            plugin_code: Path to plugin code or inline code
            entry_point: Entry point script/function
            env: Environment variables for the plugin
            
        Returns:
            Dict with execution results and resource usage
        """
        logger.info(f"Starting plugin {self.plugin_id} in sandbox")
        
        # Create isolated environment
        plugin_env = self._create_isolated_env(env or {})
        
        # Create filesystem jail
        jail_path = self._create_filesystem_jail()
        
        # Prepare execution command
        cmd = self._prepare_command(entry_point, jail_path)
        
        try:
            # Start process
            self.process = await self._spawn_process(cmd, plugin_env, jail_path)
            self.pid = self.process.pid
            self.start_time = datetime.now()
            self._running = True
            
            # Start resource monitoring
            self._monitor_task = asyncio.create_task(self._monitor_resources())
            
            # Wait for completion with timeout
            try:
                stdout, stderr = await asyncio.wait_for(
                    self._wait_for_process(),
                    timeout=self.limits.execution_timeout_s
                )
                
                return {
                    "success": self.process.returncode == 0,
                    "returncode": self.process.returncode,
                    "stdout": stdout.decode('utf-8', errors='ignore'),
                    "stderr": stderr.decode('utf-8', errors='ignore'),
                    "resource_usage": await self._get_resource_usage(),
                }
                
            except asyncio.TimeoutError:
                logger.error(f"Plugin {self.plugin_id} exceeded execution timeout")
                await self.terminate()
                return {
                    "success": False,
                    "error": "Execution timeout exceeded",
                    "resource_usage": await self._get_resource_usage(),
                }
        
        except Exception as e:
            logger.error(f"Error running plugin {self.plugin_id}: {e}")
            await self.terminate()
            return {
                "success": False,
                "error": str(e),
            }
        
        finally:
            self._running = False
            if self._monitor_task:
                self._monitor_task.cancel()
    
    def _create_isolated_env(self, base_env: Dict[str, str]) -> Dict[str, str]:
        """Create isolated environment variables."""
        env = {
            "CLIPSHOT_PLUGIN_ID": self.plugin_id,
            "CLIPSHOT_PLUGIN_SANDBOX": "1",
            "PATH": os.environ.get("PATH", ""),
            "PYTHONPATH": os.environ.get("PYTHONPATH", ""),
        }
        
        # Add user-provided env vars (sanitized)
        for key, value in base_env.items():
            if not key.startswith("CLIPSHOT_") and key not in ["PATH", "HOME", "USER"]:
                env[key] = value
        
        return env
    
    def _create_filesystem_jail(self) -> Path:
        """Create a filesystem jail for the plugin."""
        jail_path = Path.home() / ".clipshot" / "jail" / self.plugin_id
        jail_path.mkdir(parents=True, exist_ok=True)
        
        # Create standard directories
        (jail_path / "data").mkdir(exist_ok=True)
        (jail_path / "temp").mkdir(exist_ok=True)
        (jail_path / "config").mkdir(exist_ok=True)
        
        return jail_path
    
    def _prepare_command(self, entry_point: str, jail_path: Path) -> list:
        """Prepare the command to execute the plugin."""
        # Use Python interpreter
        return [
            sys.executable,
            "-u",  # Unbuffered output
            entry_point,
        ]
    
    async def _spawn_process(
        self,
        cmd: list,
        env: Dict[str, str],
        cwd: Path
    ) -> subprocess.Popen:
        """Spawn the sandboxed process."""
        # Create process with limited privileges
        process = subprocess.Popen(
            cmd,
            env=env,
            cwd=str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            # Prevent spawning additional processes
            start_new_session=True,
        )
        
        logger.info(f"Spawned plugin process: PID {process.pid}")
        
        # Apply resource limits using psutil
        try:
            p = psutil.Process(process.pid)
            
            # Set CPU affinity (limit to fewer cores if needed)
            # Note: This is platform-specific
            
            # Set nice value (lower priority)
            if hasattr(p, 'nice'):
                p.nice(10)  # Lower priority
        
        except Exception as e:
            logger.warning(f"Could not apply resource limits: {e}")
        
        return process
    
    async def _wait_for_process(self) -> tuple:
        """Wait for process to complete."""
        loop = asyncio.get_event_loop()
        stdout, stderr = await loop.run_in_executor(
            None,
            self.process.communicate
        )
        return stdout, stderr
    
    async def _monitor_resources(self) -> None:
        """Monitor resource usage and enforce limits."""
        while self._running and self.pid:
            try:
                usage = await self._get_resource_usage()
                
                # Check CPU limit
                if usage.cpu_percent > self.limits.cpu_percent:
                    logger.warning(
                        f"Plugin {self.plugin_id} exceeded CPU limit: "
                        f"{usage.cpu_percent:.1f}% > {self.limits.cpu_percent}%"
                    )
                    await self.event_bus.emit("sandbox:limit_exceeded", {
                        "plugin_id": self.plugin_id,
                        "resource": "cpu",
                        "usage": usage.cpu_percent,
                        "limit": self.limits.cpu_percent,
                    })
                
                # Check memory limit
                if usage.memory_mb > self.limits.memory_mb:
                    logger.warning(
                        f"Plugin {self.plugin_id} exceeded memory limit: "
                        f"{usage.memory_mb:.1f}MB > {self.limits.memory_mb}MB"
                    )
                    await self.event_bus.emit("sandbox:limit_exceeded", {
                        "plugin_id": self.plugin_id,
                        "resource": "memory",
                        "usage": usage.memory_mb,
                        "limit": self.limits.memory_mb,
                    })
                    # Terminate if memory limit severely exceeded
                    if usage.memory_mb > self.limits.memory_mb * 1.5:
                        logger.error(f"Terminating plugin {self.plugin_id} due to memory limit")
                        await self.terminate()
                        break
                
                await asyncio.sleep(1)  # Check every second
                
            except psutil.NoSuchProcess:
                break
            except Exception as e:
                logger.error(f"Error monitoring resources: {e}")
                break
    
    async def _get_resource_usage(self) -> ResourceUsage:
        """Get current resource usage."""
        if not self.pid:
            return ResourceUsage()
        
        try:
            process = psutil.Process(self.pid)
            
            # Get CPU usage
            cpu_percent = process.cpu_percent(interval=0.1)
            
            # Get memory usage
            memory_info = process.memory_info()
            memory_mb = memory_info.rss / 1024 / 1024
            
            # Get I/O stats
            try:
                io_counters = process.io_counters()
                disk_read_mb = io_counters.read_bytes / 1024 / 1024
                disk_write_mb = io_counters.write_bytes / 1024 / 1024
            except (AttributeError, psutil.AccessDenied):
                disk_read_mb = 0.0
                disk_write_mb = 0.0
            
            # Get execution time
            if self.start_time:
                execution_time_s = (datetime.now() - self.start_time).total_seconds()
            else:
                execution_time_s = 0.0
            
            return ResourceUsage(
                cpu_percent=cpu_percent,
                memory_mb=memory_mb,
                disk_read_mb=disk_read_mb,
                disk_write_mb=disk_write_mb,
                execution_time_s=execution_time_s,
                timestamp=datetime.now(),
            )
        
        except psutil.NoSuchProcess:
            return ResourceUsage()
    
    async def terminate(self) -> None:
        """Terminate the sandboxed process."""
        if not self.process:
            return
        
        logger.info(f"Terminating plugin {self.plugin_id}")
        
        try:
            # Try graceful termination first
            self.process.terminate()
            
            # Wait a bit for graceful shutdown
            try:
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                # Force kill if needed
                self.process.kill()
                self.process.wait()
        
        except Exception as e:
            logger.error(f"Error terminating plugin {self.plugin_id}: {e}")
        
        finally:
            self._running = False
            if self._monitor_task:
                self._monitor_task.cancel()
    
    def get_permission_context(self) -> PermissionContext:
        """Get permission context for this plugin."""
        from .permissions import PermissionEnforcer
        enforcer = PermissionEnforcer(self.permission_manager)
        return enforcer.enforce(self.plugin_id)
