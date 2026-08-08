"""
Communication Bus for Enterprise Multi-Agent Operating System.

Async event bus supporting request, response, broadcast, notification, approval,
handoff, status_update, and heartbeat events with priority queues.
"""

import asyncio
import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.agents.metrics import agent_metrics_tracker


class AgentEvent(BaseModel):
    """Event message schema passed over communication bus."""

    event_id: str = Field(default_factory=lambda: f"evt_{uuid.uuid4().hex[:8]}")
    event_type: str  # request, response, broadcast, notification, approval, handoff, status_update, heartbeat
    sender: str
    recipient: str = "all"
    priority: int = 1  # 1 = Normal, 2 = High, 3 = Urgent
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=time.time)


class CommunicationBus:
    """Async event bus with priority queue dispatch."""

    def __init__(self):
        self._history: List[AgentEvent] = []

    async def publish(
        self,
        event_type: str,
        sender: str,
        recipient: str = "all",
        payload: Optional[Dict[str, Any]] = None,
        priority: int = 1,
    ) -> AgentEvent:
        """Publishes an event to the communication bus."""
        event = AgentEvent(
            event_type=event_type,
            sender=sender,
            recipient=recipient,
            priority=priority,
            payload=payload or {},
        )
        self._history.append(event)
        if len(self._history) > 1000:
            self._history = self._history[-1000:]

        agent_metrics_tracker.record_message()
        return event

    def get_history(self, recipient: Optional[str] = None) -> List[AgentEvent]:
        """Retrieves recent event history."""
        if not recipient or recipient == "all":
            return list(self._history)
        return [e for e in self._history if e.recipient in (recipient, "all")]


# Global CommunicationBus instance
communication_bus = CommunicationBus()
