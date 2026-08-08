"""
Enterprise Behavioral Intelligence Report Builder.

Generates comprehensive Behavioral Intelligence Reports containing executive summaries,
behavioral overviews, influence analysis, trust network summaries, anomaly findings,
risk assessments, trend analyses, AI explanations, and recommendations.
Supports JSON and Markdown formatting.
"""

import json
import time
from typing import Dict, Any, List, Optional
from app.core.logging import security_logger
from app.core.human_intelligence.behavior.behavior_model_engine import ProbabilisticBehaviorProfile
from app.core.human_intelligence.behavior.influence_analysis import InfluenceMetric
from app.core.human_intelligence.behavior.explainability_engine import BehavioralExplanation


class BehaviorReportBuilder:
    """Enterprise Behavioral Intelligence Report Builder."""

    def build_report_data(
        self,
        profile: ProbabilisticBehaviorProfile,
        influence: InfluenceMetric,
        explanation: BehavioralExplanation,
        anomalies_count: int = 0,
    ) -> Dict[str, Any]:
        """
        Builds structured behavioral intelligence report dictionary.
        """
        report_data = {
            "title": f"Enterprise Behavioral Intelligence Report — {profile.employee_id}",
            "employee_id": profile.employee_id,
            "security_habit_score": profile.security_habit_score,
            "decision_consistency_score": profile.decision_consistency_score,
            "awareness_trend": profile.awareness_evolution_trend,
            "influence_score": influence.influence_score,
            "collaboration_density": influence.collaboration_density,
            "anomalies_count": anomalies_count,
            "ai_explanation": explanation.summary_rationale,
            "generated_at": time.time(),
        }

        security_logger.info(f"BehaviorReportBuilder: Built report data for employee '{profile.employee_id}'.")
        return report_data

    def to_markdown(self, report_data: Dict[str, Any]) -> str:
        """Renders report data as formatted GitHub Markdown."""
        lines = [
            f"# {report_data['title']}",
            f"**Generated At**: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(report_data['generated_at']))}  ",
            "",
            "## 🛡️ Executive Behavioral Overview",
            f"- **Employee ID**: `{report_data['employee_id']}`",
            f"- **Security Habit Score**: `{report_data['security_habit_score']} / 100`",
            f"- **Decision Consistency**: `{report_data['decision_consistency_score']} / 100`",
            f"- **Awareness Evolution Trend**: `{report_data['awareness_trend']}`",
            f"- **Organizational Influence Score**: `{report_data['influence_score']} / 100`",
            f"- **Flagged Anomalies Count**: `{report_data['anomalies_count']}`",
            "",
            "## 🧠 Transparent AI Reasoning & Rationale",
            report_data['ai_explanation'],
            "",
            "## 💡 Recommended Next Actions",
            "1. Maintain periodic security awareness learning paths.",
            "2. Continue positive security habit reinforcement.",
        ]

        return "\n".join(lines)

    def to_json(self, report_data: Dict[str, Any]) -> str:
        """Renders report data as JSON string."""
        return json.dumps(report_data, indent=2, default=str)


# Global BehaviorReportBuilder instance
behavior_report_builder = BehaviorReportBuilder()
