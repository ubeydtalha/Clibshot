"""
Plugin permission system.

Manages plugin permissions for various resources and operations.
"""

import json
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime

from ..core.logging import get_logger
from ..db.session import get_session

logger = get_logger(__name__)


class PermissionLevel(str, Enum):
    """Permission level for a capability."""
    NONE = "none"
    LIMITED = "limited"
    OPTIONAL = "optional"
    REQUIRED = "required"


class PermissionCategory(str, Enum):
    """Categories of permissions."""
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
    
    # Path aliases for filesystem permissions
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
            # Create table if not exists
            session.execute("""
                CREATE TABLE IF NOT EXISTS plugin_permissions (
                    plugin_id TEXT NOT NULL,
                    category TEXT NOT NULL,
                    level TEXT NOT NULL,
                    granted INTEGER NOT NULL DEFAULT 0,
                    granted_at TEXT,
                    paths TEXT,
                    hosts TEXT,
                    apis TEXT,
                    PRIMARY KEY (plugin_id, category)
                )
            """)
            
            # Load from database
            grants = session.execute(
                "SELECT * FROM plugin_permissions WHERE plugin_id = ?",
                (plugin_id,)
            )
            
            result = {}
            for row in grants:
                category = PermissionCategory(row["category"])
                result[category] = PermissionGrant(
                    category=category,
                    level=PermissionLevel(row["level"]),
                    granted=bool(row["granted"]),
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
                session.execute("""
                    INSERT OR REPLACE INTO plugin_permissions 
                    (plugin_id, category, level, granted, granted_at, paths, hosts, apis)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    plugin_id,
                    category.value,
                    grant.level.value,
                    int(grant.granted),
                    grant.granted_at or datetime.now().isoformat(),
                    json.dumps(grant.paths),
                    json.dumps(grant.hosts),
                    json.dumps(grant.apis),
                ))
        
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
        try:
            path_obj = Path(path).resolve()
        except Exception:
            return False
        
        for allowed_pattern in grant.paths:
            # Resolve aliases
            if allowed_pattern.startswith("$"):
                alias_func = self.PATH_ALIASES.get(allowed_pattern)
                if alias_func:
                    allowed_path = alias_func(plugin_id)
                    try:
                        if path_obj == allowed_path or allowed_path in path_obj.parents:
                            return True
                    except Exception:
                        continue
            else:
                try:
                    allowed_path = Path(allowed_pattern).resolve()
                    if path_obj == allowed_path or allowed_path in path_obj.parents:
                        return True
                except Exception:
                    continue
        
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
        """Check screen capture permission."""
        return self.manager.check_permission(self.plugin_id, PermissionCategory.SCREEN)
    
    def require_microphone(self) -> bool:
        """Check microphone permission."""
        return self.manager.check_permission(self.plugin_id, PermissionCategory.MICROPHONE)
    
    def require_filesystem(self, path: str, operation: str = "read") -> bool:
        """Check filesystem permission for a path."""
        return self.manager.check_permission(
            self.plugin_id, 
            PermissionCategory.FILESYSTEM, 
            path
        )
    
    def require_network(self, host: str) -> bool:
        """Check network permission for a host."""
        return self.manager.check_permission(
            self.plugin_id, 
            PermissionCategory.NETWORK, 
            host
        )
    
    def require_gpu(self) -> bool:
        """Check GPU access permission."""
        return self.manager.check_permission(self.plugin_id, PermissionCategory.GPU)
    
    def require_system(self, api: str) -> bool:
        """Check system API permission."""
        return self.manager.check_permission(
            self.plugin_id, 
            PermissionCategory.SYSTEM, 
            api
        )
