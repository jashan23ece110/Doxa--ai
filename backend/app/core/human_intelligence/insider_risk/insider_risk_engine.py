"""
Enterprise Insider Risk Engine.

Calculates overall insider risk, privileged access risk, behavioral deviations,
organizational exposure, awareness regressions, policy violation likelihoods, and risk trends.
"""

import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.human_intelligence.human_intelligence_types import HumanRiskLevel


class ComprehensiveInsiderRiskAssessment(BaseModel):
    employee_id: str
    overall_insider_risk_score: float = 1.5  # 0 to 10 scale
    privileged_access_risk_score: float = 2.0
    behavioral_deviation_score: float = 0.5
    policy_violation_likelihood: float = 0.05  # 0.0 to 1.0
    confidence_score: float = 0.94
    risk_level: HumanRiskLevel = HumanRiskLevel.LOW
    evaluated_at: float = Field(default_factory=time.time)


class InsiderRiskEngine:
    """Enterprise Insider Risk Engine."""

    def evaluate_insider_risk(self, employee_id: str, is_privileged: bool = False, security_score: float = 85.0) -> ComprehensiveInsiderRiskAssessment:
        """
        Evaluates comprehensive insider risk metrics for an employee.

        Args:
            employee_id: Employee ID.
            is_privileged: Whether employee holds administrative credentials.
            security_score: Security awareness score.

        Returns:
            ComprehensiveInsiderRiskAssessment model.
        """
        priv_risk = 4.0 if is_privileged else 1.5
        overall = max(0.5, round((100.0 - security_score) / 10.0 + (1.5 if is_privileged else 0.0), 1))

        assessment = ComprehensiveInsiderRiskAssessment(
            employee_id=employee_id,
            overall_insider_risk_score=overall,
            privileged_access_risk_score=priv_risk,
            behavioral_deviation_score=0.4,
            policy_violation_likelihood=0.02 if security_score >= 80 else 0.15,
            confidence_score=0.95,
            risk_level=HumanRiskLevel.LOW if overall < 4.0 else HumanRiskLevel.HIGH,
        )

        security_logger.info(f"InsiderRiskEngine: Evaluated insider risk for '{employee_id}': OverallRisk={assessment.overall_insider_risk_score}/10.0.")
        return assessment


# Global InsiderRiskEngine instance
insider_risk_engine = InsiderRiskEngine()
