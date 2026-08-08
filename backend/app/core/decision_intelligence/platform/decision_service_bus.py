"""
Enterprise Decision Event Bus.

Handles asynchronous decision, risk, forecast, optimization, approval, and outcome events with correlation tracking.
"""

import threading
import time
import uuid
from typing import Dict, Any, List, Callable, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class DecisionEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"devent_{uuid.uuid4().hex[:8]}")
    event_type: str  # DECISION_CREATED, RISK_ASSESSED, OPTIMIZATION_COMPLETED, APPROVAL_GRANTED
    correlation_id: str = Field(default_factory=lambda: f"corr_{uuid.uuid4().hex[:8]}")
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=time.time)


class DecisionServiceBus:
    """Thread-safe Enterprise Decision Event Bus."""

    def __init__(self):
        self._lock = threading.Lock()
        self._handlers: Dict[str, List[Callable]] = {}
        self._events: List[DecisionEvent] = []

    def publish_event(self, event_type: str, payload: Dict[str, Any], correlation_id: Optional[str] = None) -> DecisionEvent:
        """
        Publishes an event to the Decision Service Bus.

        Args:
            event_type: Event topic string.
            payload: Payload dictionary.
            correlation_id: Optional correlation ID string.

        Returns:
            DecisionEvent object.
        """
        cid = correlation_id or f"corr_{uuid.uuid4().hex[:8]}"
        event = DecisionEvent(event_type=event_type, correlation_id=cid, payload=payload)

        with self._lock:
            self._events.append(event)
            handlers = self._handlers.get(event_type, [])

        for h in handlers:
            try:
                h(event)
            except Exception as e:
                security_logger.error(f"DecisionServiceBus: Handler exception for '{event_type}': {e}")

        security_logger.info(f"DecisionServiceBus: Published event '{event.event_id}' ({event_type}, CID={cid}).")
        return event

    def subscribe(self, event_type: str, handler: Callable):
        """Subscribes handler to target event_type."""
        with self._lock:
            if event_type not in self._handlers:
                self._handlers[event_type] = []
            self._handlers[event_type].append(handler)


# Global DecisionServiceBus instance
decision_service_bus = DecisionServiceBus()
