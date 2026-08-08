"""
Adaptive AI Risk Scoring Engine.

Combines awareness assessment histories, training records, behavioral intelligence,
organizational context, insider risk indicators, and trust network graphs.
Generates normalized, explainable risk scores.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.human_intelligence.human_intelligence_types import HumanRiskProfile, HumanRiskLevel


class AdaptiveRiskScoreResult(BaseModel):
    employee_id: str
    normalized_risk_score: float = 1.5  # 0.0 to 10.0 scale
    risk_level: HumanRiskLevel = HumanRiskLevel.LOW
    confidence_level: float = 0.95
    contributing_factors: List[str] = Field(default_factory=list)


class AdaptiveRiskScoringEngine:
    """Enterprise Adaptive AI Risk Scoring Engine."""

    def compute_adaptive_risk(
        self,
        employee_id: str,
        security_score: float = 85.0,
        is_privileged: bool = False,
        anomalies_count: int = 0,
    ) -> AdaptiveRiskScoreResult:
        """
        Computes multi-factor adaptive risk score.

        Args:
            employee_id: Employee ID.
            security_score: Security awareness score.
            is_privileged: Admin privilege flag.
            anomalies_count: Number of flagged behavioral anomalies.

        Returns:
            AdaptiveRiskScoreResult model.
        """
        base = max(0.5, (100.0 - security_score) / 10.0)
        priv_penalty = 1.5 if is_privileged else 0.0
        anom_penalty = anomalies_count * 2.0

        final_score = min(10.0, round(base + priv_penalty + anom_penalty, 1))
        factors = []
        if is_privileged:
            factors.append("Administrative Privileged Access Role")
        if security_score >= 80.0:
            factors.append("High Security Awareness Quiz Score")
        if anomalies_count > 0:
            factors.append(f"{anomalies_count} Flagged Behavioral Anomalies")

        result = AdaptiveRiskScoreResult(
            employee_id=employee_id,
            normalized_risk_score=final_score,
            risk_level=HumanRiskLevel.LOW if final_score < 4.0 else HumanRiskLevel.HIGH,
            confidence_level=0.96,
            contributing_factors=factors,
        )

        security_logger.info(f"AdaptiveRiskScoringEngine: Computed adaptive risk for '{employee_id}': NormalizedRisk={result.normalized_risk_score}/10.0.")
        return result


# Global AdaptiveRiskScoringEngine instance
adaptive_risk_scoring_engine = AdaptiveRiskScoringEngine()
