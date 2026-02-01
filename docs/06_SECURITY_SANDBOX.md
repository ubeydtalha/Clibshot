# 🛡️ SECURITY & SANDBOX — CLIPSHOT

> Plugin güvenlik modeli, sandbox katmanları, izin sistemi ve çakışma tespiti.

---

## 🎯 GÜVENLİK PRENSİPLERİ

1. **Zero Trust** — Hiçbir plugin güvenilir kabul edilmez
2. **Least Privilege** — Minimum gerekli izinler
3. **Defense in Depth** — Çoklu güvenlik katmanları
4. **Audit Everything** — Tüm erişimler loglanır
5. **Fail Secure** — Hata durumunda erişim engellenir

---

## 🏗️ SANDBOX MİMARİSİ

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIPSHOT CORE                            │
│                     (Trusted Component)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                  SANDBOX GATEWAY                          │   │
│  │              (Permission Enforcement)                     │   │
│  └────────────────────────┬─────────────────────────────────┘   │
│                           │                                      │
│  ┌────────────────────────┼─────────────────────────────────┐   │
│  │                    IPC LAYER                              │   │
│  │            (Structured Communication Only)                │   │
│  └────────────────────────┬─────────────────────────────────┘   │
│                           │                                      │
├───────────────────────────┼──────────────────────────────────────┤
│                           │                                      │
│  ┌─────────────┐  ┌───────┴───────┐  ┌─────────────┐            │
│  │  SANDBOX 1  │  │   SANDBOX 2   │  │  SANDBOX 3  │            │
│  │  Plugin A   │  │   Plugin B    │  │   Plugin C  │            │
│  │             │  │               │  │             │            │
│  │ ┌─────────┐ │  │ ┌───────────┐ │  │ ┌─────────┐ │            │
│  │ │ Process │ │  │ │  Process  │ │  │ │ Process │ │            │
│  │ │ Jail    │ │  │ │   Jail    │ │  │ │  Jail   │ │            │
│  │ └─────────┘ │  │ └───────────┘ │  │ └─────────┘ │            │
│  │ ┌─────────┐ │  │ ┌───────────┐ │  │ ┌─────────┐ │            │
│  │ │ FS Jail │ │  │ │  FS Jail  │ │  │ │ FS Jail │ │            │
│  │ └─────────┘ │  │ └───────────┘ │  │ └─────────┘ │            │
│  │ ┌─────────┐ │  │ ┌───────────┐ │  │ ┌─────────┐ │            │
│  │ │Resource │ │  │ │ Resource  │ │  │ │Resource │ │            │
│  │ │ Limits  │ │  │ │  Limits   │ │  │ │ Limits  │ │            │
│  │ └─────────┘ │  │ └───────────┘ │  │ └─────────┘ │            │
│  └─────────────┘  └───────────────┘  └─────────────┘            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔒 SANDBOX KATMANLARI

### Layer 1: Process Isolation

```python
# src/plugins/sandbox.py

import subprocess
import ctypes
from ctypes import wintypes
from typing import Optional
import win32job
import win32process
import win32security

class ProcessSandbox:
    """Windows process isolation using Job Objects and Restricted Tokens."""
    
    def __init__(self, plugin_id: str):
        self.plugin_id = plugin_id
        self.job_handle: Optional[int] = None
        self.process_handle: Optional[int] = None
    
    def create_sandbox(self) -> None:
        """Create sandboxed process environment."""
        # Create Job Object for resource limits
        self.job_handle = win32job.CreateJobObject(None, f"ClipShot_Plugin_{self.plugin_id}")
        
        # Set Job Object limits
        job_info = win32job.QueryInformationJobObject(
            self.job_handle, 
            win32job.JobObjectExtendedLimitInformation
        )
        
        # Limit process creation
        job_info['BasicLimitInformation']['LimitFlags'] |= (
            win32job.JOB_OBJECT_LIMIT_ACTIVE_PROCESS |
            win32job.JOB_OBJECT_LIMIT_DIE_ON_UNHANDLED_EXCEPTION |
            win32job.JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        )
        job_info['BasicLimitInformation']['ActiveProcessLimit'] = 1
        
        win32job.SetInformationJobObject(
            self.job_handle,
            win32job.JobObjectExtendedLimitInformation,
            job_info
        )
    
    def create_restricted_token(self) -> int:
        """Create a restricted security token."""
        # Get current token
        current_token = win32security.OpenProcessToken(
            win32process.GetCurrentProcess(),
            win32security.TOKEN_ALL_ACCESS
        )
        
        # Create restricted token
        # Remove dangerous privileges
        disabled_sids = []
        delete_privileges = [
            win32security.LookupPrivilegeValue(None, "SeDebugPrivilege"),
            win32security.LookupPrivilegeValue(None, "SeTakeOwnershipPrivilege"),
            win32security.LookupPrivilegeValue(None, "SeLoadDriverPrivilege"),
            win32security.LookupPrivilegeValue(None, "SeBackupPrivilege"),
            win32security.LookupPrivilegeValue(None, "SeRestorePrivilege"),
        ]
        
        restricted_token = win32security.CreateRestrictedToken(
            current_token,
            win32security.DISABLE_MAX_PRIVILEGE,
            disabled_sids,
            delete_privileges,
            []
        )
        
        return restricted_token
    
    async def spawn_plugin_process(
        self, 
        entry_script: str,
        env: dict
    ) -> subprocess.Popen:
        """Spawn a sandboxed plugin process."""
        # Create restricted token
        token = self.create_restricted_token()
        
        # Create process with restricted token
        startup_info = subprocess.STARTUPINFO()
        startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startup_info.wShowWindow = subprocess.SW_HIDE
        
        process = subprocess.Popen(
            ["python", entry_script],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            creationflags=subprocess.CREATE_SUSPENDED,
            startupinfo=startup_info,
        )
        
        # Assign to job object
        win32job.AssignProcessToJobObject(self.job_handle, process._handle)
        
        # Resume process
        win32process.ResumeThread(process._handle)
        
        self.process_handle = process
        return process
    
    def terminate(self) -> None:
        """Terminate sandboxed process."""
        if self.process_handle:
            self.process_handle.terminate()
        if self.job_handle:
            win32job.TerminateJobObject(self.job_handle, 1)
```

### Layer 2: Permission Gate

```python
# src/plugins/permissions.py

from enum import Enum
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field
from pathlib import Path
import json

from src.core.logging import get_logger
from src.db.session import get_session

logger = get_logger(__name__)


class PermissionLevel(str, Enum):
    NONE = "none"
    LIMITED = "limited"
    OPTIONAL = "optional"
    REQUIRED = "required"


class PermissionCategory(str, Enum):
    SCREEN = "screen"
    MICROPHONE = "microphone"
    FILESYSTEM = "filesystem"
    NETWORK = "network"
    GPU = "gpu"
    SYSTEM = "system"
    CLIPBOARD = "clipboard"
    NOTIFICATIONS = "notifications"


@dataclass
class PermissionGrant:
    """Represents a granted permission."""
    category: PermissionCategory
    level: PermissionLevel
    granted: bool = False
    granted_at: Optional[str] = None
    granted_by: str = "user"
    
    # Category-specific restrictions
    paths: List[str] = field(default_factory=list)      # filesystem
    hosts: List[str] = field(default_factory=list)      # network
    apis: List[str] = field(default_factory=list)       # system
    operations: List[str] = field(default_factory=list) # filesystem


class PermissionManager:
    """Manages plugin permissions."""
    
    # Path aliases
    PATH_ALIASES = {
        "$PLUGIN_DATA": lambda pid: Path.home() / ".clipshot" / "plugins" / pid / "data",
        "$CLIPS": lambda pid: Path.home() / ".clipshot" / "clips",
        "$TEMP": lambda pid: Path.home() / ".clipshot" / "temp" / pid,
        "$CONFIG": lambda pid: Path.home() / ".clipshot" / "config",
    }
    
    def __init__(self):
        self.grants: Dict[str, Dict[PermissionCategory, PermissionGrant]] = {}
    
    async def load_grants(self, plugin_id: str) -> Dict[PermissionCategory, PermissionGrant]:
        """Load granted permissions from database."""
        async with get_session() as session:
            # Load from database
            grants = await session.execute(
                "SELECT * FROM plugin_permissions WHERE plugin_id = ?",
                (plugin_id,)
            )
            
            result = {}
            for row in grants:
                category = PermissionCategory(row["category"])
                result[category] = PermissionGrant(
                    category=category,
                    level=PermissionLevel(row["level"]),
                    granted=row["granted"],
                    granted_at=row["granted_at"],
                    paths=json.loads(row["paths"] or "[]"),
                    hosts=json.loads(row["hosts"] or "[]"),
                    apis=json.loads(row["apis"] or "[]"),
                )
            
            self.grants[plugin_id] = result
            return result
    
    async def save_grants(
        self, 
        plugin_id: str, 
        grants: Dict[PermissionCategory, PermissionGrant]
    ) -> None:
        """Save permission grants to database."""
        async with get_session() as session:
            for category, grant in grants.items():
                await session.execute("""
                    INSERT OR REPLACE INTO plugin_permissions 
                    (plugin_id, category, level, granted, granted_at, paths, hosts, apis)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    plugin_id,
                    category.value,
                    grant.level.value,
                    grant.granted,
                    grant.granted_at,
                    json.dumps(grant.paths),
                    json.dumps(grant.hosts),
                    json.dumps(grant.apis),
                ))
            await session.commit()
        
        self.grants[plugin_id] = grants
    
    def check_permission(
        self, 
        plugin_id: str, 
        category: PermissionCategory,
        resource: Optional[str] = None
    ) -> bool:
        """Check if plugin has permission for a resource."""
        grants = self.grants.get(plugin_id, {})
        grant = grants.get(category)
        
        if not grant or not grant.granted:
            self._log_denied(plugin_id, category, resource)
            return False
        
        # Check resource-specific restrictions
        if category == PermissionCategory.FILESYSTEM and resource:
            return self._check_filesystem_access(plugin_id, grant, resource)
        
        if category == PermissionCategory.NETWORK and resource:
            return self._check_network_access(grant, resource)
        
        if category == PermissionCategory.SYSTEM and resource:
            return self._check_system_access(grant, resource)
        
        return True
    
    def _check_filesystem_access(
        self, 
        plugin_id: str,
        grant: PermissionGrant, 
        path: str
    ) -> bool:
        """Check if plugin can access a filesystem path."""
        path = Path(path).resolve()
        
        for allowed_pattern in grant.paths:
            # Resolve aliases
            if allowed_pattern.startswith("$"):
                alias_func = self.PATH_ALIASES.get(allowed_pattern)
                if alias_func:
                    allowed_path = alias_func(plugin_id)
                    if path == allowed_path or allowed_path in path.parents:
                        return True
            else:
                allowed_path = Path(allowed_pattern).resolve()
                if path == allowed_path or allowed_path in path.parents:
                    return True
        
        return False
    
    def _check_network_access(self, grant: PermissionGrant, host: str) -> bool:
        """Check if plugin can access a network host."""
        import fnmatch
        
        for pattern in grant.hosts:
            if fnmatch.fnmatch(host, pattern):
                return True
        
        return False
    
    def _check_system_access(self, grant: PermissionGrant, api: str) -> bool:
        """Check if plugin can use a system API."""
        return api in grant.apis
    
    def _log_denied(
        self, 
        plugin_id: str, 
        category: PermissionCategory, 
        resource: Optional[str]
    ) -> None:
        """Log permission denial for audit."""
        logger.warning(
            f"Permission denied: plugin={plugin_id} category={category.value} resource={resource}"
        )


class PermissionEnforcer:
    """Runtime permission enforcement."""
    
    def __init__(self, manager: PermissionManager):
        self.manager = manager
    
    def enforce(self, plugin_id: str):
        """Create a permission enforcement context."""
        return PermissionContext(plugin_id, self.manager)


class PermissionContext:
    """Context manager for permission enforcement."""
    
    def __init__(self, plugin_id: str, manager: PermissionManager):
        self.plugin_id = plugin_id
        self.manager = manager
    
    def require_screen(self) -> bool:
        return self.manager.check_permission(self.plugin_id, PermissionCategory.SCREEN)
    
    def require_microphone(self) -> bool:
        return self.manager.check_permission(self.plugin_id, PermissionCategory.MICROPHONE)
    
    def require_filesystem(self, path: str, operation: str = "read") -> bool:
        return self.manager.check_permission(
            self.plugin_id, 
            PermissionCategory.FILESYSTEM, 
            path
        )
    
    def require_network(self, host: str) -> bool:
        return self.manager.check_permission(
            self.plugin_id, 
            PermissionCategory.NETWORK, 
            host
        )
    
    def require_gpu(self) -> bool:
        return self.manager.check_permission(self.plugin_id, PermissionCategory.GPU)
    
    def require_system(self, api: str) -> bool:
        return self.manager.check_permission(
            self.plugin_id, 
            PermissionCategory.SYSTEM, 
            api
        )
```

### Layer 3: Resource Control

```python
# src/plugins/watchdog.py

import asyncio
import psutil
from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime

from src.core.logging import get_logger
from src.core.events import EventBus

logger = get_logger(__name__)


@dataclass
class ResourceLimits:
    """Resource limits for a plugin."""
    cpu_percent: float = 20.0
    memory_mb: float = 512.0
    gpu_percent: float = 30.0
    io_read_mb_s: float = 100.0
    io_write_mb_s: float = 50.0


@dataclass
class ResourceUsage:
    """Current resource usage for a plugin."""
    cpu_percent: float = 0.0
    memory_mb: float = 0.0
    gpu_percent: float = 0.0
    io_read_bytes: int = 0
    io_write_bytes: int = 0
    timestamp: datetime = None


class PluginWatchdog:
    """Monitors and limits plugin resource usage."""
    
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.plugins: Dict[str, PluginMonitor] = {}
        self.running = False
        self._task: Optional[asyncio.Task] = None
    
    async def start(self) -> None:
        """Start the watchdog."""
        self.running = True
        self._task = asyncio.create_task(self._monitor_loop())
        logger.info("Plugin watchdog started")
    
    async def stop(self) -> None:
        """Stop the watchdog."""
        self.running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Plugin watchdog stopped")
    
    def register_plugin(
        self, 
        plugin_id: str, 
        pid: int, 
        limits: ResourceLimits
    ) -> None:
        """Register a plugin for monitoring."""
        self.plugins[plugin_id] = PluginMonitor(plugin_id, pid, limits)
        logger.info(f"Registered plugin for monitoring: {plugin_id} (PID: {pid})")
    
    def unregister_plugin(self, plugin_id: str) -> None:
        """Unregister a plugin from monitoring."""
        if plugin_id in self.plugins:
            del self.plugins[plugin_id]
            logger.info(f"Unregistered plugin: {plugin_id}")
    
    async def _monitor_loop(self) -> None:
        """Main monitoring loop."""
        while self.running:
            for plugin_id, monitor in list(self.plugins.items()):
                try:
                    usage = await monitor.get_usage()
                    violations = monitor.check_limits(usage)
                    
                    if violations:
                        await self._handle_violations(plugin_id, violations, usage)
                    
                except psutil.NoSuchProcess:
                    # Plugin process died
                    await self.event_bus.emit("plugin:crashed", {"plugin_id": plugin_id})
                    self.unregister_plugin(plugin_id)
                    
                except Exception as e:
                    logger.error(f"Error monitoring plugin {plugin_id}: {e}")
            
            await asyncio.sleep(1)  # Check every second
    
    async def _handle_violations(
        self, 
        plugin_id: str, 
        violations: Dict[str, float],
        usage: ResourceUsage
    ) -> None:
        """Handle resource limit violations."""
        monitor = self.plugins.get(plugin_id)
        if not monitor:
            return
        
        monitor.violation_count += 1
        
        # Emit warning event
        await self.event_bus.emit("plugin:resource_warning", {
            "plugin_id": plugin_id,
            "violations": violations,
            "usage": usage.__dict__,
            "violation_count": monitor.violation_count,
        })
        
        # Throttle after 3 warnings
        if monitor.violation_count >= 3 and not monitor.throttled:
            await self._throttle_plugin(plugin_id)
        
        # Kill after 10 violations
        if monitor.violation_count >= 10:
            await self._kill_plugin(plugin_id)
    
    async def _throttle_plugin(self, plugin_id: str) -> None:
        """Throttle a misbehaving plugin."""
        monitor = self.plugins.get(plugin_id)
        if not monitor:
            return
        
        logger.warning(f"Throttling plugin: {plugin_id}")
        monitor.throttled = True
        
        # Reduce process priority
        try:
            process = psutil.Process(monitor.pid)
            process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
        except Exception as e:
            logger.error(f"Failed to throttle plugin {plugin_id}: {e}")
        
        await self.event_bus.emit("plugin:throttled", {"plugin_id": plugin_id})
    
    async def _kill_plugin(self, plugin_id: str) -> None:
        """Kill a plugin that exceeded limits too many times."""
        monitor = self.plugins.get(plugin_id)
        if not monitor:
            return
        
        logger.error(f"Killing plugin due to resource abuse: {plugin_id}")
        
        try:
            process = psutil.Process(monitor.pid)
            process.terminate()
            await asyncio.sleep(1)
            if process.is_running():
                process.kill()
        except Exception as e:
            logger.error(f"Failed to kill plugin {plugin_id}: {e}")
        
        await self.event_bus.emit("plugin:killed", {
            "plugin_id": plugin_id,
            "reason": "resource_abuse",
        })
        
        self.unregister_plugin(plugin_id)


class PluginMonitor:
    """Monitor for a single plugin."""
    
    def __init__(self, plugin_id: str, pid: int, limits: ResourceLimits):
        self.plugin_id = plugin_id
        self.pid = pid
        self.limits = limits
        self.violation_count = 0
        self.throttled = False
        self._process: Optional[psutil.Process] = None
    
    @property
    def process(self) -> psutil.Process:
        if not self._process:
            self._process = psutil.Process(self.pid)
        return self._process
    
    async def get_usage(self) -> ResourceUsage:
        """Get current resource usage."""
        loop = asyncio.get_event_loop()
        
        def _get():
            cpu = self.process.cpu_percent()
            memory = self.process.memory_info().rss / 1024 / 1024
            io = self.process.io_counters()
            
            return ResourceUsage(
                cpu_percent=cpu,
                memory_mb=memory,
                gpu_percent=0,  # TODO: GPU monitoring
                io_read_bytes=io.read_bytes,
                io_write_bytes=io.write_bytes,
                timestamp=datetime.now(),
            )
        
        return await loop.run_in_executor(None, _get)
    
    def check_limits(self, usage: ResourceUsage) -> Dict[str, float]:
        """Check if usage exceeds limits. Returns violations."""
        violations = {}
        
        if usage.cpu_percent > self.limits.cpu_percent:
            violations["cpu"] = usage.cpu_percent
        
        if usage.memory_mb > self.limits.memory_mb:
            violations["memory"] = usage.memory_mb
        
        if usage.gpu_percent > self.limits.gpu_percent:
            violations["gpu"] = usage.gpu_percent
        
        return violations
```

### Layer 4: Filesystem Jail

```python
# src/plugins/filesystem_jail.py

import os
from pathlib import Path
from typing import Optional, Set
from contextlib import contextmanager

from src.core.logging import get_logger

logger = get_logger(__name__)


class FilesystemJail:
    """Restricts filesystem access to allowed paths only."""
    
    def __init__(self, plugin_id: str, allowed_paths: Set[Path]):
        self.plugin_id = plugin_id
        self.allowed_paths = {p.resolve() for p in allowed_paths}
        self.base_path = Path.home() / ".clipshot" / "plugins" / plugin_id
        
        # Always allow plugin's own directory
        self.allowed_paths.add(self.base_path.resolve())
    
    def is_allowed(self, path: str) -> bool:
        """Check if a path is allowed."""
        target = Path(path).resolve()
        
        # Check if path is within allowed paths
        for allowed in self.allowed_paths:
            try:
                target.relative_to(allowed)
                return True
            except ValueError:
                continue
        
        return False
    
    def resolve_path(self, path: str) -> Optional[Path]:
        """Resolve a path within the jail."""
        if not self.is_allowed(path):
            logger.warning(f"Filesystem access denied: {path} for plugin {self.plugin_id}")
            return None
        
        return Path(path).resolve()
    
    def open(self, path: str, mode: str = "r"):
        """Safely open a file within the jail."""
        resolved = self.resolve_path(path)
        if not resolved:
            raise PermissionError(f"Access denied: {path}")
        
        # Check mode restrictions
        if "w" in mode or "a" in mode:
            # Only allow writing to plugin data directory
            try:
                resolved.relative_to(self.base_path / "data")
            except ValueError:
                # Not in data directory, check if in temp
                try:
                    resolved.relative_to(Path.home() / ".clipshot" / "temp" / self.plugin_id)
                except ValueError:
                    raise PermissionError(f"Write access denied: {path}")
        
        return open(resolved, mode)
    
    def mkdir(self, path: str, parents: bool = False) -> None:
        """Create a directory within the jail."""
        resolved = self.resolve_path(path)
        if not resolved:
            raise PermissionError(f"Access denied: {path}")
        
        # Only allow in data directory
        try:
            resolved.relative_to(self.base_path / "data")
        except ValueError:
            raise PermissionError(f"Cannot create directory outside data: {path}")
        
        resolved.mkdir(parents=parents, exist_ok=True)
    
    def exists(self, path: str) -> bool:
        """Check if a path exists within the jail."""
        resolved = self.resolve_path(path)
        if not resolved:
            return False
        return resolved.exists()
    
    def listdir(self, path: str) -> list:
        """List directory contents within the jail."""
        resolved = self.resolve_path(path)
        if not resolved:
            raise PermissionError(f"Access denied: {path}")
        return os.listdir(resolved)
```

---

## 🔄 CONFLICT DETECTION

```python
# src/plugins/conflict.py

from typing import Dict, List, Set, Optional
from dataclasses import dataclass
from enum import Enum

from src.core.logging import get_logger

logger = get_logger(__name__)


class ConflictType(str, Enum):
    API_CONFLICT = "api_conflict"           # Same API provided by multiple plugins
    RESOURCE_CONFLICT = "resource_conflict"  # Same resource used exclusively
    EXPLICIT_CONFLICT = "explicit_conflict"  # Declared in manifest
    VERSION_CONFLICT = "version_conflict"    # Incompatible versions


class ConflictSeverity(str, Enum):
    WARNING = "warning"   # Can coexist but may cause issues
    ERROR = "error"       # Cannot coexist


@dataclass
class Conflict:
    """Represents a conflict between plugins."""
    type: ConflictType
    severity: ConflictSeverity
    plugin_a: str
    plugin_b: str
    resource: str  # The conflicting API, resource, etc.
    message: str
    resolution: List[str]  # Suggested resolutions


class ConflictDetector:
    """Detects conflicts between plugins."""
    
    def __init__(self):
        self.installed_plugins: Dict[str, dict] = {}  # id -> manifest
        self.api_providers: Dict[str, str] = {}  # api -> plugin_id
    
    def register_plugin(self, plugin_id: str, manifest: dict) -> None:
        """Register a plugin's manifest."""
        self.installed_plugins[plugin_id] = manifest
        
        # Register provided APIs
        for api in manifest.get("provides", []):
            self.api_providers[api] = plugin_id
    
    def unregister_plugin(self, plugin_id: str) -> None:
        """Unregister a plugin."""
        manifest = self.installed_plugins.pop(plugin_id, None)
        if manifest:
            for api in manifest.get("provides", []):
                if self.api_providers.get(api) == plugin_id:
                    del self.api_providers[api]
    
    def check_conflicts(self, new_manifest: dict) -> List[Conflict]:
        """Check for conflicts before installing a new plugin."""
        conflicts = []
        new_id = new_manifest["id"]
        
        # Check explicit conflicts
        conflicts.extend(self._check_explicit_conflicts(new_manifest))
        
        # Check API conflicts
        conflicts.extend(self._check_api_conflicts(new_manifest))
        
        # Check resource conflicts
        conflicts.extend(self._check_resource_conflicts(new_manifest))
        
        # Check dependency conflicts
        conflicts.extend(self._check_dependency_conflicts(new_manifest))
        
        return conflicts
    
    def _check_explicit_conflicts(self, manifest: dict) -> List[Conflict]:
        """Check for explicitly declared conflicts."""
        conflicts = []
        new_id = manifest["id"]
        
        # Check if new plugin conflicts with installed ones
        for conflict_id in manifest.get("conflicts", []):
            if conflict_id in self.installed_plugins:
                conflicts.append(Conflict(
                    type=ConflictType.EXPLICIT_CONFLICT,
                    severity=ConflictSeverity.ERROR,
                    plugin_a=new_id,
                    plugin_b=conflict_id,
                    resource="",
                    message=f"Plugin '{new_id}' declares conflict with installed plugin '{conflict_id}'",
                    resolution=[
                        f"Uninstall '{conflict_id}' before installing '{new_id}'",
                        f"Choose one of the conflicting plugins",
                    ],
                ))
        
        # Check if installed plugins conflict with new one
        for installed_id, installed_manifest in self.installed_plugins.items():
            if new_id in installed_manifest.get("conflicts", []):
                conflicts.append(Conflict(
                    type=ConflictType.EXPLICIT_CONFLICT,
                    severity=ConflictSeverity.ERROR,
                    plugin_a=installed_id,
                    plugin_b=new_id,
                    resource="",
                    message=f"Installed plugin '{installed_id}' conflicts with '{new_id}'",
                    resolution=[
                        f"Uninstall '{installed_id}' before installing '{new_id}'",
                    ],
                ))
        
        return conflicts
    
    def _check_api_conflicts(self, manifest: dict) -> List[Conflict]:
        """Check for API provision conflicts."""
        conflicts = []
        new_id = manifest["id"]
        
        for api in manifest.get("provides", []):
            if api in self.api_providers:
                existing_id = self.api_providers[api]
                conflicts.append(Conflict(
                    type=ConflictType.API_CONFLICT,
                    severity=ConflictSeverity.WARNING,
                    plugin_a=new_id,
                    plugin_b=existing_id,
                    resource=api,
                    message=f"Both '{new_id}' and '{existing_id}' provide API '{api}'",
                    resolution=[
                        f"Disable one of the plugins",
                        f"The newer plugin will take precedence",
                    ],
                ))
        
        return conflicts
    
    def _check_resource_conflicts(self, manifest: dict) -> List[Conflict]:
        """Check for exclusive resource conflicts."""
        conflicts = []
        new_id = manifest["id"]
        
        # Check for capture source conflicts
        if manifest.get("category") == "capture":
            for installed_id, installed_manifest in self.installed_plugins.items():
                if installed_manifest.get("category") == "capture":
                    conflicts.append(Conflict(
                        type=ConflictType.RESOURCE_CONFLICT,
                        severity=ConflictSeverity.WARNING,
                        plugin_a=new_id,
                        plugin_b=installed_id,
                        resource="capture_source",
                        message=f"Multiple capture plugins detected",
                        resolution=[
                            f"Only one capture plugin should be active at a time",
                        ],
                    ))
        
        return conflicts
    
    def _check_dependency_conflicts(self, manifest: dict) -> List[Conflict]:
        """Check for unmet or conflicting dependencies."""
        conflicts = []
        new_id = manifest["id"]
        
        for required_api in manifest.get("requires", []):
            if required_api not in self.api_providers:
                # Check if any installed plugin provides it
                found = False
                for installed_manifest in self.installed_plugins.values():
                    if required_api in installed_manifest.get("provides", []):
                        found = True
                        break
                
                if not found:
                    # This is a warning, not a conflict
                    logger.warning(f"Plugin '{new_id}' requires API '{required_api}' which is not provided")
        
        return conflicts


def format_conflict_message(conflict: Conflict) -> str:
    """Format a conflict for user display."""
    icon = "⚠️" if conflict.severity == ConflictSeverity.WARNING else "❌"
    
    message = f"{icon} {conflict.message}\n"
    message += "\nSuggested resolutions:\n"
    for i, resolution in enumerate(conflict.resolution, 1):
        message += f"  {i}. {resolution}\n"
    
    return message
```

---

## 📋 AUDIT LOGGING

```python
# src/plugins/audit.py

import json
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum
from pathlib import Path
import aiofiles

from src.core.logging import get_logger

logger = get_logger(__name__)


class AuditAction(str, Enum):
    PERMISSION_GRANTED = "permission_granted"
    PERMISSION_DENIED = "permission_denied"
    PERMISSION_REVOKED = "permission_revoked"
    
    FILE_READ = "file_read"
    FILE_WRITE = "file_write"
    FILE_DELETE = "file_delete"
    
    NETWORK_REQUEST = "network_request"
    NETWORK_BLOCKED = "network_blocked"
    
    SYSTEM_API_CALL = "system_api_call"
    SYSTEM_API_BLOCKED = "system_api_blocked"
    
    PLUGIN_INSTALLED = "plugin_installed"
    PLUGIN_UNINSTALLED = "plugin_uninstalled"
    PLUGIN_ENABLED = "plugin_enabled"
    PLUGIN_DISABLED = "plugin_disabled"
    PLUGIN_CRASHED = "plugin_crashed"
    PLUGIN_THROTTLED = "plugin_throttled"
    PLUGIN_KILLED = "plugin_killed"


class AuditEntry:
    """Single audit log entry."""
    
    def __init__(
        self,
        action: AuditAction,
        plugin_id: str,
        details: Optional[Dict[str, Any]] = None,
        success: bool = True,
    ):
        self.timestamp = datetime.utcnow().isoformat()
        self.action = action
        self.plugin_id = plugin_id
        self.details = details or {}
        self.success = success
    
    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "action": self.action.value,
            "plugin_id": self.plugin_id,
            "details": self.details,
            "success": self.success,
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict())


class AuditLogger:
    """Audit logger for security events."""
    
    def __init__(self):
        self.log_dir = Path.home() / ".clipshot" / "logs" / "audit"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self._current_file: Optional[str] = None
    
    @property
    def current_log_file(self) -> Path:
        """Get current log file (daily rotation)."""
        today = datetime.utcnow().strftime("%Y-%m-%d")
        return self.log_dir / f"audit_{today}.jsonl"
    
    async def log(self, entry: AuditEntry) -> None:
        """Log an audit entry."""
        async with aiofiles.open(self.current_log_file, "a") as f:
            await f.write(entry.to_json() + "\n")
        
        # Also log to standard logger for debugging
        if not entry.success:
            logger.warning(f"Audit: {entry.action.value} failed for {entry.plugin_id}")
    
    async def log_permission_denied(
        self, 
        plugin_id: str, 
        permission: str, 
        resource: Optional[str] = None
    ) -> None:
        """Log a permission denial."""
        await self.log(AuditEntry(
            action=AuditAction.PERMISSION_DENIED,
            plugin_id=plugin_id,
            details={"permission": permission, "resource": resource},
            success=False,
        ))
    
    async def log_file_access(
        self,
        plugin_id: str,
        path: str,
        operation: str,
        success: bool = True,
    ) -> None:
        """Log file access."""
        action = AuditAction.FILE_READ if operation == "read" else AuditAction.FILE_WRITE
        await self.log(AuditEntry(
            action=action,
            plugin_id=plugin_id,
            details={"path": path, "operation": operation},
            success=success,
        ))
    
    async def log_network_request(
        self,
        plugin_id: str,
        host: str,
        method: str,
        success: bool = True,
    ) -> None:
        """Log network request."""
        action = AuditAction.NETWORK_REQUEST if success else AuditAction.NETWORK_BLOCKED
        await self.log(AuditEntry(
            action=action,
            plugin_id=plugin_id,
            details={"host": host, "method": method},
            success=success,
        ))
    
    async def query_logs(
        self,
        plugin_id: Optional[str] = None,
        action: Optional[AuditAction] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
    ) -> list:
        """Query audit logs."""
        entries = []
        
        for log_file in sorted(self.log_dir.glob("audit_*.jsonl"), reverse=True):
            async with aiofiles.open(log_file, "r") as f:
                async for line in f:
                    entry = json.loads(line)
                    
                    # Apply filters
                    if plugin_id and entry["plugin_id"] != plugin_id:
                        continue
                    if action and entry["action"] != action.value:
                        continue
                    
                    entries.append(entry)
                    
                    if len(entries) >= limit:
                        return entries
        
        return entries
```

---

## 🎯 Bu Mimarinin Avantajları

1. **Defense in Depth** — Çoklu güvenlik katmanı
2. **Least Privilege** — Minimum gerekli izin
3. **Auditability** — Tüm eylemler loglanır
4. **Conflict Prevention** — Kurulum öncesi uyarı
5. **Resource Protection** — Kötüye kullanım engeli
6. **User Control** — İzinler her zaman değiştirilebilir
