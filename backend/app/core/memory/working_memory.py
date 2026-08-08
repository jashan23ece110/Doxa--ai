"""
Layer 1: Working Memory Manager.

Manages active in-flight conversation turns for current reasoning continuity without context bloat.
"""

from typing import List, Dict, Any


class WorkingMemory:
    """Manages immediate working memory turns for current interaction."""

    def __init__(self, max_turns: int = 6):
        self.max_turns = max_turns
        self._turns: List[Dict[str, str]] = []

    def add_turn(self, role: str, content: str) -> None:
        """Appends a new turn to working memory and prunes oldest beyond max_turns."""
        self._turns.append({"role": role, "content": content})
        if len(self._turns) > self.max_turns:
            self._turns = self._turns[-self.max_turns:]

    def get_recent_turns(self) -> List[Dict[str, str]]:
        """Returns active working memory turns."""
        return list(self._turns)

    def clear(self) -> None:
        """Clears active working memory."""
        self._turns.clear()
