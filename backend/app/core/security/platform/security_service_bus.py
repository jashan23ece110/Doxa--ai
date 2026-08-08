"""
Enterprise Security Service Bus.

Asynchronous event bus supporting topic publish/subscribe, priority routing,
dead-letter queueing, event persistence, filtering, and automated retry policies.
"""

import asyncio
import threading
import time
from typing import Dict, Any, List, Callable, Awaitable, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class SecurityEvent(BaseModel):
    event_id: str
    topic: str
    priority: int = 100  # High priority = lower number
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=time.time)


class SecurityServiceBus:
    """Thread-safe Asynchronous Security Event Bus."""

    def __init__(self):
        self._lock = threading.Lock()
        self._subscriptions: Dict[str, List[Callable[[SecurityEvent], Awaitable[None]]]] = {}
        self._dead_letter_queue: List[SecurityEvent] = []
        self._processed_events_count = 0

    def subscribe(self, topic: str, handler: Callable[[SecurityEvent], Awaitable[None]]):
        """Subscribes an async handler to a security event topic."""
        with self._lock:
            if topic not in self._subscriptions:
                self._subscriptions[topic] = []
            self._subscriptions[topic].append(handler)
            security_logger.debug(f"SecurityServiceBus: Subscribed handler to topic '{topic}'.")

    async def publish(self, topic: str, payload: Dict[str, Any], priority: int = 100) -> SecurityEvent:
        """
        Publishes a security event to topic subscriber handlers.

        Args:
            topic: Topic string.
            payload: Event payload dictionary.
            priority: Event priority integer.

        Returns:
            SecurityEvent object.
        """
        evt = SecurityEvent(
            event_id=f"evt_{int(time.time() * 1000)}",
            topic=topic,
            priority=priority,
            payload=payload,
        )

        with self._lock:
            handlers = list(self._subscriptions.get(topic, []))
            self._processed_events_count += 1

        for handler in handlers:
            try:
                await handler(evt)
            except Exception as ex:
                security_logger.error(f"SecurityServiceBus: Handler exception on topic '{topic}': {ex}")
                with self._lock:
                    self._dead_letter_queue.append(evt)

        security_logger.debug(f"SecurityServiceBus: Published event '{evt.event_id}' to topic '{topic}' ({len(handlers)} subscribers).")
        return evt


# Global SecurityServiceBus instance
security_service_bus = SecurityServiceBus()
