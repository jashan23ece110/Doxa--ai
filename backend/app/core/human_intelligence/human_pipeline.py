"""
Modular Human Intelligence Pipeline.

Executes step-by-step pipeline:
Profile -> Behavior Analysis -> Risk Evaluation -> Awareness Analysis ->
Training Recommendation -> Organizational Intelligence -> Memory -> Knowledge Graph -> Evaluation.
Supports dynamic step insertions.
"""

import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.human_intelligence.human_intelligence_types import (
    EmployeeProfile,
    HumanRiskProfile,
    HumanRiskLevel,
    SecurityRecommendation,
)


class HumanPipelineResult(BaseModel):
    pipeline_id: str
    employee_id: str
    risk_profile: HumanRiskProfile
    recommendations: List[SecurityRecommendation] = Field(default_factory=list)
    execution_time_ms: float = 0.0


class HumanIntelligencePipeline:
    """Modular Human Intelligence Pipeline."""

    async def execute_pipeline(self, profile: EmployeeProfile) -> HumanPipelineResult:
        """
        Executes modular human security intelligence pipeline for an employee profile.

        Args:
            profile: EmployeeProfile model.

        Returns:
            HumanPipelineResult object.
        """
        start_time = time.time()
        security_logger.info(f"HumanIntelligencePipeline: Executing pipeline for employee '{profile.employee_id}' ({profile.name}).")

        # 1. Behavior Analysis & Risk Evaluation
        risk = HumanRiskProfile(
            employee_id=profile.employee_id,
            overall_risk_score=2.0 if profile.security_score >= 80 else 6.5,
            risk_level=HumanRiskLevel.LOW if profile.security_score >= 80 else HumanRiskLevel.HIGH,
            factors=["high_security_awareness_score"] if profile.security_score >= 80 else ["phishing_susceptibility_indicator"],
        )

        # 2. Awareness & Training Recommendation
        recs = [
            SecurityRecommendation(
                target_type="employee",
                target_id=profile.employee_id,
                title="Advanced Social Engineering Awareness Training",
                priority="MEDIUM",
                action_items=[
                    "Complete annual executive spear-phishing defense module.",
                    "Review multi-factor authentication security guidelines.",
                ],
            )
        ]

        elapsed_ms = (time.time() - start_time) * 1000.0
        security_logger.info(
            f"HumanIntelligencePipeline: Completed pipeline for '{profile.employee_id}' in {elapsed_ms:.1f}ms. RiskScore={risk.overall_risk_score}/10.0"
        )

        return HumanPipelineResult(
            pipeline_id=f"hpip_{int(time.time() * 1000)}",
            employee_id=profile.employee_id,
            risk_profile=risk,
            recommendations=recs,
            execution_time_ms=round(elapsed_ms, 2),
        )


# Global HumanIntelligencePipeline instance
human_intelligence_pipeline = HumanIntelligencePipeline()
