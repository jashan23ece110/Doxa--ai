"""
Analytics Explainability Engine.

Generates human-readable and structured explainability metadata for anomaly detections,
correlations, forecasts, predictions, and statistical aggregations.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class AnalyticalExplanation(BaseModel):
    explanation_id: str
    target_result_id: str
    summary_reasoning: str
    contributing_features: List[str] = Field(default_factory=list)
    confidence_level: float = 0.95
    provenance_reference_ids: List[str] = Field(default_factory=list)


class AnalyticsExplainabilityEngine:
    """Enterprise Analytics Explainability Engine."""

    def explain_result(self, result_id: str, result_type: str, evidence_items: List[str]) -> AnalyticalExplanation:
        """
        Generates explainability metadata for an analytical output.

        Args:
            result_id: Target result identifier.
            result_type: Category string (anomaly, correlation, forecast, prediction).
            evidence_items: Supporting evidence items list.

        Returns:
            AnalyticalExplanation object.
        """
        expl = AnalyticalExplanation(
            explanation_id=f"expl_{result_id[:6]}",
            target_result_id=result_id,
            summary_reasoning=f"Generated explanation for {result_type} '{result_id}' based on {len(evidence_items)} evidence features.",
            contributing_features=evidence_items,
            confidence_level=0.96,
        )

        security_logger.info(f"AnalyticsExplainabilityEngine: Generated explanation for '{result_id}' (Type={result_type}).")
        return expl


# Global AnalyticsExplainabilityEngine instance
analytics_explainability_engine = AnalyticsExplainabilityEngine()
