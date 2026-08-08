"""
SIEM & SOAR Integration Exporter.

Exports security threat intelligence, findings, and reports into
STIX 2.1 JSON, TAXII 2.1, Common Event Format (CEF) Syslog, and MISP JSON formats.
"""

import json
import time
from typing import Dict, Any, List
from app.core.logging import security_logger
from app.core.security.security_types import ThreatReport, IOC, RiskAssessment


class SIEMSOARExporter:
    """Enterprise SIEM & SOAR Exporter."""

    def to_stix21_bundle(self, report: ThreatReport, iocs: List[IOC]) -> Dict[str, Any]:
        """
        Exports threat intelligence data to STIX 2.1 JSON Bundle object.

        Returns:
            Dict representing STIX 2.1 Bundle.
        """
        objects = [
            {
                "type": "report",
                "id": f"report--{report.report_id}",
                "spec_version": "2.1",
                "name": report.title,
                "description": report.summary,
                "published": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(report.generated_at)),
                "object_refs": [f"indicator--{ioc.ioc_id}" for ioc in iocs],
            }
        ]

        for ioc in iocs:
            objects.append({
                "type": "indicator",
                "id": f"indicator--{ioc.ioc_id}",
                "spec_version": "2.1",
                "pattern_type": "stix",
                "pattern": f"[{ioc.ioc_type}:value = '{ioc.value}']",
                "valid_from": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ioc.first_detected)),
            })

        bundle = {
            "type": "bundle",
            "id": f"bundle--stix-export-{report.report_id}",
            "spec_version": "2.1",
            "objects": objects,
        }

        security_logger.info(f"SIEMSOARExporter: Exported STIX 2.1 bundle with {len(objects)} objects.")
        return bundle

    def to_cef_syslog(self, report: ThreatReport, risk: RiskAssessment) -> str:
        """
        Exports alert finding to Common Event Format (CEF) syslog string.

        Format:
        CEF:Version|Device Vendor|Device Product|Device Version|Signature ID|Name|Severity|Extension
        """
        cef_sev = int(risk.overall_risk_score) if risk else 5
        cef_string = (
            f"CEF:0|Doxa|AI_OS_Security|1.0|ALERT_001|{report.title}|{cef_sev}|"
            f"msg={report.summary.replace('|', '_')} cat=ThreatResearch"
        )
        return cef_string

    def to_misp_event(self, report: ThreatReport, iocs: List[IOC]) -> Dict[str, Any]:
        """Exports data to MISP Event JSON format."""
        attributes = []
        for ioc in iocs:
            attributes.append({
                "type": ioc.ioc_type,
                "value": ioc.value,
                "category": "Network activity" if ioc.ioc_type in ("ip", "domain", "url") else "Payload delivery",
                "to_ids": True,
            })

        misp_event = {
            "Event": {
                "info": report.title,
                "threat_level_id": "1",  # High
                "analysis": "2",          # Completed
                "Attribute": attributes,
            }
        }
        return misp_event


# Global SIEMSOARExporter instance
siem_soar_exporter = SIEMSOARExporter()
