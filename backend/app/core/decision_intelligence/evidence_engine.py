"""
Enterprise Decision Evidence Engine.

Ranks, corroborates, and evaluates decision evidence while distinguishing facts, inferences, predictions, and assumptions.
"""

from typing import Dict, Any, List
from app.core.logging import security_logger
from app.core.decision_intelligence.decision_types import DecisionEvidence


class EvidenceEngine:
    """Enterprise Decision Evidence Engine."""

    def evaluate_evidence_quality(self, evidences: List[DecisionEvidence]) -> float:
        """
        Calculates aggregate evidence quality score across collected evidence items.

        Args:
            evidences: List of DecisionEvidence objects.

        Returns:
            Aggregate evidence quality score (0.0 to 1.0).
        """
        if not evidences:
            return 0.50

        scores = [e.confidence_score for e in evidences]
        avg_score = round(sum(scores) / len(scores), 3)

        security_logger.info(f"EvidenceEngine: Evaluated {len(evidences)} evidence items -> Aggregate Quality={avg_score}.")
        return avg_score


# Global EvidenceEngine instance
evidence_engine = EvidenceEngine()
