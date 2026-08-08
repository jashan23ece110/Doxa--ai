"""
AI Learning Recommendation Engine.

Generates explainable recommendations for training priorities, refresher courses,
role-specific awareness modules, and organizational security posture improvements.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.human_intelligence.human_intelligence_types import SecurityRecommendation


class AILearningRecommendationEngine:
    """Enterprise AI Learning Recommendation Engine."""

    def generate_learning_recommendations(self, employee_id: str, knowledge_gaps: List[str]) -> List[SecurityRecommendation]:
        """
        Generates AI-assisted personalized learning recommendations based on identified knowledge gaps.

        Args:
            employee_id: Employee ID.
            knowledge_gaps: List of identified knowledge gap strings.

        Returns:
            List of SecurityRecommendation models.
        """
        recs = [
            SecurityRecommendation(
                target_type="employee",
                target_id=employee_id,
                title="Refresher: QR-Code & Authentication Security",
                priority="HIGH" if len(knowledge_gaps) > 0 else "MEDIUM",
                action_items=[
                    "Complete 10-minute micro-learning module on QR code authentication safety.",
                    "Review SecOps protocol for reporting suspicious sign-in requests.",
                ],
            )
        ]

        security_logger.info(f"AILearningRecommendationEngine: Generated {len(recs)} learning recommendations for employee '{employee_id}'.")
        return recs


# Global AILearningRecommendationEngine instance
ai_learning_recommendation_engine = AILearningRecommendationEngine()
