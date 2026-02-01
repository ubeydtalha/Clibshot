"""Pydantic schemas for plugins."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class PluginType(str, Enum):
    """Plugin type classification."""
    
    CORE = "core"
    OPTIONAL = "optional"
    AI = "ai"
    UI = "ui"
    SYSTEM = "system"


class PluginCategory(str, Enum):
    """Plugin category classification."""
    
    CAPTURE = "capture"
    AI = "ai"
    EDITOR = "editor"
    SOCIAL = "social"
    ENHANCEMENT = "enhancement"
    CODEC = "codec"
    TEMPLATE = "template"
    ANALYTICS = "analytics"


class PluginStatus(str, Enum):
    """Plugin status."""
    
    INSTALLED = "installed"
    LOADED = "loaded"
    ACTIVE = "active"
    ERROR = "error"
    DISABLED = "disabled"


class PluginAuthor(BaseModel):
    """Plugin author information."""
    
    name: str
    email: Optional[str] = None
    url: Optional[str] = None


class PluginManifest(BaseModel):
    """Plugin manifest schema."""
    
    id: str = Field(..., description="Unique plugin identifier (reverse domain)")
    name: str = Field(..., description="Display name")
    version: str = Field(..., description="Semantic version (X.Y.Z)")
    api_version: str = Field(default="v1", description="ClipShot API version")
    type: PluginType
    category: PluginCategory
    description: Dict[str, str] = Field(default_factory=dict)
    author: PluginAuthor
    repository: Optional[str] = None
    license: str = "MIT"
    homepage: Optional[str] = None
    bugs: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)
    entry: Dict[str, str] = Field(default_factory=dict)
    permissions: Dict[str, Any] = Field(default_factory=dict)
    capabilities: List[str] = Field(default_factory=list)
    provides: List[str] = Field(default_factory=list)
    requires: List[str] = Field(default_factory=list)
    conflicts: List[str] = Field(default_factory=list)
    settings: Optional[Dict[str, Any]] = None
    ui: Optional[Dict[str, bool]] = None
    localization: Optional[Dict[str, Any]] = None
    resources: Optional[Dict[str, Any]] = None
    security: Optional[Dict[str, Any]] = None
    platforms: List[str] = Field(default_factory=lambda: ["windows"])
    engines: Optional[Dict[str, str]] = None


class PluginInfo(BaseModel):
    """Plugin information response."""
    
    id: str
    name: str
    version: str
    type: PluginType
    category: PluginCategory
    description: str
    author: PluginAuthor
    status: PluginStatus
    enabled: bool
    installed_at: Optional[str] = None
    loaded_at: Optional[str] = None
    error: Optional[str] = None


class PluginConfig(BaseModel):
    """Plugin configuration."""
    
    plugin_id: str
    config: Dict[str, Any]


class PluginInstallRequest(BaseModel):
    """Plugin installation request."""
    
    source: str = Field(..., description="GitHub URL or local path")
    version: Optional[str] = Field(None, description="Specific version to install")


class PluginLoadResponse(BaseModel):
    """Plugin load response."""
    
    plugin_id: str
    status: PluginStatus
    message: str


class PluginHealth(BaseModel):
    """Plugin health status."""
    
    plugin_id: str
    healthy: bool
    cpu_percent: float
    memory_mb: float
    uptime_seconds: float
    errors: List[str] = Field(default_factory=list)
