"""
Behavioral Pattern Repository.

Stores historical behaviors, awareness evolution, assessment logs, learning milestones,
organizational interactions, and human risk history.
"""

import threading
import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.human_intelligence.human_intelligence_types import BehaviorPattern


class BehavioralHistoryRecord(BaseModel):
    record_id: str
    employee_id: str
    patterns: List[BehaviorPattern] = Field(default_factory=list)
    recorded_at: float = Field(default_factory=time.time)


class BehavioralPatternRepository:
    """Thread-safe Behavioral Pattern Repository."""

    def __init__(self):
        self._lock = threading.Lock()
        self._store: Dict[str, List[BehavioralHistoryRecord]] = {}

    def save_patterns(self, employee_id: str, patterns: List[BehaviorPattern]) -> BehavioralHistoryRecord:
        """Saves a historical behavioral observation record."""
        rec = BehavioralHistoryRecord(
            record_id=f"brec_{int(time.time() * 1000)}",
            employee_id=employee_id,
            patterns=patterns,
        )
        with self._lock:
            if employee_id not in self._store:
                self._store[employee_id] = []
            self._store[employee_id].append(rec)

        security_logger.debug(f"BehavioralPatternRepository: Saved {len(patterns)} patterns for '{employee_id}'.")
        return rec

    def get_history(self, employee_id: str) -> List[BehavioralHistoryRecord]:
        """Retrieves historical behavioral records."""
        with self._lock:
            return list(self._store.get(employee_id, []))


# Global BehavioralPatternRepository instance
behavioral_pattern_repository = BehavioralPatternRepository()
