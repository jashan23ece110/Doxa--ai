"""
Shared Working Memory Workspace.

Provides thread-safe inter-agent task messaging, versioned state updates,
and shared evidence storage without direct mutable reference coupling.
"""

import threading
import time
from typing import List, Dict, Any, Optional
from app.core.logging import logger


class SharedWorkingMemory:
    """Thread-safe shared workspace for inter-agent communication."""

    def __init__(self, goal: str = ""):
        self.goal = goal
        self._lock = threading.Lock()
        self.version: int = 1
        self.evidence: List[Dict[str, Any]] = []
        self.messages: List[Dict[str, Any]] = []
        self.agent_outputs: Dict[str, Any] = {}
        self.created_at: float = time.time()

    @property
    def results(self) -> Dict[str, Any]:
        """Convenience accessor for agent_outputs."""
        return self.get_all_outputs()

    def add_result(self, role_name: str, data: Any) -> None:
        """Convenience method to store output for an agent role."""
        self.set_agent_output(role_name, data)

    def add_evidence(self, source: str, data: Any) -> None:
        """Appends evidence to shared workspace."""
        with self._lock:
            self.evidence.append({
                "source": source,
                "data": data,
                "timestamp": time.time(),
            })
            self.version += 1

    def send_message(self, sender: str, recipient: str, message: str) -> None:
        """Sends inter-agent message."""
        with self._lock:
            self.messages.append({
                "sender": sender,
                "recipient": recipient,
                "message": message,
                "timestamp": time.time(),
            })
            self.version += 1

    def set_agent_output(self, role_name: str, output_data: Any) -> None:
        """Stores output data for a specific agent role."""
        with self._lock:
            self.agent_outputs[role_name] = output_data
            self.version += 1
            logger.debug(f"Workspace updated by agent '{role_name}' (v{self.version})")

    def get_all_outputs(self) -> Dict[str, Any]:
        """Returns snapshot of all agent outputs."""
        with self._lock:
            return dict(self.agent_outputs)

    def get_all_evidence(self) -> List[Dict[str, Any]]:
        """Returns snapshot of all collected evidence."""
        with self._lock:
            return list(self.evidence)
