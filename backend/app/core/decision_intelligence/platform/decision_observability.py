"""
Decision Observability Engine.

Tracks real-time telemetry metrics for active decision pipelines, execution latency, and accuracy metrics.
"""

from typing import Dict, Any
from app.core.logging import security_logger


class DecisionObservability:
    """Decision Observability Engine."""

    def record_decision_telemetry(self, decision_id: str, latency_ms: float, confidence_score: float) -> Dict[str, Any]:
        """
        Records decision execution telemetry.

        Args:
            decision_id: Decision ID string.
            latency_ms: Execution duration in ms.
            confidence_score: System confidence score float.

        Returns:
            Dictionary containing recorded telemetry metrics.
        """
        metrics = {
            "decision_id": decision_id,
            "latency_ms": round(latency_ms, 2),
            "confidence_score": confidence_score,
            "observability_logged": True,
        }

        security_logger.info(f"DecisionObservability: Logged telemetry for '{decision_id}' (Latency={latency_ms}ms, Confidence={confidence_score}).")
        return metrics


# Global DecisionObservability instance
decision_observability = DecisionObservability()
