"""
Decision Lifecycle Manager.

Manages complete decision lifecycles from creation through governance, approval, and archival.
"""

import threading
import time
from typing import Dict, Any
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class DecisionLifecycleRecord(BaseModel):
    decision_id: str
    stage: str = "CREATED"  # CREATED, ANALYZED, APPROVED, EXECUTED, ARCHIVED
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)


class DecisionLifecycleManager:
    """Thread-safe Decision Lifecycle Manager."""

    def __init__(self):
        self._lock = threading.Lock()
        self._records: Dict[str, DecisionLifecycleRecord] = {}

    def initialize_lifecycle(self, decision_id: str) -> DecisionLifecycleRecord:
        """Initializes a new decision lifecycle record."""
        rec = DecisionLifecycleRecord(decision_id=decision_id)
        with self._lock:
            self._records[decision_id] = rec
            security_logger.info(f"DecisionLifecycleManager: Initialized lifecycle for '{decision_id}'.")
        return rec

    def transition_stage(self, decision_id: str, new_stage: str) -> DecisionLifecycleRecord:
        """Transitions decision lifecycle to a new stage."""
        with self._lock:
            if decision_id in self._records:
                rec = self._records[decision_id]
                rec.stage = new_stage
                rec.updated_at = time.time()
                security_logger.info(f"DecisionLifecycleManager: Transitioned '{decision_id}' to '{new_stage}'.")
                return rec
            rec_new = DecisionLifecycleRecord(decision_id=decision_id, stage=new_stage)
            self._records[decision_id] = rec_new
            return rec_new


# Global DecisionLifecycleManager instance
decision_lifecycle_manager = DecisionLifecycleManager()
