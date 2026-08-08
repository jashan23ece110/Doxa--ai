"""
Internal Reasoning Confidence Estimator.

Calculates internal reasoning confidence scores (0.0 - 1.0) based on retrieval scores,
memory grounding, and evidence coverage without exposing confidence metrics externally.
"""

from typing import List, Dict, Any


class ConfidenceEstimator:
    """Calculates internal reasoning confidence scores."""

    @staticmethod
    def estimate_confidence(
        contexts: List[Dict[str, Any]],
        evidence_verification: Dict[str, Any],
        contradictions: List[Dict[str, str]],
    ) -> float:
        """Calculates overall reasoning confidence score."""
        score = 0.60

        # High top retrieval score bonus
        if contexts:
            top_score = contexts[0].get("cross_encoder_score", contexts[0].get("similarity", 0.5))
            score += min(top_score * 0.25, 0.25)

        # Grounded ratio bonus
        grounded_ratio = evidence_verification.get("grounded_ratio", 0.5)
        score += grounded_ratio * 0.15

        # Contradiction penalty
        if contradictions:
            score -= 0.20

        return min(max(round(score, 2), 0.0), 1.0)


# Global ConfidenceEstimator instance
confidence_estimator = ConfidenceEstimator()
