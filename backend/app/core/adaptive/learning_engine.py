"""
Learning Engine for Enterprise Self-Learning & Adaptive Intelligence Engine.

Aggregates execution statistics and persists optimization weights to disk (./adaptive_data/learning_stats.json).
Never stores sensitive user prompts or chain-of-thought traces.
"""

import json
import os
import threading
from typing import Dict, Any, List, Optional
from app.core.adaptive.adaptive_metrics import adaptive_metrics_tracker
from app.core.adaptive.feedback_engine import feedback_engine, FeedbackSignal
from app.core.logging import logger


class LearningEngine:
    """Asynchronously aggregates statistics and persists optimization weights."""

    def __init__(self, file_path: str = "./adaptive_data/learning_stats.json"):
        self.file_path = file_path
        self._lock = threading.Lock()
        self.stats: Dict[str, Any] = {
            "strategy_success_counts": {},
            "model_success_counts": {},
            "avg_retrieval_similarity": 0.80,
            "total_signals_processed": 0,
            "learned_dense_weight": 0.50,
            "learned_bm25_weight": 0.50,
        }
        self._ensure_storage_dir()
        self._load_from_disk()

    def _ensure_storage_dir(self) -> None:
        """Ensures storage directory exists."""
        dir_path = os.path.dirname(self.file_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

    def _load_from_disk(self) -> None:
        """Loads learning statistics from disk."""
        if not os.path.exists(self.file_path):
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.stats.update(data)
            logger.info(f"Loaded learning statistics from disk ({self.file_path}).")
        except Exception as e:
            logger.error(f"Failed to load learning statistics from disk ({e}).")

    def _save_to_disk(self) -> None:
        """Saves learning statistics to disk."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save learning statistics to disk: {e}")

    def process_feedback_batch(self) -> int:
        """Processes recent buffered feedback signals to update optimization weights."""
        signals = feedback_engine.get_recent_signals(limit=200)
        if not signals:
            return 0

        with self._lock:
            for sig in signals:
                self.stats["total_signals_processed"] += 1
                strat = sig.strategy_used
                self.stats["strategy_success_counts"][strat] = (
                    self.stats["strategy_success_counts"].get(strat, 0) + (1 if sig.verification_passed else 0)
                )

            # Adaptive dense/bm25 weight tuning
            avg_sim = sum(s.retrieval_similarity for s in signals) / len(signals)
            self.stats["avg_retrieval_similarity"] = round(avg_sim, 3)

            if avg_sim > 0.75:
                # Dense vector retrieval is performing strongly
                self.stats["learned_dense_weight"] = 0.55
                self.stats["learned_bm25_weight"] = 0.45
            else:
                # Increase BM25 keyword weight to boost recall
                self.stats["learned_dense_weight"] = 0.45
                self.stats["learned_bm25_weight"] = 0.55

            self._save_to_disk()
            adaptive_metrics_tracker.record_learning_iteration(optimizations=1)
            logger.info(f"LearningEngine processed batch of {len(signals)} feedback signals.")
            return len(signals)


# Global LearningEngine instance
learning_engine = LearningEngine()
