"""
Abstract Trace Repository Interface.

Defines the contract for agent trace storage backends (Firestore, PostgreSQL, Memory, MongoDB, Redis).
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class ITraceRepository(ABC):
    """Abstract interface for agent execution trace storage."""

    @abstractmethod
    def save_trace(self, run_id: str, trace: Dict[str, Any]) -> None:
        """Saves or updates an agent execution trace."""
        pass

    @abstractmethod
    def get_trace(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves an agent execution trace by run_id."""
        pass
