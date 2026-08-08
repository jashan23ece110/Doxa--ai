"""
Decision Memory for Enterprise Decision Platform.

Persists past decisions, outcomes, lessons learned, and execution history (`./decision_data/memory.json`).
"""

import json
import os
import threading
from typing import Dict, Any, List, Optional
from app.core.decision.decision_models import DecisionMemoryRecord
from app.core.logging import logger


class DecisionMemory:
    """Thread-safe disk storage manager for decision history."""

    def __init__(self, storage_dir: str = "./decision_data"):
        self.storage_dir = storage_dir
        self.file_path = os.path.join(storage_dir, "memory.json")
        self._lock = threading.Lock()
        self._records: Dict[str, DecisionMemoryRecord] = {}
        self._ensure_storage()

    def _ensure_storage(self) -> None:
        """Ensures storage directory exists."""
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir, exist_ok=True)
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        """Loads decision records from disk."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        rec = DecisionMemoryRecord.model_validate(item)
                        self._records[rec.record_id] = rec
                logger.info(f"DecisionMemory loaded {len(self._records)} decision records from disk.")
            except Exception as e:
                logger.error(f"Failed to load decision memory from disk: {e}")

    def _save_to_disk(self) -> None:
        """Saves decision records to disk."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([r.model_dump() for r in self._records.values()], f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save decision memory to disk: {e}")

    def record_decision(
        self,
        topic: str,
        action: str,
        outcome: str = "SUCCESS",
        lessons: Optional[List[str]] = None,
    ) -> DecisionMemoryRecord:
        """Records a decision outcome."""
        rec = DecisionMemoryRecord(
            decision_topic=topic,
            action_taken=action,
            outcome_status=outcome,
            lessons_learned=lessons or ["Execute parallel workers for faster throughput"],
        )
        with self._lock:
            self._records[rec.record_id] = rec
            self._save_to_disk()
            logger.info(f"DecisionMemory recorded decision '{rec.record_id}' for topic: '{topic}'.")

        return rec

    def list_records(self) -> List[DecisionMemoryRecord]:
        """Lists all decision records."""
        with self._lock:
            return list(self._records.values())


# Global DecisionMemory instance
decision_memory = DecisionMemory()
