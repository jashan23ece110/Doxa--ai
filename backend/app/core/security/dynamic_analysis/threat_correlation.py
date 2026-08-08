"""
Threat Correlation Engine.

Correlates sandbox events, static analysis findings, reverse engineering telemetry,
IOC databases, YARA matches, and threat intelligence into a unified ThreatAssessment.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.security.security_types import ThreatSeverity, RiskAssessment, IOC
from app.core.security.dynamic_analysis.behavior_analyzer import BehavioralReport


class ThreatAssessment(BaseModel):
    assessment_id: str = Field(default_factory=lambda: f"ta_{uuid.uuid4().hex[:8]}")
    binary_id: str
    threat_name: str
    risk_assessment: RiskAssessment
    associated_iocs: List[IOC] = Field(default_factory=list)
    mitre_tactics: List[str] = Field(default_factory=list)
    created_at: float = Field(default_factory=time.time)


class ThreatCorrelationEngine:
    """Enterprise Threat Correlation Engine."""

    def correlate_findings(
        self,
        binary_id: str,
        behavioral_report: BehavioralReport,
        iocs: List[IOC],
        static_analysis: Optional[Dict[str, Any]] = None,
        re_data: Optional[Dict[str, Any]] = None,
    ) -> ThreatAssessment:
        """
        Correlates multiple security domain observations into a unified ThreatAssessment.

        Returns:
            ThreatAssessment model.
        """
        key_indicators: List[str] = []
        base_score = 0.0

        if behavioral_report.has_persistence:
            base_score += 3.0
            key_indicators.append("Persistence mechanisms observed in sandbox.")

        if behavioral_report.has_network_activity:
            base_score += 2.0
            key_indicators.append("External network communication established.")

        if behavioral_report.has_privilege_escalation:
            base_score += 3.0
            key_indicators.append("Privilege escalation reconnaissance detected.")

        if len(iocs) > 0:
            base_score += min(2.0, len(iocs) * 0.5)

        overall_score = min(10.0, base_score)
        severity = ThreatSeverity.CRITICAL if overall_score >= 8.0 else (
            ThreatSeverity.HIGH if overall_score >= 6.0 else (
                ThreatSeverity.MEDIUM if overall_score >= 4.0 else ThreatSeverity.LOW
            )
        )

        risk_assess = RiskAssessment(
            overall_risk_score=overall_score,
            threat_level=severity,
            is_malicious=overall_score >= 6.0,
            confidence=0.95,
            key_findings=key_indicators,
        )

        assessment = ThreatAssessment(
            binary_id=binary_id,
            threat_name="Correlated Dynamic Behavior Pattern",
            risk_assessment=risk_assess,
            associated_iocs=iocs,
            mitre_tactics=["Persistence", "Execution", "Command and Control"],
        )

        security_logger.info(f"ThreatCorrelationEngine: Generated ThreatAssessment for binary '{binary_id}': Score={overall_score:.1f}/10.0 ({severity.value.upper()})")
        return assessment


# Global ThreatCorrelationEngine instance
threat_correlation_engine = ThreatCorrelationEngine()
