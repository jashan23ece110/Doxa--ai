"""
Global Enterprise Human Intelligence Platform.

Central master orchestrator unifying every Stage 7 Human Intelligence subsystem into a single
production-grade enterprise security intelligence ecosystem.
"""

import time
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.human_intelligence.human_intelligence_manager import enterprise_human_intelligence_manager
from app.core.human_intelligence.awareness import campaign_manager, phishing_simulation_engine, assessment_engine
from app.core.human_intelligence.behavior import behavior_model_engine, influence_analysis_engine
from app.core.human_intelligence.insider_risk import insider_risk_engine, privileged_access_analyzer
from app.core.human_intelligence.training import adaptive_learning_engine, behavior_improvement_engine
from app.core.human_intelligence.red_team import human_attack_surface_engine, red_team_simulation_engine, resilience_engine
from app.core.human_intelligence.organization import organizational_intelligence_engine, human_intelligence_fusion_engine
from app.core.human_intelligence.platform.human_service_bus import human_service_bus
from app.core.human_intelligence.platform.human_workflow_engine import human_workflow_engine
from app.core.human_intelligence.platform.human_readiness_validator import human_readiness_validator
from app.core.human_intelligence.platform.human_lifecycle import human_lifecycle_manager


class EnterpriseHumanIntelligenceAssessment(BaseModel):
    assessment_id: str
    target_scope: str = "Enterprise"
    overall_human_security_score: float = 89.5  # 0 to 100
    overall_insider_risk_score: float = 1.5      # 0 to 10 scale (lower is better)
    human_attack_surface_score: float = 3.2     # 0 to 10 scale (lower is better)
    overall_resilience_level: str = "FORTIFIED"
    readiness_score: int = 100
    evaluated_at: float = Field(default_factory=time.time)


class EnterpriseHumanIntelligencePlatform:
    """Master Enterprise Human Intelligence Platform Orchestrator."""

    def __init__(self):
        human_lifecycle_manager.initialize()

    async def run_master_human_intelligence_assessment(self, scope_id: str = "Enterprise") -> EnterpriseHumanIntelligenceAssessment:
        """
        Executes an end-to-end master human intelligence assessment across all Stage 7 subsystems.

        Args:
            scope_id: Scope identifier (employee_id, department, or 'Enterprise').

        Returns:
            EnterpriseHumanIntelligenceAssessment model.
        """
        security_logger.info(f"EnterpriseHumanIntelligencePlatform: Initiating master human intelligence assessment for '{scope_id}'.")

        # 1. Evaluate awareness baseline
        camp_metrics = campaign_manager.get_campaign("camp_all") or campaign_manager.create_campaign("Enterprise Security Awareness", scope_id)
        
        # 2. Evaluate behavior profile & influence
        behavior_prof = behavior_model_engine.build_behavior_profile(scope_id)
        inf_metrics = influence_analysis_engine.analyze_influence(scope_id)

        # 3. Evaluate insider risk & privileges
        ins_assess = insider_risk_engine.evaluate_insider_risk(scope_id)

        # 4. Evaluate resilience & attack surface
        surface = human_attack_surface_engine.analyze_attack_surface(scope_id)
        resilience = resilience_engine.calculate_resilience(scope_id)

        # 5. Fuse intelligence
        fused = human_intelligence_fusion_engine.fuse_intelligence(scope_id)

        # 6. Readiness check
        val = human_readiness_validator.validate_readiness()

        assessment = EnterpriseHumanIntelligenceAssessment(
            assessment_id=f"ehi_{int(time.time() * 1000)}",
            target_scope=scope_id,
            overall_human_security_score=behavior_prof.security_habit_score,
            overall_insider_risk_score=ins_assess.overall_insider_risk_score,
            human_attack_surface_score=surface.overall_attack_surface_score,
            overall_resilience_level=resilience.resilience_level,
            readiness_score=val["readiness_score"],
        )

        security_logger.info(f"EnterpriseHumanIntelligencePlatform: Completed master assessment for '{scope_id}' (Score={assessment.overall_human_security_score}/100, Risk={assessment.overall_insider_risk_score}/10.0).")
        return assessment


# Global EnterpriseHumanIntelligencePlatform instance
enterprise_human_intelligence_platform = EnterpriseHumanIntelligencePlatform()
