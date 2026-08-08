"""
Enterprise Agent Communication Bus.

Facilitates agent-to-agent messaging, task delegation, pub/sub event broadcasting,
priority message routing, and correlation tracking.
"""

import asyncio
import threading
import time
from typing import Dict, Any, List, Callable, Optional
from app.core.logging import security_logger
from app.core.agents.agent_types import AgentMessage


class AgentMessageBus:
    """Thread-safe Enterprise Agent Communication Bus."""

    def __init__(self):
        self._lock = threading.Lock()
        self._subscribers: Dict[str, List[Callable]] = {}
        self._message_history: List[AgentMessage] = []

    def subscribe(self, agent_id: str, callback: Callable):
        """Subscribes an agent callback listener."""
        with self._lock:
            if agent_id not in self._subscribers:
                self._subscribers[agent_id] = []
            self._subscribers[agent_id].append(callback)
            security_logger.info(f"AgentMessageBus: Agent '{agent_id}' subscribed to message bus.")

    async def send_message(self, message: AgentMessage):
        """Asynchronously dispatches an agent-to-agent message."""
        with self._lock:
            self._message_history.append(message)
            listeners = list(self._subscribers.get(message.recipient_agent_id, []))

        for listener in listeners:
            try:
                if asyncio.iscoroutinefunction(listener):
                    await listener(message)
                else:
                    listener(message)
            except Exception as e:
                security_logger.error(f"AgentMessageBus: Error dispatching message '{message.message_id}' to agent '{message.recipient_agent_id}': {str(e)}")

        security_logger.info(f"AgentMessageBus: Sent message '{message.message_id}' from '{message.sender_agent_id}' to '{message.recipient_agent_id}'.")


# Global AgentMessageBus instance
agent_message_bus = AgentMessageBus()
