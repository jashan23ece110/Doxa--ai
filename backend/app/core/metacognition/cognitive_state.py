"""
Cognitive State Manager for Meta-Cognitive Layer.

Tracks current strategy, reasoning depth, uncertainty, confidence, tool usage,
memory usage, and active workflows.
"""

import threading
from typing import Dict, Any, Optional
from app.core.metacognition.metacognition_models import CognitiveStateSnapshot, CognitiveStrategy


class CognitiveStateManager:
    """Thread-safe cognitive state manager."""

    def __init__(self):
        self._lock = threading.Lock()
        self._state = CognitiveStateSnapshot()

    def update_state(
        self,
        strategy: Optional[CognitiveStrategy] = None,
        depth: Optional[int] = None,
        uncertainty: Optional[float] = None,
        confidence: Optional[float] = None,
    ) -> CognitiveStateSnapshot:
        """Updates internal cognitive state metrics."""
        with self._lock:
            if strategy is not None:
                self._state.active_strategy = strategy
            if depth is not None:
                self._state.reasoning_depth = depth
            if uncertainty is not None:
                self._state.uncertainty_score = uncertainty
            if confidence is not None:
                self._state.confidence_score = confidence

            return self._state

    def get_current_state(self) -> CognitiveStateSnapshot:
        """Returns active cognitive state snapshot."""
        with self._lock:
            return self._state


# Global CognitiveStateManager instance
cognitive_state_manager = CognitiveStateManager()
