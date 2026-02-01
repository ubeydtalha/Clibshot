"""Core configuration for ClipShot Backend."""

from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    # Application
    APP_NAME: str = "ClipShot API"
    VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # CORS
    CORS_ORIGINS: Union[List[str], str] = [
        "tauri://localhost",
        "http://localhost:5173",
        "http://localhost:3000",
    ]
    
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./clipshot.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_ENABLED: bool = False
    
    # Plugins
    PLUGINS_DIR: str = "./plugins"
    PLUGIN_CACHE_TTL: int = 300  # 5 minutes
    
    # AI Runtime
    AI_MODELS_DIR: str = "./models"
    AI_DEFAULT_RUNTIME: str = "onnx"  # onnx, tensorflow_lite
    
    # Performance
    MAX_WORKERS: int = 4
    REQUEST_TIMEOUT: int = 30
    
    # Security
    SECRET_KEY: str = "change-this-in-production"
    
    # Logging
    LOG_LEVEL: str = "INFO"


# Global settings instance
settings = Settings()
