"""
Enterprise Organizational Intelligence Report Builder.

Generates comprehensive Organizational Intelligence Reports containing executive summaries,
organizational health metrics, department risk analytics, workforce trends, fused intelligence findings,
resilience assessments, AI recommendations, and strategic improvement roadmaps.
Supports JSON and Markdown formatting.
"""

import json
import time
from typing import Dict, Any, List, Optional
from app.core.logging import security_logger
from app.core.human_intelligence.organization.organizational_intelligence_engine import OrganizationalIntelligenceSummary
from app.core.human_intelligence.organization.intelligence_fusion import FusedOrganizationalInsight
from app.core.human_intelligence.organization.enterprise_intelligence_metrics import EnterpriseHumanIntelligenceKPIs


class OrganizationalReportBuilder:
    """Enterprise Organizational Intelligence Report Builder."""

    def build_report_data(
        self,
        summary: OrganizationalIntelligenceSummary,
        insight: FusedOrganizationalInsight,
        kpis: EnterpriseHumanIntelligenceKPIs,
        recommendations: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Builds structured organizational report data dictionary.
        """
        recs = recommendations or [
            "Establish cross-departmental security champion networks in cloud engineering and operations.",
            "Maintain continuous fused intelligence reporting for executive leadership.",
        ]

        report_data = {
            "title": f"Enterprise Organizational Intelligence Report — {summary.scope_id}",
            "scope_id": summary.scope_id,
            "enterprise_intelligence_score": summary.enterprise_intelligence_score,
            "workforce_health_score": summary.workforce_health_score,
            "overall_posture_rating": summary.overall_posture_rating,
            "fused_insight_title": insight.summary_title,
            "fused_findings": insight.detailed_findings,
            "workforce_readiness_percent": kpis.workforce_readiness_rating_percent,
            "department_maturity_average": kpis.department_maturity_average,
            "recommendations": recs,
            "generated_at": time.time(),
        }

        security_logger.info(f"OrganizationalReportBuilder: Built report data for scope '{summary.scope_id}'.")
        return report_data

    def to_markdown(self, report_data: Dict[str, Any]) -> str:
        """Renders report data as formatted GitHub Markdown."""
        lines = [
            f"# {report_data['title']}",
            f"**Generated At**: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(report_data['generated_at']))}  ",
            "",
            "## 🛡️ Executive Organizational Intelligence Overview",
            f"- **Scope**: `{report_data['scope_id']}`",
            f"- **Enterprise Intelligence Score**: `{report_data['enterprise_intelligence_score']} / 100` ({report_data['overall_posture_rating']})",
            f"- **Workforce Health Score**: `{report_data['workforce_health_score']} / 100`",
            f"- **Workforce Readiness Rating**: `{report_data['workforce_readiness_percent']}%`",
            f"- **Department Maturity Level Average**: `{report_data['department_maturity_average']} / 5.0`",
            "",
            "## 🧠 Fused Human Intelligence Findings",
            f"### {report_data['fused_insight_title']}",
        ]

        for f in report_data['fused_findings']:
            lines.append(f"- {f}")

        lines.extend([
            "",
            "## 💡 Strategic Recommendations",
        ])

        for r in report_data['recommendations']:
            lines.append(f"- {r}")

        lines.extend([
            "",
            "## 📈 Long-Term Optimization Roadmap",
            "1. Expand departmental security champion coverage.",
            "2. Optimize continuous automated intelligence fusion workflows.",
        ])

        return "\n".join(lines)

    def to_json(self, report_data: Dict[str, Any]) -> str:
        """Renders report data as JSON string."""
        return json.dumps(report_data, indent=2, default=str)


# Global OrganizationalReportBuilder instance
organizational_report_builder = OrganizationalReportBuilder()
