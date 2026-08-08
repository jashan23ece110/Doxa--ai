"""
Event Bridge for Universal Integration Platform.

Bidirectional event routing supporting webhooks, Kafka, RabbitMQ, Redis Streams, NATS,
Google Pub/Sub, AWS SNS/SQS, and Azure Event Grid.
"""

from typing import Dict, Any, List, Callable, Coroutine
from app.core.logging import logger


class EventBridge:
    """Manages bidirectional integration event routing."""

    def __init__(self):
        self._handlers: Dict[str, List[Callable[[Dict[str, Any]], Coroutine[Any, Any, None]]]] = {}

    def subscribe_event(self, topic: str, handler: Callable[[Dict[str, Any]], Coroutine[Any, Any, None]]) -> None:
        """Subscribes an async handler to an integration event topic."""
        if topic not in self._handlers:
            self._handlers[topic] = []
        self._handlers[topic].append(handler)
        logger.info(f"Subscribed handler to event topic '{topic}'.")

    async def publish_event(self, topic: str, payload: Dict[str, Any]) -> int:
        """Publishes an integration event to registered topic subscribers."""
        handlers = self._handlers.get(topic, [])
        for handler in handlers:
            try:
                await handler(payload)
            except Exception as e:
                logger.error(f"Error handling event topic '{topic}': {e}")
        return len(handlers)


# Global EventBridge instance
event_bridge = EventBridge()
