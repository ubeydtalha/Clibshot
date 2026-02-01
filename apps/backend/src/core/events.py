"""
Event bus for asynchronous communication between components.
"""

import asyncio
from typing import Dict, List, Callable, Any
from dataclasses import dataclass

from .logging import get_logger

logger = get_logger(__name__)


@dataclass
class Event:
    """Event data structure."""
    name: str
    data: Dict[str, Any]


class EventBus:
    """Simple event bus for pub/sub communication."""
    
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_name: str, handler: Callable) -> None:
        """Subscribe to an event."""
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        self._handlers[event_name].append(handler)
        logger.debug(f"Subscribed to event: {event_name}")
    
    def unsubscribe(self, event_name: str, handler: Callable) -> None:
        """Unsubscribe from an event."""
        if event_name in self._handlers:
            self._handlers[event_name].remove(handler)
    
    async def emit(self, event_name: str, data: Dict[str, Any]) -> None:
        """Emit an event to all subscribers."""
        if event_name not in self._handlers:
            return
        
        event = Event(name=event_name, data=data)
        
        for handler in self._handlers[event_name]:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except Exception as e:
                logger.error(f"Error in event handler for {event_name}: {e}")
