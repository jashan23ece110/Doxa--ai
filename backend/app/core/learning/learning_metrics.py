"""
Learning Metrics Tracker for Enterprise Continuous Learning Layer.

Tracks learning records, feedback counts, positive/negative feedback rates,
retrieval recommendations, tool recommendations, and knowledge recommendations.
"""

import threading
import time
from typing import Dict, Any, List


class LearningMetricsTracker:
    """Thread-safe metrics tracker for continuous learning layer."""

    def __init__(self):
        self._lock = threading.Lock()
        self.learning_records_processed: int = 0
        self.total_feedback_count: int = 0
        self.positive_feedback_count: int = 0
        self.negative_feedback_count: int = 0
        self.retrieval_recommendations_count: int = 0
        self.tool_recommendations_count: int = 0
        self.knowledge_recommendations_count: int = 0

    def record_feedback_signal(self, is_positive: bool = True) -> None:
        """Records a user or system feedback signal."""
        with self._lock:
            self.total_feedback_count += 1
            if is_positive:
                self.positive_feedback_count += 1
            else:
                self.negative_feedback_count += 1

    def record_learning_record(self) -> None:
        """Records a processed learning record."""
        with self._lock:
            self.learning_records_processed += 1

    def record_recommendation(self, category: str = "retrieval") -> None:
        """Records a generated recommendation count."""
        with self._lock:
            if category == "retrieval":
                self.retrieval_recommendations_count += 1
            elif category == "tool":
                self.tool_recommendations_count += 1
            elif category == "knowledge":
                self.knowledge_recommendations_count += 1

    def get_summary(self) -> Dict[str, Any]:
        """Returns summary statistics across continuous learning operations."""
        with self._lock:
            pos_rate = (
                round(self.positive_feedback_count / self.total_feedback_count, 4)
                if self.total_feedback_count > 0
                else 1.0
            )
            neg_rate = (
                round(self.negative_feedback_count / self.total_feedback_count, 4)
                if self.total_feedback_count > 0
                else 0.0
            )

            return {
                "learning_records": self.learning_records_processed,
                "feedback_count": self.total_feedback_count,
                "positive_feedback_count": self.positive_feedback_count,
                "negative_feedback_count": self.negative_feedback_count,
                "positive_feedback_rate": pos_rate,
                "negative_feedback_rate": neg_rate,
                "retrieval_recommendations": self.retrieval_recommendations_count,
                "tool_recommendations": self.tool_recommendations_count,
                "knowledge_recommendations": self.knowledge_recommendations_count,
            }


# Global LearningMetricsTracker instance
learning_metrics_tracker = LearningMetricsTracker()
