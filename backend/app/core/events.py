"""
In-Memory Event Bus and Decoupled Domain Event System.

Enables publisher-subscriber architecture for domain events (e.g. document ingested,
agent run started/completed, timer fired) without external message broker overhead.
"""

import asyncio
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Any, Callable, Awaitable
from app.core.logging import logger


class EventType(str, Enum):
    """Supported domain event types."""
    DOCUMENT_INGESTED = "document_ingested"
    DOCUMENT_DELETED = "document_deleted"
    AGENT_STARTED = "agent_started"
    AGENT_COMPLETED = "agent_completed"
    AGENT_FAILED = "agent_failed"
    TIMER_FIRED = "timer_fired"


class DomainEvent:
    """Represents a domain event payload."""

    def __init__(self, event_type: EventType, data: Dict[str, Any]):
        self.event_type = event_type
        self.data = data
        self.timestamp = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_type": self.event_type.value,
            "timestamp": self.timestamp,
            "data": self.data,
        }


EventHandler = Callable[[DomainEvent], Awaitable[None]]


class EventDispatcher:
    """In-memory event bus managing event handlers and async dispatching."""

    def __init__(self):
        self._subscribers: Dict[EventType, List[EventHandler]] = {
            event_type: [] for event_type in EventType
        }

    def subscribe(self, event_type: EventType, handler: EventHandler) -> None:
        """Subscribes an async handler to a domain event type."""
        if handler not in self._subscribers[event_type]:
            self._subscribers[event_type].append(handler)
            logger.debug(f"Subscribed handler '{handler.__name__}' to event '{event_type.value}'")

    def unsubscribe(self, event_type: EventType, handler: EventHandler) -> None:
        """Unsubscribes a handler from an event type."""
        if handler in self._subscribers[event_type]:
            self._subscribers[event_type].remove(handler)

    async def publish(self, event_type: EventType, data: Dict[str, Any]) -> None:
        """Publishes a domain event asynchronously to all subscribed handlers."""
        event = DomainEvent(event_type, data)
        handlers = self._subscribers.get(event_type, [])
        if not handlers:
            return

        logger.debug(f"Publishing event '{event_type.value}' to {len(handlers)} handler(s)")
        tasks = []
        for handler in handlers:
            try:
                tasks.append(asyncio.create_task(handler(event)))
            except Exception as e:
                logger.error(f"Error launching event handler '{handler.__name__}': {e}")

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)


# Global event dispatcher instance
event_dispatcher = EventDispatcher()
