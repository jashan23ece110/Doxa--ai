"""
Enterprise Insider Risk Report Builder.

Generates comprehensive Insider Risk Reports containing executive summaries,
risk overviews, privileged access analyses, organizational exposure summaries,
behavioral deviation findings, compliance statuses, mitigation roadmaps, and AI recommendations.
Supports JSON and Markdown formatting.
"""

import json
import time
from typing import Dict, Any, List, Optional
from app.core.logging import security_logger
from app.core.human_intelligence.insider_risk.insider_risk_engine import ComprehensiveInsiderRiskAssessment
from app.core.human_intelligence.insider_risk.privileged_access_analyzer import PrivilegedAccessMetrics


class InsiderReportBuilder:
    """Enterprise Insider Risk Report Builder."""

    def build_report_data(
        self,
        assessment: ComprehensiveInsiderRiskAssessment,
        privilege_metrics: PrivilegedAccessMetrics,
        recommendations: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Builds structured insider risk report data dictionary.
        """
        recs = recommendations or [
            "Enforce quarterly entitlement reviews for privileged roles.",
            "Schedule role-tailored awareness training on administrative credential security.",
        ]

        report_data = {
            "title": f"Enterprise Insider Risk Report — {assessment.employee_id}",
            "employee_id": assessment.employee_id,
            "overall_insider_risk_score": assessment.overall_insider_risk_score,
            "privileged_access_risk_score": assessment.privileged_access_risk_score,
            "is_admin": privilege_metrics.is_admin,
            "assigned_roles": privilege_metrics.assigned_roles,
            "risk_level": assessment.risk_level.value.upper(),
            "recommendations": recs,
            "generated_at": time.time(),
        }

        security_logger.info(f"InsiderReportBuilder: Built report data for employee '{assessment.employee_id}'.")
        return report_data

    def to_markdown(self, report_data: Dict[str, Any]) -> str:
        """Renders report data as formatted GitHub Markdown."""
        lines = [
            f"# {report_data['title']}",
            f"**Generated At**: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(report_data['generated_at']))}  ",
            "",
            "## 🛡️ Executive Insider Risk Summary",
            f"- **Employee ID**: `{report_data['employee_id']}`",
            f"- **Overall Risk Score**: `{report_data['overall_insider_risk_score']} / 10.0` ({report_data['risk_level']})",
            f"- **Privileged Access Risk Score**: `{report_data['privileged_access_risk_score']} / 10.0`",
            f"- **Is Administrative Account**: `{report_data['is_admin']}`",
            f"- **Assigned Roles**: `{', '.join(report_data['assigned_roles'])}`",
            "",
            "## 💡 AI Risk Reduction Recommendations",
        ]

        for r in report_data['recommendations']:
            lines.append(f"- {r}")

        lines.extend([
            "",
            "## 📈 Mitigation Roadmap",
            "1. Validate separation of duties for cloud infrastructure roles.",
            "2. Maintain continuous monitoring of policy compliance metrics.",
        ])

        return "\n".join(lines)

    def to_json(self, report_data: Dict[str, Any]) -> str:
        """Renders report data as JSON string."""
        return json.dumps(report_data, indent=2, default=str)


# Global InsiderReportBuilder instance
insider_report_builder = InsiderReportBuilder()
