"""
Cognitive Event Bus for Meta-Cognitive Layer.

Publishes and routes cognitive events: STRATEGY_SELECTED, CONFIDENCE_UPDATED,
UNCERTAINTY_DETECTED, REFLECTION_COMPLETED, SELF_CRITIQUE_COMPLETED, REASONING_IMPROVED.
"""

from typing import Dict, Any, List, Callable, Coroutine
from app.core.logging import logger


class CognitiveEventBus:
    """Async cognitive event broker."""

    def __init__(self):
        self._listeners: Dict[str, List[Callable[[Dict[str, Any]], Coroutine[Any, Any, None]]]] = {}

    def subscribe(self, event_type: str, listener: Callable[[Dict[str, Any]], Coroutine[Any, Any, None]]) -> None:
        """Subscribes an async listener to a cognitive event type."""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)

    async def publish(self, event_type: str, payload: Dict[str, Any]) -> int:
        """Publishes a cognitive event to subscribed listeners."""
        listeners = self._listeners.get(event_type, [])
        for listener in listeners:
            try:
                await listener(payload)
            except Exception as e:
                logger.error(f"Error handling cognitive event '{event_type}': {e}")
        return len(listeners)


# Global CognitiveEventBus instance
cognitive_event_bus = CognitiveEventBus()
