"""
Layer 2: Session Memory Manager.

Maintains condensed, incremental summaries of the active chat session.
"""

from typing import List, Dict, Any, Optional


class SessionMemory:
    """Maintains active chat session state and condensed summaries."""

    def __init__(self, session_id: str = "default_session"):
        self.session_id = session_id
        self.summary: str = ""
        self.turns_count: int = 0

    def update_summary(self, new_summary: str) -> None:
        """Updates the session summary string."""
        self.summary = new_summary

    def increment_turns(self) -> None:
        """Increments processed turns counter."""
        self.turns_count += 1

    def to_dict(self) -> Dict[str, Any]:
        """Serializes session memory object."""
        return {
            "session_id": self.session_id,
            "summary": self.summary,
            "turns_count": self.turns_count,
        }
