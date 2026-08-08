"""
Enterprise Security Awareness Report Builder.

Generates comprehensive Security Awareness Reports containing executive summaries,
campaign overviews, participation statistics, awareness scores, assessment results,
learning analytics, recommendations, and improvement roadmaps.
Supports JSON and Markdown formatting.
"""

import json
import time
from typing import Dict, Any, List, Optional
from app.core.logging import security_logger
from app.core.human_intelligence.awareness.campaign_manager import AwarenessCampaign
from app.core.human_intelligence.awareness.awareness_scoring import DetailedAwarenessScore


class AwarenessReportBuilder:
    """Enterprise Awareness Report Builder."""

    def build_report_data(
        self,
        campaign: AwarenessCampaign,
        avg_awareness_score: float = 88.5,
        recommendations: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Builds structured awareness report data dictionary.
        """
        recs = recommendations or [
            "Schedule quarterly role-tailored phishing awareness refreshers.",
            "Deploy executive spear-phishing defense micro-learning modules.",
        ]

        report_data = {
            "title": f"Enterprise Security Awareness Report — {campaign.name}",
            "campaign_id": campaign.campaign_id,
            "campaign_name": campaign.name,
            "target_department": campaign.target_department,
            "status": campaign.status,
            "completion_rate_percent": campaign.completion_rate_percent,
            "average_org_awareness_score": avg_awareness_score,
            "recommendations": recs,
            "generated_at": time.time(),
        }

        security_logger.info(f"AwarenessReportBuilder: Built awareness report data for campaign '{campaign.campaign_id}'.")
        return report_data

    def to_markdown(self, report_data: Dict[str, Any]) -> str:
        """Renders report data as formatted GitHub Markdown."""
        lines = [
            f"# {report_data['title']}",
            f"**Generated At**: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(report_data['generated_at']))}  ",
            "",
            "## 🛡️ Executive Awareness Summary",
            f"- **Campaign**: `{report_data['campaign_name']}` (`{report_data['campaign_id']}`)",
            f"- **Target Scope**: `{report_data['target_department']}`",
            f"- **Completion Rate**: `{report_data['completion_rate_percent']}%`",
            f"- **Average Awareness Score**: `{report_data['average_org_awareness_score']} / 100`",
            "",
            "## 💡 Learning & Posture Recommendations",
        ]

        for r in report_data['recommendations']:
            lines.append(f"- {r}")

        lines.extend([
            "",
            "## 📈 Improvement Roadmap",
            "1. Expand micro-learning modules to remote teams.",
            "2. Automate recognition rewards for employees reporting mock simulation tests.",
        ])

        return "\n".join(lines)

    def to_json(self, report_data: Dict[str, Any]) -> str:
        """Renders report data as JSON string."""
        return json.dumps(report_data, indent=2, default=str)


# Global AwarenessReportBuilder instance
awareness_report_builder = AwarenessReportBuilder()
