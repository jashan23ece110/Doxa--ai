"""
Enterprise Security Operations Orchestrator.

Unifies Incident Response Playbooks, SIEM/SOAR Exporting, Real-Time Telemetry Streaming,
and SOC Operations Backend for Doxa.
"""

from typing import Dict, Any, List, Optional
from app.core.logging import security_logger
from app.core.security.security_types import ThreatReport, RiskAssessment, IOC
from app.core.security.operations.playbook_engine import playbook_engine, PlaybookExecutionResult
from app.core.security.operations.siem_soar_exporter import siem_soar_exporter
from app.core.security.operations.telemetry_streamer import telemetry_streamer
from app.core.security.operations.soc_dashboard_backend import soc_dashboard_backend, SOCDashboardMetrics


class SecurityOperationsManager:
    """Enterprise Security Operations Orchestrator."""

    async def handle_security_incident(
        self,
        incident_id: str,
        report: ThreatReport,
        risk_assessment: RiskAssessment,
        iocs: List[IOC],
        targets: List[str],
    ) -> Dict[str, Any]:
        """
        Handles a security incident end-to-end:
        1. Emits real-time telemetry event.
        2. Executes automated incident response playbook.
        3. Exports SIEM/SOAR bundles (STIX 2.1, CEF, MISP).
        """
        security_logger.info(f"SecurityOperationsManager: Handling incident '{incident_id}' (RiskScore={risk_assessment.overall_risk_score:.1f}).")

        # 1. Telemetry Stream
        await telemetry_streamer.emit_event(
            event_type="security_incident",
            payload={"incident_id": incident_id, "title": report.title, "risk_score": risk_assessment.overall_risk_score},
            severity=risk_assessment.threat_level.value,
        )

        # 2. Automated Response Playbook
        playbook_res = await playbook_engine.run_playbook(incident_id, risk_assessment, targets)

        # 3. SIEM / SOAR Exports
        stix_bundle = siem_soar_exporter.to_stix21_bundle(report, iocs)
        cef_syslog = siem_soar_exporter.to_cef_syslog(report, risk_assessment)
        misp_event = siem_soar_exporter.to_misp_event(report, iocs)

        return {
            "incident_id": incident_id,
            "playbook_result": playbook_res,
            "stix_bundle": stix_bundle,
            "cef_syslog": cef_syslog,
            "misp_event": misp_event,
        }

    def get_soc_dashboard(self) -> SOCDashboardMetrics:
        """Retrieves real-time SOC dashboard metrics."""
        return soc_dashboard_backend.get_dashboard_summary()


# Global SecurityOperationsManager instance
security_operations_manager = SecurityOperationsManager()
