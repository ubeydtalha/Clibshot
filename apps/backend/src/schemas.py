"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============ Plugin Schemas ============

class PluginBase(BaseModel):
    """Base plugin schema"""
    name: str = Field(..., min_length=1, max_length=255, description="Unique plugin name")
    display_name: str = Field(..., min_length=1, max_length=255, description="Display name")
    description: Optional[str] = Field(None, description="Plugin description")
    version: str = Field(..., min_length=1, max_length=50, description="Plugin version")
    author: Optional[str] = Field(None, max_length=255, description="Plugin author")
    plugin_type: str = Field(default="python", description="Plugin type (python, rust, cpp, etc.)")
    entry_point: str = Field(..., min_length=1, max_length=500, description="Entry point path")
    enabled: bool = Field(default=True, description="Plugin enabled status")
    plugin_metadata: Optional[Dict[str, Any]] = Field(None, serialization_alias="metadata", description="Additional metadata")


class PluginCreate(PluginBase):
    """Schema for creating a new plugin"""
    install_path: Optional[str] = Field(None, max_length=500, description="Installation path")


class PluginUpdate(BaseModel):
    """Schema for updating an existing plugin"""
    display_name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    version: Optional[str] = Field(None, min_length=1, max_length=50)
    author: Optional[str] = Field(None, max_length=255)
    enabled: Optional[bool] = None
    plugin_metadata: Optional[Dict[str, Any]] = Field(None, serialization_alias="metadata")
    
    model_config = ConfigDict(extra='forbid', populate_by_name=True)


class PluginResponse(PluginBase):
    """Schema for plugin response"""
    id: int
    install_path: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(
        from_attributes=True, 
        populate_by_name=True, 
        by_alias=True,
        ignored_types=(type,)
    )


# ============ Plugin Configuration Schemas ============

class PluginConfigBase(BaseModel):
    """Base plugin configuration schema"""
    key: str = Field(..., min_length=1, max_length=255, description="Configuration key")
    value: Optional[Any] = Field(None, description="Configuration value")


class PluginConfigCreate(PluginConfigBase):
    """Schema for creating plugin configuration"""
    pass  # plugin_id comes from URL path parameter


class PluginConfigUpdate(BaseModel):
    """Schema for updating plugin configuration"""
    value: Optional[Any] = None
    
    model_config = ConfigDict(extra='forbid')


class PluginConfigResponse(PluginConfigBase):
    """Schema for plugin configuration response"""
    id: int
    plugin_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============ Clip Schemas ============

class ClipBase(BaseModel):
    """Base clip schema"""
    title: str = Field(..., min_length=1, max_length=255, description="Clip title")
    description: Optional[str] = Field(None, description="Clip description")
    game_name: Optional[str] = Field(None, max_length=255, description="Game name")
    game_id: Optional[str] = Field(None, max_length=255, description="Game ID")
    tags: Optional[List[str]] = Field(None, description="Clip tags")
    clip_metadata: Optional[Dict[str, Any]] = Field(None, serialization_alias="metadata", description="Additional metadata")


class ClipCreate(ClipBase):
    """Schema for creating a new clip"""
    file_path: str = Field(..., min_length=1, max_length=500, description="File path")
    file_size: Optional[int] = Field(None, gt=0, description="File size in bytes")
    duration: Optional[int] = Field(None, gt=0, description="Duration in seconds")
    resolution: Optional[str] = Field(None, max_length=50, description="Video resolution")
    fps: Optional[int] = Field(None, gt=0, description="Frames per second")
    codec: Optional[str] = Field(None, max_length=50, description="Video codec")
    recorded_at: Optional[datetime] = Field(None, description="Recording timestamp")
    processed: Optional[bool] = Field(False, description="Processed status")
    processing_status: Optional[str] = Field(None, max_length=50, description="Processing status")


class ClipUpdate(BaseModel):
    """Schema for updating an existing clip"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    game_name: Optional[str] = Field(None, max_length=255)
    game_id: Optional[str] = Field(None, max_length=255)
    tags: Optional[List[str]] = None
    clip_metadata: Optional[Dict[str, Any]] = Field(None, serialization_alias="metadata")
    processed: Optional[bool] = None
    processing_status: Optional[str] = Field(None, max_length=50)
    
    model_config = ConfigDict(extra='forbid', populate_by_name=True)


class ClipResponse(ClipBase):
    """Schema for clip response"""
    id: int
    file_path: str
    file_size: Optional[int]
    duration: Optional[int]
    resolution: Optional[str]
    fps: Optional[int]
    codec: Optional[str]
    processed: bool
    processing_status: Optional[str]
    recorded_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(
        from_attributes=True, 
        populate_by_name=True, 
        by_alias=True,
        # Explicitly exclude SQLAlchemy metadata attribute
        ignored_types=(type,)
    )


# ============ Common Response Schemas ============

class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    detail: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str
    detail: Optional[str] = None
    status_code: int


class PaginatedResponse(BaseModel):
    """Paginated response wrapper"""
    items: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int
