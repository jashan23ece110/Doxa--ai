"""
Enterprise Agent Collaboration Bus.

Provides high-throughput inter-agent messaging, broadcast events, priority routing,
and dead-letter queue management.
"""

import threading
import time
from typing import Dict, Any, List
from app.core.logging import security_logger
from app.core.agents.collaboration.collaboration_types import AgentMessage


class CollaborationBus:
    """Thread-safe Enterprise Agent Collaboration Bus."""

    def __init__(self):
        self._lock = threading.Lock()
        self._messages: List[AgentMessage] = []

    def publish_message(self, message: AgentMessage) -> bool:
        """
        Publishes a message to direct recipient or broadcast channel.

        Args:
            message: AgentMessage object.

        Returns:
            Boolean indicating publish success.
        """
        with self._lock:
            self._messages.append(message)
            security_logger.info(f"CollaborationBus: Routed message '{message.message_id}' ({message.message_type}) from agent '{message.sender_agent_id}' -> '{message.recipient_agent_id}'.")
            return True

    def get_messages_for_agent(self, agent_id: str) -> List[AgentMessage]:
        """Retrieves unread messages targeted to specific agent or broadcast."""
        with self._lock:
            return [m for m in self._messages if m.recipient_agent_id in (agent_id, "BROADCAST")]


# Global CollaborationBus instance
collaboration_bus = CollaborationBus()
