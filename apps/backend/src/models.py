"""
Database models for ClipShot
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Plugin(Base):
    """Plugin model - represents an installed plugin"""
    __tablename__ = "plugins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    display_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    version = Column(String(50), nullable=False)
    author = Column(String(255), nullable=True)
    
    # Plugin type: python, rust, cpp, etc.
    plugin_type = Column(String(50), nullable=False, default="python")
    
    # Entry point: path to main file or module
    entry_point = Column(String(500), nullable=False)
    
    # Plugin status
    enabled = Column(Boolean, default=True, nullable=False)
    
    # Installation path
    install_path = Column(String(500), nullable=True)
    
    # Plugin metadata (JSON): dependencies, config schema, etc.
    plugin_metadata = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    configurations = relationship("PluginConfiguration", back_populates="plugin", cascade="all, delete-orphan")
    

class PluginConfiguration(Base):
    """Plugin configuration - stores plugin-specific settings"""
    __tablename__ = "plugin_configurations"

    id = Column(Integer, primary_key=True, index=True)
    plugin_id = Column(Integer, ForeignKey("plugins.id", ondelete="CASCADE"), nullable=False)
    
    # Configuration key-value
    key = Column(String(255), nullable=False)
    value = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    plugin = relationship("Plugin", back_populates="configurations")
    
    # Unique constraint on plugin_id + key
    __table_args__ = (
        {'sqlite_autoincrement': True},
    )


class Clip(Base):
    """Clip model - represents a captured gaming clip"""
    __tablename__ = "clips"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # File information
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=True)  # in bytes
    duration = Column(Integer, nullable=True)  # in seconds
    
    # Video metadata
    resolution = Column(String(50), nullable=True)  # e.g., "1920x1080"
    fps = Column(Integer, nullable=True)
    codec = Column(String(50), nullable=True)
    
    # Game information
    game_name = Column(String(255), nullable=True, index=True)
    game_id = Column(String(255), nullable=True)
    
    # Processing status
    processed = Column(Boolean, default=False, nullable=False)
    processing_status = Column(String(50), nullable=True)  # pending, processing, completed, failed
    
    # Tags and metadata
    tags = Column(JSON, nullable=True)  # Array of tags
    clip_metadata = Column(JSON, nullable=True)  # Additional metadata
    
    # Timestamps
    recorded_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
