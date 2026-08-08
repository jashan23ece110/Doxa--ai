"""
Enterprise Human Security Resilience Report Builder.

Generates comprehensive Human Security Resilience Reports containing executive summaries,
attack surface analyses, simulation overviews, resilience assessments, control validation results,
organizational readiness ratings, AI recommendations, and improvement roadmaps.
Supports JSON and Markdown formatting.
"""

import json
import time
from typing import Dict, Any, List, Optional
from app.core.logging import security_logger
from app.core.human_intelligence.red_team.human_attack_surface_engine import HumanAttackSurfaceMetrics
from app.core.human_intelligence.red_team.resilience_engine import HumanResilienceMetrics
from app.core.human_intelligence.red_team.control_validation_engine import SecurityControlValidationResult


class ResilienceReportBuilder:
    """Enterprise Human Security Resilience Report Builder."""

    def build_report_data(
        self,
        surface: HumanAttackSurfaceMetrics,
        resilience: HumanResilienceMetrics,
        validation: SecurityControlValidationResult,
        recommendations: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Builds structured resilience report data dictionary.
        """
        recs = recommendations or [
            "Maintain monthly conceptual educational simulations across all operational departments.",
            "Enforce out-of-band wire transfer authorization controls.",
        ]

        report_data = {
            "title": f"Enterprise Human Security Resilience Report — {resilience.scope_name}",
            "scope_name": resilience.scope_name,
            "overall_resilience_score": resilience.overall_resilience_score,
            "resilience_level": resilience.resilience_level,
            "attack_surface_score": surface.overall_attack_surface_score,
            "awareness_coverage_percent": surface.awareness_coverage_percent,
            "control_validated": validation.control_name,
            "control_efficacy_percent": validation.efficacy_rating_percent,
            "recommendations": recs,
            "generated_at": time.time(),
        }

        security_logger.info(f"ResilienceReportBuilder: Built report data for scope '{resilience.scope_name}'.")
        return report_data

    def to_markdown(self, report_data: Dict[str, Any]) -> str:
        """Renders report data as formatted GitHub Markdown."""
        lines = [
            f"# {report_data['title']}",
            f"**Generated At**: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(report_data['generated_at']))}  ",
            "",
            "## 🛡️ Executive Resilience Overview",
            f"- **Scope**: `{report_data['scope_name']}`",
            f"- **Human Resilience Score**: `{report_data['overall_resilience_score']} / 100` ({report_data['resilience_level']})",
            f"- **Human Attack Surface Score**: `{report_data['attack_surface_score']} / 10.0`",
            f"- **Awareness Coverage**: `{report_data['awareness_coverage_percent']}%`",
            f"- **Validated Control**: `{report_data['control_validated']}` (`{report_data['control_efficacy_percent']}% Efficacy`)",
            "",
            "## 💡 AI Strategic Resilience Recommendations",
        ]

        for r in report_data['recommendations']:
            lines.append(f"- {r}")

        lines.extend([
            "",
            "## 📈 Improvement Roadmap",
            "1. Conduct quarterly conceptual executive impersonation scenario reviews.",
            "2. Maintain continuous automated reporting extension validation.",
        ])

        return "\n".join(lines)

    def to_json(self, report_data: Dict[str, Any]) -> str:
        """Renders report data as JSON string."""
        return json.dumps(report_data, indent=2, default=str)


# Global ResilienceReportBuilder instance
resilience_report_builder = ResilienceReportBuilder()
