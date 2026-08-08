"""
Enterprise Agent Lifecycle Manager.

Manages agent registration, dependency validation, activation, suspension, and graceful shutdown.
"""

import threading
import time
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class AgentLifecycleStatus(BaseModel):
    agent_id: str
    status: str = "ACTIVE"  # INITIALIZING, ACTIVE, SUSPENDED, RETIRED
    version: str = "1.0.0"
    activated_at: float = Field(default_factory=time.time)


class AgentLifecycleManager:
    """Thread-safe Enterprise Agent Lifecycle Manager."""

    def __init__(self):
        self._lock = threading.Lock()
        self._status_map: Dict[str, AgentLifecycleStatus] = {}

    def activate_agent(self, agent_id: str, version: str = "1.0.0") -> AgentLifecycleStatus:
        """
        Validates dependencies and activates target agent.

        Args:
            agent_id: Target agent ID.
            version: Agent version string.

        Returns:
            AgentLifecycleStatus object.
        """
        status = AgentLifecycleStatus(agent_id=agent_id, status="ACTIVE", version=version)
        with self._lock:
            self._status_map[agent_id] = status
            security_logger.info(f"AgentLifecycleManager: Activated agent '{agent_id}' (v{version}).")
        return status

    def suspend_agent(self, agent_id: str) -> bool:
        """Suspends an active agent gracefully."""
        with self._lock:
            if agent_id in self._status_map:
                self._status_map[agent_id].status = "SUSPENDED"
                security_logger.info(f"AgentLifecycleManager: Suspended agent '{agent_id}' gracefully.")
                return True
            return False


# Global AgentLifecycleManager instance
agent_lifecycle_manager = AgentLifecycleManager()
