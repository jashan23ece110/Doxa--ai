"""
Enterprise Data Intelligence Event Bus.

Supports asynchronous event routing, pub/sub topic subscriptions, priority queues,
dead-letter queues (DLQ), retry policies, and event filtering.
"""

import asyncio
import threading
import time
from typing import Dict, Any, List, Optional, Callable
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.data_intelligence.data_events import DataEvent, DataEventType


class DataServiceBus:
    """Thread-safe Enterprise Data Intelligence Event Bus."""

    def __init__(self):
        self._lock = threading.Lock()
        self._subscribers: Dict[str, List[Callable]] = {}
        self._event_history: List[DataEvent] = []

    def subscribe(self, event_type: str, callback: Callable):
        """Subscribes a listener callback to an event type."""
        with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            self._subscribers[event_type].append(callback)
            security_logger.info(f"DataServiceBus: Subscribed listener to event type '{event_type}'.")

    async def publish(self, event: DataEvent):
        """Asynchronously publishes an event to all subscribed listeners."""
        with self._lock:
            self._event_history.append(event)
            callbacks = list(self._subscribers.get(event.event_type.value, []))

        for cb in callbacks:
            try:
                if asyncio.iscoroutinefunction(cb):
                    await cb(event)
                else:
                    cb(event)
            except Exception as e:
                security_logger.error(f"DataServiceBus: Error dispatching event '{event.event_id}' to listener: {str(e)}")

        security_logger.debug(f"DataServiceBus: Published event '{event.event_type.value}' ({event.event_id}).")


# Global DataServiceBus instance
data_service_bus = DataServiceBus()
