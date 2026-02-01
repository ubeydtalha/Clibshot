"""Event bus for inter-component communication."""

from typing import Any, Callable, Dict, List
import asyncio
from src.core.logging import get_logger

logger = get_logger(__name__)


class EventBus:
    """Simple event bus for pub/sub pattern."""
    
    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Callable]] = {}
        self._running = True
    
    def subscribe(self, event_type: str, callback: Callable) -> None:
        """Subscribe to an event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)
        logger.debug(f"Subscribed to event: {event_type}")
    
    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """Unsubscribe from an event type."""
        if event_type in self._subscribers:
            self._subscribers[event_type].remove(callback)
            logger.debug(f"Unsubscribed from event: {event_type}")
    
    async def publish(self, event_type: str, data: Any = None) -> None:
        """Publish an event."""
        if not self._running:
            return
        
        if event_type in self._subscribers:
            logger.debug(f"Publishing event: {event_type}")
            for callback in self._subscribers[event_type]:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(data)
                    else:
                        callback(data)
                except Exception as e:
                    logger.error(f"Error in event callback for {event_type}: {e}")
    
    async def close(self) -> None:
        """Close the event bus."""
        self._running = False
        self._subscribers.clear()
        logger.info("Event bus closed")
