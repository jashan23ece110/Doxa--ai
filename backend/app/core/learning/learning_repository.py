"""
JSON Learning Repository for Enterprise Continuous Learning Layer.

Persists LearningRecord data (successful retrievals, successful/failed prompts,
retrieval failures, hallucination reports, tool failures, memory misses, and conversation outcomes) to disk.
"""

import json
import os
import threading
import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.config import settings
from app.core.logging import logger


class LearningRecord(BaseModel):
    """Container for a completed conversation learning record."""

    record_id: str
    conversation_id: str
    user_id: str = "default_user"
    prompt_text: str
    successful_retrieval: bool = True
    retrieval_similarity: float = 0.80
    successful_prompt: bool = True
    hallucination_detected: bool = False
    tool_failures: List[str] = Field(default_factory=list)
    memory_misses: bool = False
    quality_score: float = 0.85
    response_latency_ms: float = 0.0
    timestamp: float = Field(default_factory=time.time)


class JSONLearningRepository:
    """Thread-safe JSON repository for learning records persistence."""

    def __init__(self, file_path: str = "./learning_data/learning_records.json"):
        self.file_path = file_path
        self._lock = threading.Lock()
        self._records: List[LearningRecord] = []
        self._ensure_storage_dir()
        self._load_from_disk()

    def _ensure_storage_dir(self) -> None:
        """Ensures storage directory exists."""
        dir_path = os.path.dirname(self.file_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

    def _load_from_disk(self) -> None:
        """Loads learning records from disk."""
        if not os.path.exists(self.file_path):
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            for item in data:
                self._records.append(LearningRecord.model_validate(item))

            logger.info(f"Loaded {len(self._records)} learning records from disk ({self.file_path}).")
        except Exception as e:
            logger.error(f"Failed to load learning records from disk: {e}")

    def _save_to_disk(self) -> None:
        """Saves learning records to disk."""
        try:
            data = [rec.model_dump() for rec in self._records]
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save learning records to disk: {e}")

    def save_record(self, record: LearningRecord) -> None:
        """Saves a learning record to repository."""
        with self._lock:
            self._records.append(record)
            limit = getattr(settings, "LEARNING_HISTORY_LIMIT", 5000)
            if len(self._records) > limit:
                self._records = self._records[-limit:]
            self._save_to_disk()

    def get_all_records(self) -> List[LearningRecord]:
        """Returns all stored learning records."""
        with self._lock:
            return list(self._records)


# Global JSONLearningRepository instance
learning_repository = JSONLearningRepository()
