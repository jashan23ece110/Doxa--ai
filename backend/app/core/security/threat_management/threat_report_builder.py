"""
Enterprise Threat Intelligence Report Builder.

Generates comprehensive Threat Intelligence Reports containing executive summaries,
vulnerability overviews, CVE mappings, STRIDE threat models, attack surface summaries,
compliance findings, remediation roadmaps, risk trends, and AI recommendations.
Supports JSON and Markdown formatting.
"""

import json
import time
from typing import Dict, Any, List, Optional
from app.core.logging import security_logger
from app.core.security.threat_management.vulnerability_engine import VulnerabilityMetadata
from app.core.security.threat_management.threat_model_engine import ThreatModel
from app.core.security.threat_management.attack_surface_analyzer import AttackSurfaceInventory
from app.core.security.threat_management.compliance_engine import FrameworkComplianceResult
from app.core.security.threat_management.recommendation_engine import SecurityRecommendation


class ThreatIntelligenceReportBuilder:
    """Enterprise Threat Intelligence Report Builder."""

    def build_report_data(
        self,
        system_name: str,
        vulnerabilities: List[VulnerabilityMetadata],
        threat_model: ThreatModel,
        attack_surface: AttackSurfaceInventory,
        compliance: FrameworkComplianceResult,
        recommendations: List[SecurityRecommendation],
    ) -> Dict[str, Any]:
        """
        Builds comprehensive threat intelligence report dictionary.
        """
        report_data = {
            "title": f"Enterprise Vulnerability & Threat Intelligence Report — {system_name}",
            "system_name": system_name,
            "vulnerabilities_count": len(vulnerabilities),
            "threats_identified_count": len(threat_model.threats),
            "attack_surface_score": attack_surface.attack_surface_score,
            "compliance_framework": compliance.framework_name,
            "compliance_score": compliance.compliance_score,
            "recommendations_count": len(recommendations),
            "generated_at": time.time(),
        }

        security_logger.info(f"ThreatIntelligenceReportBuilder: Built report data for system '{system_name}'.")
        return report_data

    def to_markdown(self, report_data: Dict[str, Any], vulnerabilities: List[VulnerabilityMetadata], recommendations: List[SecurityRecommendation]) -> str:
        """Renders report data as formatted GitHub Markdown."""
        lines = [
            f"# {report_data['title']}",
            f"**Generated At**: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(report_data['generated_at']))}  ",
            "",
            "## 🛡️ Executive Security Summary",
            f"- **System**: `{report_data['system_name']}`",
            f"- **Compliance Score**: `{report_data['compliance_score']}%` (`{report_data['compliance_framework']}`)",
            f"- **Attack Surface Score**: `{report_data['attack_surface_score']} / 100`",
            f"- **Correlated Vulnerabilities**: `{report_data['vulnerabilities_count']}`",
            f"- **Identified STRIDE Threats**: `{report_data['threats_identified_count']}`",
            "",
            "## 🔍 Correlated Vulnerabilities (CVE Mapping)",
        ]

        for v in vulnerabilities:
            lines.append(f"- **{v.cve_id}** (`{v.cwe_id}`): Score `{v.cvss_score}` ({v.severity.value.upper()}) — *{v.remediation_guidance}*")

        lines.extend([
            "",
            "## 💡 AI Security Recommendations & Remediation Roadmap",
        ])

        for rec in recommendations:
            lines.append(f"### {rec.title} (Priority: `{rec.priority}`)")
            lines.append(f"*{rec.explainability_rationale}*")
            for step in rec.action_steps:
                lines.append(f"1. {step}")
            lines.append("")

        return "\n".join(lines)

    def to_json(self, report_data: Dict[str, Any]) -> str:
        """Renders report data as JSON string."""
        return json.dumps(report_data, indent=2, default=str)


# Global ThreatIntelligenceReportBuilder instance
threat_intel_report_builder = ThreatIntelligenceReportBuilder()
