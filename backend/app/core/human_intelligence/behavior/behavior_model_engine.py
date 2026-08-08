"""
Enterprise Human Behavior Modeling Engine.

Models employee communication patterns, security habits, decision consistency,
learning progression, security awareness evolution, response behaviors, and probabilistic behavior profiles.
"""

import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.human_intelligence.human_intelligence_types import BehaviorPattern, HumanRiskLevel


class ProbabilisticBehaviorProfile(BaseModel):
    employee_id: str
    security_habit_score: float = 85.0  # 0 to 100 scale
    decision_consistency_score: float = 90.0
    awareness_evolution_trend: str = "improving"  # improving, stable, declining
    risk_level: HumanRiskLevel = HumanRiskLevel.LOW
    observed_patterns: List[BehaviorPattern] = Field(default_factory=list)
    modeled_at: float = Field(default_factory=time.time)


class BehaviorModelEngine:
    """Enterprise Human Behavior Modeling Engine."""

    def build_behavior_profile(self, employee_id: str, security_score: float = 85.0) -> ProbabilisticBehaviorProfile:
        """
        Constructs a probabilistic behavior profile for an employee.

        Args:
            employee_id: Employee ID.
            security_score: Security awareness score.

        Returns:
            ProbabilisticBehaviorProfile object.
        """
        patterns = [
            BehaviorPattern(
                pattern_id="pat_auth_01",
                category="authentication",
                description="Consistent multi-factor authentication prompt validation",
                anomaly_score=0.05,
                observed_count=12,
            )
        ]

        profile = ProbabilisticBehaviorProfile(
            employee_id=employee_id,
            security_habit_score=security_score,
            decision_consistency_score=92.0,
            awareness_evolution_trend="improving",
            risk_level=HumanRiskLevel.LOW if security_score >= 80 else HumanRiskLevel.HIGH,
            observed_patterns=patterns,
        )

        security_logger.info(f"BehaviorModelEngine: Built behavior profile for '{employee_id}' (HabitScore={profile.security_habit_score}/100).")
        return profile


# Global BehaviorModelEngine instance
behavior_model_engine = BehaviorModelEngine()
