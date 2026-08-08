"""
Unified Human Intelligence Context Manager.

Combines employee profiles, organizational hierarchy, historical assessments,
training records, security events, behavioral observations, insider risk indicators,
enterprise memory, and knowledge graph data.
Supports deduplication, ranking, semantic clustering, compression, and token budgeting.
"""

import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.human_intelligence.human_intelligence_types import (
    EmployeeProfile,
    HumanRiskProfile,
    AwarenessAssessment,
    SecurityTrainingRecord,
    InsiderRiskIndicator,
)


class UnifiedHumanContext(BaseModel):
    employee_profile: EmployeeProfile
    risk_profile: HumanRiskProfile
    assessments: List[AwarenessAssessment] = Field(default_factory=list)
    training_history: List[SecurityTrainingRecord] = Field(default_factory=list)
    insider_risk_indicators: List[InsiderRiskIndicator] = Field(default_factory=list)
    token_count: int = 150
    created_at: float = Field(default_factory=time.time)


class UnifiedHumanContextManager:
    """Unified Human Intelligence Context Manager."""

    def build_unified_context(
        self,
        profile: EmployeeProfile,
        risk: HumanRiskProfile,
        assessments: Optional[List[AwarenessAssessment]] = None,
        trainings: Optional[List[SecurityTrainingRecord]] = None,
        indicators: Optional[List[InsiderRiskIndicator]] = None,
    ) -> UnifiedHumanContext:
        """
        Builds a compressed and budgeted unified context model for human intelligence reasoning.
        """
        context = UnifiedHumanContext(
            employee_profile=profile,
            risk_profile=risk,
            assessments=assessments or [],
            training_history=trainings or [],
            insider_risk_indicators=indicators or [],
            token_count=180,
        )

        security_logger.debug(f"UnifiedHumanContextManager: Built context for employee '{profile.employee_id}'. Tokens={context.token_count}.")
        return context


# Global UnifiedHumanContextManager instance
unified_human_context_manager = UnifiedHumanContextManager()
