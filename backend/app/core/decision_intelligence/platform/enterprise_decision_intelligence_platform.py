"""
Global Enterprise Decision Intelligence Platform Facade.

Master entry point unifying Stage 10 Parts 1-7 into a single asynchronous enterprise facade.
"""

import time
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.decision_intelligence.decision_intelligence_orchestrator import decision_intelligence_orchestrator
from app.core.decision_intelligence.strategy.strategic_orchestrator import strategic_orchestrator
from app.core.decision_intelligence.risk.risk_intelligence_orchestrator import risk_intelligence_orchestrator
from app.core.decision_intelligence.prediction.predictive_decision_orchestrator import predictive_decision_orchestrator
from app.core.decision_intelligence.optimization.optimization_orchestrator import optimization_orchestrator
from app.core.decision_intelligence.governance.decision_explanation_engine import decision_explanation_engine
from app.core.decision_intelligence.executive.executive_decision_orchestrator import executive_decision_orchestrator


class MasterPlatformDecisionAssessment(BaseModel):
    platform_assessment_id: str = Field(default_factory=lambda: f"mpdec_{int(time.time() * 1000)}")
    request_title: str
    decision_foundation: Dict[str, Any] = Field(default_factory=dict)
    strategic_analysis: Dict[str, Any] = Field(default_factory=dict)
    risk_intelligence: Dict[str, Any] = Field(default_factory=dict)
    predictive_decision: Dict[str, Any] = Field(default_factory=dict)
    optimization_solution: Dict[str, Any] = Field(default_factory=dict)
    explanation: Dict[str, Any] = Field(default_factory=dict)
    executive_brief: Dict[str, Any] = Field(default_factory=dict)
    platform_readiness_score: float = 100.0
    status: str = "COMPLETED"
    executed_at: float = Field(default_factory=time.time)


class EnterpriseDecisionIntelligencePlatform:
    """Master Global Enterprise Decision Intelligence Platform Facade."""

    async def execute_master_decision_intelligence_pipeline(self, title: str, description: str = "") -> MasterPlatformDecisionAssessment:
        """
        Executes end-to-end master decision intelligence pipeline across Stage 10 Parts 1-7.

        Args:
            title: Decision title string.
            description: Detailed decision context string.

        Returns:
            MasterPlatformDecisionAssessment object.
        """
        t0 = time.time()
        security_logger.info(f"EnterpriseDecisionIntelligencePlatform: Initiating master decision intelligence pipeline for '{title}'.")

        # Part 1: Decision Intelligence Foundation
        d_res = await decision_intelligence_orchestrator.execute_decision_analysis(title, description)

        # Part 2: Strategic Planning
        s_res = await strategic_orchestrator.execute_strategic_analysis(title)

        # Part 3: Risk Intelligence
        r_res = await risk_intelligence_orchestrator.execute_risk_assessment(title)

        # Part 4: Predictive Decision
        p_res = await predictive_decision_orchestrator.execute_predictive_analysis(title)

        # Part 5: Optimization Engine
        o_res = await optimization_orchestrator.execute_optimization_analysis(title)

        # Part 6: Explainability & Governance
        expl = decision_explanation_engine.generate_explanation(d_res.decision_id, title)

        # Part 7: Executive Decision Support
        e_res = await executive_decision_orchestrator.execute_executive_analysis(title)

        assessment = MasterPlatformDecisionAssessment(
            request_title=title,
            decision_foundation={"decision_id": d_res.decision_id, "confidence_score": d_res.confidence.overall_confidence},
            strategic_analysis={"strategic_plan_id": s_res.analysis_id, "strategic_fit": s_res.evaluation.overall_strategic_fit},
            risk_intelligence={"assessment_id": r_res.assessment_id, "risk_score": r_res.assessment.overall_risk_score},
            predictive_decision={"prediction_id": p_res.analysis_id, "predicted_value": p_res.prediction.predicted_value},
            optimization_solution={"optimization_id": o_res.analysis_id, "efficiency": o_res.allocation_plan.efficiency_score},
            explanation={"explanation_id": expl.explanation_id, "rationale": expl.summary_rationale},
            executive_brief={"brief_id": e_res.brief.brief_id, "auth_level": e_res.authorization_level},
            platform_readiness_score=100.0,
            status="COMPLETED",
        )

        security_logger.info(f"EnterpriseDecisionIntelligencePlatform: Completed master pipeline for '{title}' in {round((time.time() - t0)*1000, 2)}ms.")
        return assessment


# Global EnterpriseDecisionIntelligencePlatform instance
enterprise_decision_intelligence_platform = EnterpriseDecisionIntelligencePlatform()
