"""
Observability Event Bus for Enterprise Observability Platform.

Publishes and routes observability events: TRACE_STARTED, TRACE_FINISHED, SPAN_CREATED,
ALERT_CREATED, HEALTH_CHANGED, RECOVERY_STARTED, RECOVERY_COMPLETED, DIAGNOSTIC_COMPLETED.
"""

from typing import Dict, Any, List, Callable, Coroutine
from app.core.logging import logger


class ObservabilityEventBus:
    """Async observability event broker."""

    def __init__(self):
        self._listeners: Dict[str, List[Callable[[Dict[str, Any]], Coroutine[Any, Any, None]]]] = {}

    def subscribe(self, event_type: str, listener: Callable[[Dict[str, Any]], Coroutine[Any, Any, None]]) -> None:
        """Subscribes an async listener to an observability event type."""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)

    async def publish(self, event_type: str, payload: Dict[str, Any]) -> int:
        """Publishes an observability event to all subscribed listeners."""
        listeners = self._listeners.get(event_type, [])
        for listener in listeners:
            try:
                await listener(payload)
            except Exception as e:
                logger.error(f"Error handling observability event '{event_type}': {e}")
        return len(listeners)


# Global ObservabilityEventBus instance
observability_event_bus = ObservabilityEventBus()
