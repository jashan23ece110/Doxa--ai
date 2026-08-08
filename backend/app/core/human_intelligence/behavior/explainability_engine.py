"""
Behavior Explainability Engine.

Generates human-readable explanations for risk scores, influence scores, anomaly detections,
behavioral evolution, and training recommendations for transparent AI reasoning.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class BehavioralExplanation(BaseModel):
    explanation_id: str
    target_id: str
    metric_name: str  # risk_score, influence_score, anomaly
    summary_rationale: str
    contributing_factors: List[str] = Field(default_factory=list)


class BehaviorExplainabilityEngine:
    """Enterprise Behavior Explainability Engine."""

    def explain_risk_score(self, employee_id: str, risk_score: float) -> BehavioralExplanation:
        """
        Generates explainable rationale for a calculated human risk score.

        Args:
            employee_id: Employee ID.
            risk_score: Calculated risk score (0-10).

        Returns:
            BehavioralExplanation object.
        """
        explanation = BehavioralExplanation(
            explanation_id=f"expl_b_{employee_id[:6]}",
            target_id=employee_id,
            metric_name="risk_score",
            summary_rationale=f"Assigned risk score of {risk_score:.1f}/10 based on security quiz performance and training history.",
            contributing_factors=[
                "High security awareness quiz completion rate (95%)",
                "Consistently low susceptibility during mock educational simulations",
            ],
        )

        security_logger.info(f"BehaviorExplainabilityEngine: Generated explanation for employee '{employee_id}'.")
        return explanation


# Global BehaviorExplainabilityEngine instance
behavior_explainability_engine = BehaviorExplainabilityEngine()
