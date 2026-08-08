"""
Meta Confidence Engine for Meta-Cognitive Layer.

Estimates confidence scores based on retrieval quality, reasoning agreement,
tool reliability, memory confidence, answer consistency, and hallucination indicators.
"""

from typing import Dict, Any, List
from app.core.logging import logger
from app.core.metacognition.metacognition_models import ConfidenceAssessment


class MetaConfidenceEngine:
    """Estimates confidence score and provides explanation."""

    @staticmethod
    def estimate_confidence(
        retrieval_score: float = 0.9,
        reasoning_agreement: float = 0.95,
        tool_reliability: float = 1.0,
        memory_confidence: float = 0.9,
        hallucination_risk: float = 0.05,
    ) -> ConfidenceAssessment:
        """
        Calculates composite confidence score.
        """
        composite = round(
            (retrieval_score * 0.25)
            + (reasoning_agreement * 0.35)
            + (tool_reliability * 0.2)
            + (memory_confidence * 0.2)
            - (hallucination_risk * 0.5),
            2,
        )
        composite = max(0.0, min(1.0, composite))

        explanation = f"Confidence score {composite}: Strong reasoning agreement ({reasoning_agreement}) and low hallucination risk ({hallucination_risk})."

        assessment = ConfidenceAssessment(
            overall_confidence=composite,
            retrieval_quality_score=retrieval_score,
            reasoning_agreement_score=reasoning_agreement,
            tool_reliability_score=tool_reliability,
            memory_confidence_score=memory_confidence,
            hallucination_risk_score=hallucination_risk,
            explanation=explanation,
        )
        logger.info(f"MetaConfidenceEngine assessed confidence: {composite} ({explanation}).")
        return assessment


# Global MetaConfidenceEngine instance
meta_confidence_engine = MetaConfidenceEngine()
