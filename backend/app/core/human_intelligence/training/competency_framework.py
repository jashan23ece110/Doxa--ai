"""
Enterprise Competency Framework.

Manages security competency models, skill proficiency levels, corporate certifications,
role security expectations, and learning objective evaluations.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class CompetencyProfile(BaseModel):
    employee_id: str
    proficiency_level: str = "ADVANCED"  # NOVICE, INTERMEDIATE, ADVANCED, MASTER
    overall_proficiency_score: float = 88.0  # 0 to 100
    certified_skills: List[str] = Field(default_factory=list)


class CompetencyFramework:
    """Enterprise Security Competency Framework."""

    def evaluate_competency(self, employee_id: str, security_score: float = 85.0) -> CompetencyProfile:
        """
        Evaluates security competency level and certifications.

        Args:
            employee_id: Employee ID.
            security_score: Security awareness score.

        Returns:
            CompetencyProfile model.
        """
        level = "MASTER" if security_score >= 95 else ("ADVANCED" if security_score >= 80 else "INTERMEDIATE")
        certs = ["General Security Awareness Certified"]
        if security_score >= 90:
            certs.append("Phishing Defense Champion")

        profile = CompetencyProfile(
            employee_id=employee_id,
            proficiency_level=level,
            overall_proficiency_score=security_score,
            certified_skills=certs,
        )

        security_logger.info(f"CompetencyFramework: Evaluated competency for '{employee_id}': Level={level}, Score={security_score}.")
        return profile


# Global CompetencyFramework instance
competency_framework = CompetencyFramework()
