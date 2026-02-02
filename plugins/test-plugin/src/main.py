"""Test Plugin for ClipShot."""

import asyncio
from typing import Any


async def init() -> None:
    """Initialize the test plugin."""
    print("Test Plugin: Initializing...")
    await asyncio.sleep(0.1)
    print("Test Plugin: Initialized successfully!")


async def shutdown() -> None:
    """Shutdown the test plugin."""
    print("Test Plugin: Shutting down...")
    await asyncio.sleep(0.1)
    print("Test Plugin: Shutdown complete!")


def get_info() -> dict[str, Any]:
    """Get plugin information."""
    return {
        "name": "Test Plugin",
        "version": "1.0.0",
        "status": "active",
    }
