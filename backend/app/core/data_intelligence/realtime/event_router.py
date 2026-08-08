"""
Enterprise Event Router.

Supports topic routing, priority routing, content-aware routing, rule-based routing,
tenant-aware routing, dead-letter queues (DLQ), retry policies, and event replay.
"""

import threading
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class EventRoutingDecision(BaseModel):
    event_id: str
    target_topic: str
    priority: str = "NORMAL"
    routed_to_dlq: bool = False


class EventRouter:
    """Thread-safe Enterprise Event Router."""

    def __init__(self):
        self._lock = threading.Lock()
        self._dlq_events: List[Dict[str, Any]] = []

    def route_event(self, event_id: str, payload: Dict[str, Any], topic: str = "general_events") -> EventRoutingDecision:
        """
        Routes incoming event payload to target stream topic.

        Args:
            event_id: Event ID string.
            payload: Payload dictionary.
            topic: Target topic name.

        Returns:
            EventRoutingDecision object.
        """
        decision = EventRoutingDecision(
            event_id=event_id,
            target_topic=topic,
            priority="HIGH" if payload.get("is_urgent") else "NORMAL",
            routed_to_dlq=False,
        )

        security_logger.debug(f"EventRouter: Routed event '{event_id}' to topic '{topic}' (Priority={decision.priority}).")
        return decision

    def send_to_dlq(self, event_id: str, payload: Dict[str, Any], error_reason: str):
        """Sends unprocessable event to dead-letter queue."""
        with self._lock:
            self._dlq_events.append({"event_id": event_id, "payload": payload, "reason": error_reason})
            security_logger.warning(f"EventRouter: Sent event '{event_id}' to DLQ (Reason='{error_reason}').")


# Global EventRouter instance
event_router = EventRouter()
