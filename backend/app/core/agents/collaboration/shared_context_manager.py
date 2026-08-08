"""
Shared Multi-Agent Context Manager.

Provides controlled, session-isolated shared context preventing uncontrolled memory growth
and cross-session data leakage.
"""

import threading
import time
from typing import Dict, Any, Optional
from app.core.logging import security_logger
from app.core.agents.collaboration.collaboration_types import SharedContext, AgentObservation


class SharedContextManager:
    """Thread-safe Shared Multi-Agent Context Manager."""

    def __init__(self):
        self._lock = threading.Lock()
        self._contexts: Dict[str, SharedContext] = {}

    def get_or_create_context(self, session_id: str) -> SharedContext:
        """Retrieves or initializes a session-isolated SharedContext."""
        with self._lock:
            if session_id not in self._contexts:
                self._contexts[session_id] = SharedContext(session_id=session_id)
                security_logger.info(f"SharedContextManager: Initialized shared context for session '{session_id}'.")
            return self._contexts[session_id]

    def add_observation(self, session_id: str, observation: AgentObservation) -> None:
        """Adds an agent observation to shared context."""
        ctx = self.get_or_create_context(session_id)
        with self._lock:
            ctx.observations.append(observation)
            ctx.updated_at = time.time()
            security_logger.debug(f"SharedContextManager: Added observation from agent '{observation.agent_id}' to session '{session_id}'.")


# Global SharedContextManager instance
shared_context_manager = SharedContextManager()
