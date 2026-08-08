"""
Enterprise Adaptive Learning Engine.

Generates personalized learning paths, adaptive difficulty modules, role-based learning curricula,
competency progression paths, and continuous refresher schedules.
"""

import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class LearningPathModule(BaseModel):
    module_id: str
    title: str
    difficulty_level: str = "medium"  # beginner, medium, advanced, expert
    estimated_minutes: int = 15
    prerequisites: List[str] = Field(default_factory=list)


class PersonalizedLearningPath(BaseModel):
    path_id: str
    employee_id: str
    role: str
    competency_target: str = "Advanced Security Awareness"
    assigned_modules: List[LearningPathModule] = Field(default_factory=list)
    created_at: float = Field(default_factory=time.time)


class AdaptiveLearningEngine:
    """Enterprise Adaptive Learning Engine."""

    def build_personalized_path(self, employee_id: str, role: str = "Standard", security_score: float = 85.0) -> PersonalizedLearningPath:
        """
        Builds a role-tailored adaptive learning path based on security score.

        Args:
            employee_id: Employee ID.
            role: Assigned role name.
            security_score: Current security score.

        Returns:
            PersonalizedLearningPath model.
        """
        diff = "beginner" if security_score < 70 else ("medium" if security_score < 90 else "advanced")

        modules = [
            LearningPathModule(
                module_id="mod_phish_01",
                title="Spear-Phishing & Social Engineering Defense",
                difficulty_level=diff,
                estimated_minutes=15,
            ),
            LearningPathModule(
                module_id="mod_cred_01",
                title="Multi-Factor Auth & Credential Protection",
                difficulty_level=diff,
                estimated_minutes=10,
            ),
        ]

        path = PersonalizedLearningPath(
            path_id=f"path_{employee_id[:6]}",
            employee_id=employee_id,
            role=role,
            assigned_modules=modules,
        )

        security_logger.info(f"AdaptiveLearningEngine: Created personalized path for '{employee_id}' ({len(modules)} modules, difficulty={diff}).")
        return path


# Global AdaptiveLearningEngine instance
adaptive_learning_engine = AdaptiveLearningEngine()
