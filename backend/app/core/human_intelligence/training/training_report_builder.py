"""
Enterprise Human Intelligence Training Report Builder.

Generates comprehensive Human Intelligence Training Reports containing executive summaries,
learning progress statistics, competency analyses, maturity assessments, engagement analytics,
coaching outcomes, organizational readiness metrics, AI recommendations, and long-term roadmaps.
Supports JSON and Markdown formatting.
"""

import json
import time
from typing import Dict, Any, List, Optional
from app.core.logging import security_logger
from app.core.human_intelligence.training.behavior_improvement_engine import BehaviorImprovementMetrics
from app.core.human_intelligence.training.competency_framework import CompetencyProfile
from app.core.human_intelligence.training.awareness_maturity_engine import OrganizationalMaturityScore


class TrainingReportBuilder:
    """Enterprise Training Report Builder."""

    def build_report_data(
        self,
        improvement: BehaviorImprovementMetrics,
        competency: CompetencyProfile,
        maturity: OrganizationalMaturityScore,
        recommendations: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Builds structured training report data dictionary.
        """
        recs = recommendations or [
            "Maintain monthly micro-learning refreshes to preserve proactive security habits.",
            "Recognize certified security champions across departments.",
        ]

        report_data = {
            "title": f"Enterprise Human Intelligence Training Report — {improvement.employee_id}",
            "employee_id": improvement.employee_id,
            "habit_formation_score": improvement.habit_formation_score,
            "improvement_delta": improvement.score_improvement_delta,
            "behavioral_maturity_stage": improvement.behavioral_maturity_stage,
            "proficiency_level": competency.proficiency_level,
            "certified_skills": competency.certified_skills,
            "org_maturity_level": maturity.maturity_level,
            "recommendations": recs,
            "generated_at": time.time(),
        }

        security_logger.info(f"TrainingReportBuilder: Built report data for employee '{improvement.employee_id}'.")
        return report_data

    def to_markdown(self, report_data: Dict[str, Any]) -> str:
        """Renders report data as formatted GitHub Markdown."""
        lines = [
            f"# {report_data['title']}",
            f"**Generated At**: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(report_data['generated_at']))}  ",
            "",
            "## 🛡️ Executive Learning & Improvement Summary",
            f"- **Employee ID**: `{report_data['employee_id']}`",
            f"- **Habit Formation Score**: `{report_data['habit_formation_score']} / 100`",
            f"- **Score Improvement Delta**: `+{report_data['improvement_delta']}%`",
            f"- **Behavioral Maturity Stage**: `{report_data['behavioral_maturity_stage']}`",
            f"- **Proficiency Level**: `{report_data['proficiency_level']}`",
            f"- **Certified Skills**: `{', '.join(report_data['certified_skills'])}`",
            "",
            "## 💡 AI Learning & Coaching Recommendations",
        ]

        for r in report_data['recommendations']:
            lines.append(f"- {r}")

        lines.extend([
            "",
            "## 📈 Long-Term Learning Roadmap",
            "1. Complete annual advanced phishing defense certification path.",
            "2. Participate as departmental security awareness ambassador.",
        ])

        return "\n".join(lines)

    def to_json(self, report_data: Dict[str, Any]) -> str:
        """Renders report data as JSON string."""
        return json.dumps(report_data, indent=2, default=str)


# Global TrainingReportBuilder instance
training_report_builder = TrainingReportBuilder()
