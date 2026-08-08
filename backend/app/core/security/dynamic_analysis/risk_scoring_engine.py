"""
Enterprise Risk Scoring Engine.

Calculates severity, confidence, exploitability estimate, persistence likelihood,
lateral movement indicators, and privilege escalation indicators into a normalized score (0–100).
"""

from typing import Dict, Any, List
from pydantic import BaseModel
from app.core.logging import security_logger
from app.core.security.dynamic_analysis.behavior_analyzer import BehavioralReport


class OrganizationalRiskScore(BaseModel):
    normalized_score: float  # 0.0 to 100.0
    threat_category: str
    exploitability_estimate: float
    persistence_likelihood: float
    lateral_movement_risk: float
    privilege_escalation_risk: float


class RiskScoringEngine:
    """Enterprise Risk Scoring Engine."""

    def calculate_risk(self, behavioral_report: BehavioralReport, ioc_count: int = 0) -> OrganizationalRiskScore:
        """
        Calculates normalized organizational risk score (0-100).

        Args:
            behavioral_report: BehavioralReport model.
            ioc_count: Total extracted IOCs count.

        Returns:
            OrganizationalRiskScore model.
        """
        score = 0.0

        persistence_risk = 85.0 if behavioral_report.has_persistence else 10.0
        lateral_risk = 75.0 if behavioral_report.has_network_activity else 15.0
        priv_esc_risk = 90.0 if behavioral_report.has_privilege_escalation else 10.0
        exploitability = min(100.0, 40.0 + (len(behavioral_report.suspicious_process_spawns) * 15.0))

        score += persistence_risk * 0.3
        score += lateral_risk * 0.25
        score += priv_esc_risk * 0.25
        score += exploitability * 0.20

        normalized = round(min(100.0, score), 1)
        category = "CRITICAL" if normalized >= 80.0 else (
            "HIGH" if normalized >= 60.0 else (
                "MEDIUM" if normalized >= 40.0 else "LOW"
            )
        )

        org_risk = OrganizationalRiskScore(
            normalized_score=normalized,
            threat_category=category,
            exploitability_estimate=exploitability,
            persistence_likelihood=persistence_risk,
            lateral_movement_risk=lateral_risk,
            privilege_escalation_risk=priv_esc_risk,
        )

        security_logger.info(f"RiskScoringEngine: Calculated normalized risk score: {normalized}/100 ({category}).")
        return org_risk


# Global RiskScoringEngine instance
risk_scoring_engine = RiskScoringEngine()
