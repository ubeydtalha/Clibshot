"""Logging configuration for ClipShot Backend."""

import sys
from loguru import logger

from src.config import settings


def setup_logging() -> None:
    """Configure logging for the application."""
    # Remove default handler
    logger.remove()
    
    # Add custom handler
    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True,
    )
    
    # Add file handler in production
    if not settings.DEBUG:
        logger.add(
            "logs/clipshot_{time:YYYY-MM-DD}.log",
            rotation="00:00",
            retention="7 days",
            level="INFO",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        )


def get_logger(name: str) -> logger:
    """Get a logger instance."""
    return logger.bind(name=name)
