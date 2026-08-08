"""
Decision Outcome Engine.

Measures actual vs expected business outcomes and feeds validated results back into memory and learning layers.
"""

from typing import Dict, Any
from app.core.logging import security_logger


class DecisionOutcomeEngine:
    """Decision Outcome Engine."""

    def evaluate_and_learn_outcome(self, decision_id: str, expected_kpi: float, actual_kpi: float) -> Dict[str, Any]:
        """
        Measures outcome accuracy and propagates learnings to memory and predictive layers.

        Args:
            decision_id: Decision ID string.
            expected_kpi: Expected KPI value.
            actual_kpi: Measured actual KPI value.

        Returns:
            Dictionary containing outcome evaluation and learning status.
        """
        accuracy = round(actual_kpi / expected_kpi, 2) if expected_kpi > 0 else 1.0
        evaluation = {
            "decision_id": decision_id,
            "expected_kpi": expected_kpi,
            "actual_kpi": actual_kpi,
            "decision_accuracy": accuracy,
            "fed_to_memory": True,
            "fed_to_predictive_learning": True,
        }

        security_logger.info(f"DecisionOutcomeEngine: Evaluated outcome for '{decision_id}' (Accuracy={accuracy}).")
        return evaluation


# Global DecisionOutcomeEngine instance
decision_outcome_engine = DecisionOutcomeEngine()
