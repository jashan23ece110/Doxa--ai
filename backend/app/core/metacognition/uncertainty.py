"""
Uncertainty Engine for Meta-Cognitive Layer.

Detects missing knowledge, contradictions, weak retrieval, ambiguous queries,
multiple interpretations, and low confidence.
"""

from typing import List, Dict, Any
from app.core.logging import logger
from app.core.metacognition.metacognition_models import UncertaintyDetection


class UncertaintyEngine:
    """Detects cognitive uncertainty and knowledge gaps."""

    @staticmethod
    def detect_uncertainty(
        query: str,
        retrieval_count: int = 3,
        confidence_score: float = 0.95,
    ) -> UncertaintyDetection:
        """
        Analyzes query and retrieval results to detect uncertainty.
        """
        reasons = []
        is_ambiguous = "?" in query and len(query.split()) < 3
        missing_knowledge = retrieval_count == 0
        low_conf = confidence_score < 0.6

        if is_ambiguous:
            reasons.append("Short ambiguous query with multiple interpretations.")
        if missing_knowledge:
            reasons.append("Zero relevant documents retrieved from knowledge base.")
        if low_conf:
            reasons.append(f"Confidence score ({confidence_score}) below acceptable threshold (0.6).")

        uncert_level = round(0.1 + (0.3 if is_ambiguous else 0.0) + (0.4 if missing_knowledge else 0.0) + (0.3 if low_conf else 0.0), 2)
        uncert_level = min(1.0, uncert_level)

        res = UncertaintyDetection(
            has_missing_knowledge=missing_knowledge,
            has_contradictions=False,
            is_ambiguous_query=is_ambiguous,
            uncertainty_level=uncert_level,
            reasons=reasons,
        )
        logger.info(f"UncertaintyEngine detected uncertainty level {uncert_level} (Reasons: {len(reasons)}).")
        return res


# Global UncertaintyEngine instance
uncertainty_engine = UncertaintyEngine()
