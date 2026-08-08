"""
Recommendation Outcome Monitor.

Tracks post-execution outcome metrics and feeds validated results back into the Decision Intelligence learning layer.
"""

from typing import Dict, Any
from app.core.logging import security_logger


class RecommendationMonitor:
    """Recommendation Outcome Monitor."""

    def record_recommendation_outcome(self, recommendation_id: str, expected_benefit: float, actual_benefit: float) -> Dict[str, Any]:
        """
        Records actual vs expected recommendation outcome metrics.

        Args:
            recommendation_id: Target recommendation ID string.
            expected_benefit: Expected benefit float.
            actual_benefit: Measured actual benefit float.

        Returns:
            Dictionary containing accuracy and feedback metrics.
        """
        accuracy = round(actual_benefit / expected_benefit, 2) if expected_benefit > 0 else 1.0
        result = {
            "recommendation_id": recommendation_id,
            "expected_benefit": expected_benefit,
            "actual_benefit": actual_benefit,
            "recommendation_accuracy": accuracy,
            "feedback_recorded": True,
        }

        security_logger.info(f"RecommendationMonitor: Recorded outcome for '{recommendation_id}' (Accuracy={accuracy}).")
        return result


# Global RecommendationMonitor instance
recommendation_monitor = RecommendationMonitor()
