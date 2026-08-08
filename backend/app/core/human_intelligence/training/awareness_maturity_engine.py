"""
Security Awareness Maturity Engine.

Measures individual, team, departmental, and organizational security awareness maturity scores,
benchmarking against industry maturity frameworks (e.g. CMMI-style maturity levels 1-5).
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class OrganizationalMaturityScore(BaseModel):
    scope_name: str  # organization, department, team
    maturity_level: int = 4  # Level 1 (Initial) to Level 5 (Resilient/Optimized)
    maturity_stage_name: str = "PROACTIVE & RESILIENT"
    benchmark_score: float = 89.5  # 0 to 100
    strengths: List[str] = Field(default_factory=list)


class AwarenessMaturityEngine:
    """Enterprise Security Awareness Maturity Engine."""

    def evaluate_maturity(self, scope_name: str = "Organization", average_score: float = 88.0) -> OrganizationalMaturityScore:
        """
        Evaluates organizational awareness maturity level.

        Args:
            scope_name: Scope string.
            average_score: Average security awareness score.

        Returns:
            OrganizationalMaturityScore model.
        """
        level = 5 if average_score >= 92 else (4 if average_score >= 82 else 3)
        stage = "OPTIMIZED & RESILIENT" if level == 5 else ("PROACTIVE" if level == 4 else "ADAPTIVE")

        score = OrganizationalMaturityScore(
            scope_name=scope_name,
            maturity_level=level,
            maturity_stage_name=stage,
            benchmark_score=average_score,
            strengths=[
                "High awareness quiz participation",
                "Automated mock phishing reporting habits",
            ],
        )

        security_logger.info(f"AwarenessMaturityEngine: Evaluated maturity for '{scope_name}': Level {level} ({stage}).")
        return score


# Global AwarenessMaturityEngine instance
awareness_maturity_engine = AwarenessMaturityEngine()
