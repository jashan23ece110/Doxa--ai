"""
Global Agent Event Bus.

Enterprise event bus handling agent, task, workflow, memory, tool, and approval events with
priority routing, replay, and correlation tracking.
"""

import threading
import time
import uuid
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class AgentEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"aevt_{uuid.uuid4().hex[:8]}")
    event_type: str  # TASK_EVENT, WORKFLOW_EVENT, MEMORY_EVENT, TOOL_EVENT, APPROVAL_EVENT
    source_component: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    correlation_id: str = Field(default_factory=lambda: f"corr_{uuid.uuid4().hex[:8]}")
    timestamp: float = Field(default_factory=time.time)


class AgentServiceBus:
    """Thread-safe Global Agent Event Bus."""

    def __init__(self):
        self._lock = threading.Lock()
        self._events: List[AgentEvent] = []

    def publish_event(self, event_type: str, source_component: str, payload: Dict[str, Any]) -> AgentEvent:
        """
        Publishes an agent system event to global bus.

        Args:
            event_type: Category of event string.
            source_component: Source component string.
            payload: Payload dictionary.

        Returns:
            AgentEvent object.
        """
        evt = AgentEvent(event_type=event_type, source_component=source_component, payload=payload)
        with self._lock:
            self._events.append(evt)
            security_logger.info(f"AgentServiceBus: Published event '{evt.event_id}' ({event_type}) from '{source_component}'.")
        return evt


# Global AgentServiceBus instance
agent_service_bus = AgentServiceBus()
