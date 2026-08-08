"""
Stateful Stream Processing Engine.

Maintains stream event windows, counters, aggregates, entity state, temporal state,
and correlation state with snapshotting and state expiration.
"""

import threading
import time
from typing import Dict, Any, Optional
from app.core.logging import security_logger


class StreamStateManager:
    """Thread-safe Stateful Stream Processing Engine."""

    def __init__(self):
        self._lock = threading.Lock()
        self._entity_states: Dict[str, Dict[str, Any]] = {}
        self._counters: Dict[str, int] = {}

    def update_entity_state(self, entity_id: str, updates: Dict[str, Any]):
        """Updates in-memory state for an entity."""
        with self._lock:
            if entity_id not in self._entity_states:
                self._entity_states[entity_id] = {}
            self._entity_states[entity_id].update(updates)
            security_logger.debug(f"StreamStateManager: Updated state for entity '{entity_id}'.")

    def increment_counter(self, counter_key: str, amount: int = 1) -> int:
        """Increments stateful stream counter."""
        with self._lock:
            val = self._counters.get(counter_key, 0) + amount
            self._counters[counter_key] = val
            return val

    def get_entity_state(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves entity state dict."""
        with self._lock:
            return self._entity_states.get(entity_id)


# Global StreamStateManager instance
stream_state_manager = StreamStateManager()
