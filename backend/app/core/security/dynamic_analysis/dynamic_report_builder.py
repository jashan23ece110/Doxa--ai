"""
Enterprise Dynamic Analysis Report Builder.

Generates comprehensive Dynamic Analysis Threat Reports containing sandbox summaries,
behavioral findings, IOC summaries, forensic timelines, threat correlation, risk scores,
evidence inventories, analyst observations, and recommendations.
Supports JSON and Markdown formatting.
"""

import json
import time
from typing import Dict, Any, List, Optional
from app.core.logging import security_logger
from app.core.security.dynamic_analysis.behavior_analyzer import BehavioralReport
from app.core.security.dynamic_analysis.forensic_timeline import ForensicTimeline
from app.core.security.dynamic_analysis.risk_scoring_engine import OrganizationalRiskScore


class DynamicReportBuilder:
    """Enterprise Dynamic Analysis Report Builder."""

    def build_report_data(
        self,
        binary_id: str,
        behavioral_report: BehavioralReport,
        timeline: ForensicTimeline,
        risk_score: OrganizationalRiskScore,
        iocs_count: int,
    ) -> Dict[str, Any]:
        """
        Builds dynamic analysis report dictionary.
        """
        report_data = {
            "title": f"Enterprise Dynamic Sandbox & Forensic Report — {binary_id}",
            "binary_id": binary_id,
            "risk_score": risk_score.normalized_score,
            "threat_category": risk_score.threat_category,
            "has_persistence": behavioral_report.has_persistence,
            "has_network_activity": behavioral_report.has_network_activity,
            "has_privilege_escalation": behavioral_report.has_privilege_escalation,
            "total_timeline_events": timeline.total_events,
            "total_iocs_detected": iocs_count,
            "detected_behaviors": behavioral_report.detected_behaviors,
            "generated_at": time.time(),
        }

        security_logger.info(f"DynamicReportBuilder: Built report for binary '{binary_id}'.")
        return report_data

    def to_markdown(self, report_data: Dict[str, Any]) -> str:
        """Renders report data as formatted GitHub Markdown."""
        lines = [
            f"# {report_data['title']}",
            f"**Generated At**: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(report_data['generated_at']))}  ",
            "",
            "## 🛡️ Dynamic Analysis Executive Summary",
            f"- **Binary ID**: `{report_data['binary_id']}`",
            f"- **Organizational Risk Score**: `{report_data['risk_score']} / 100` (`{report_data['threat_category']}`)",
            f"- **Persistence Detected**: `{report_data['has_persistence']}`",
            f"- **Network Activity Detected**: `{report_data['has_network_activity']}`",
            f"- **Privilege Escalation Detected**: `{report_data['has_privilege_escalation']}`",
            f"- **Total IOCs Detected**: `{report_data['total_iocs_detected']}`",
            f"- **Timeline Events**: `{report_data['total_timeline_events']}`",
            "",
            "## ⚠️ Observed Behaviors",
        ]

        for b in report_data["detected_behaviors"]:
            lines.append(f"- {b}")

        lines.extend([
            "",
            "## 💡 Remediation Recommendations",
            "1. Revoke persistence registry entries and terminate associated dropped processes.",
            "2. Block identified network C2 IP indicators across enterprise boundary gateways.",
        ])

        return "\n".join(lines)

    def to_json(self, report_data: Dict[str, Any]) -> str:
        """Renders report data as JSON string."""
        return json.dumps(report_data, indent=2, default=str)


# Global DynamicReportBuilder instance
dynamic_report_builder = DynamicReportBuilder()
