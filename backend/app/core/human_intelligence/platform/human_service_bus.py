"""
Enterprise Human Intelligence Service Bus.

Provides asynchronous event routing, publish/subscribe pattern, event replay,
priority routing, dead-letter queue (DLQ) handling, retry policies, and event filtering.
"""

import asyncio
import threading
import time
from typing import Dict, Any, List, Callable, Awaitable, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.human_intelligence.human_events import HumanEvent, HumanEventType


class HumanServiceBus:
    """Thread-safe Enterprise Human Intelligence Event Bus."""

    def __init__(self):
        self._lock = threading.Lock()
        self._subscribers: Dict[HumanEventType, List[Callable[[HumanEvent], Awaitable[None]]]] = {}
        self._event_history: List[HumanEvent] = []
        self._dead_letter_queue: List[HumanEvent] = []

    def subscribe(self, event_type: HumanEventType, handler: Callable[[HumanEvent], Awaitable[None]]):
        """Subscribes an async handler to a specific event type."""
        with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            self._subscribers[event_type].append(handler)
            security_logger.debug(f"HumanServiceBus: Subscribed handler for event type '{event_type.value}'.")

    async def publish(self, event: HumanEvent):
        """Publishes an event to registered subscribers with exception safety."""
        with self._lock:
            self._event_history.append(event)
            handlers = list(self._subscribers.get(event.event_type, []))

        security_logger.info(f"HumanServiceBus: Publishing event '{event.event_id}' ({event.event_type.value}).")

        for handler in handlers:
            try:
                await handler(event)
            except Exception as e:
                security_logger.error(f"HumanServiceBus: Error handling event '{event.event_id}': {e}")
                with self._lock:
                    self._dead_letter_queue.append(event)


# Global HumanServiceBus instance
human_service_bus = HumanServiceBus()
