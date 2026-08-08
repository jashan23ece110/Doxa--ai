"""
Evaluation Storage & Benchmark Manager.

Manages thread-safe storage of evaluation metric records, JSON disk persistence,
golden QA benchmark datasets, and experiment A/B configuration wrappers.
"""

import json
import os
import threading
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.logging import logger


class EvaluationStorage:
    """Thread-safe evaluation storage and disk persistence manager."""

    def __init__(self, persistence_path: Optional[str] = None):
        self.persistence_path = persistence_path or settings.EVAL_STORE_PATH
        self._lock = threading.Lock()
        self.metric_records: List[Dict[str, Any]] = []
        self._load_from_disk()

    def _save_to_disk(self) -> None:
        """Persists evaluation records to JSON file."""
        if not self.persistence_path:
            return
        try:
            parent_dir = Path(self.persistence_path).parent
            parent_dir.mkdir(parents=True, exist_ok=True)
            with open(self.persistence_path, "w", encoding="utf-8") as f:
                json.dump(self.metric_records[-settings.MAX_METRIC_HISTORY:], f, ensure_ascii=False)
            logger.debug(f"Persisted {len(self.metric_records)} evaluation records to disk.")
        except Exception as e:
            logger.error(f"Failed to persist evaluation records to disk: {e}")

    def _load_from_disk(self) -> None:
        """Loads evaluation records from JSON file."""
        if not self.persistence_path or not os.path.exists(self.persistence_path):
            return
        try:
            with open(self.persistence_path, "r", encoding="utf-8") as f:
                self.metric_records = json.load(f)
            logger.info(f"Loaded {len(self.metric_records)} evaluation records from disk.")
        except Exception as e:
            logger.warning(f"Failed to load evaluation records from disk: {e}")

    def add_evaluation_record(self, record: Dict[str, Any]) -> None:
        """Adds an evaluation record thread-safely."""
        with self._lock:
            record["timestamp"] = time.time()
            self.metric_records.append(record)
            if len(self.metric_records) > settings.MAX_METRIC_HISTORY:
                self.metric_records = self.metric_records[-settings.MAX_METRIC_HISTORY:]
            self._save_to_disk()

    def get_summary_statistics(self) -> Dict[str, Any]:
        """Calculates aggregated summary statistics across evaluation records."""
        with self._lock:
            if not self.metric_records:
                return {"records_count": 0, "avg_overall_score": 0.0, "avg_latency_ms": 0.0}

            total_records = len(self.metric_records)
            scores = [r.get("overall_pipeline_score", 0.0) for r in self.metric_records]
            latencies = [r.get("total_latency_ms", 0.0) for r in self.metric_records]

            avg_score = round(sum(scores) / total_records, 2)
            avg_lat = round(sum(latencies) / total_records, 2)

            return {
                "records_count": total_records,
                "avg_overall_score": avg_score,
                "avg_latency_ms": avg_lat,
            }


# Global EvaluationStorage instance
eval_storage = EvaluationStorage()
