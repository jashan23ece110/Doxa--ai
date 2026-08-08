"""
AI Learning Recommendation Engine.

Recommends next learning modules, coaching priorities, refresher schedules,
certification milestones, and organizational training strategies.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.human_intelligence.human_intelligence_types import SecurityRecommendation


class TrainingRecommendationEngine:
    """Enterprise Training AI Recommendation Engine."""

    def generate_training_recommendations(self, employee_id: str, current_score: float = 85.0) -> List[SecurityRecommendation]:
        """
        Generates AI-driven recommendations for next training steps.

        Args:
            employee_id: Employee ID.
            current_score: Current security score.

        Returns:
            List of SecurityRecommendation models.
        """
        recs = [
            SecurityRecommendation(
                target_type="employee",
                target_id=employee_id,
                title="Enroll in Advanced Executive Spear-Phishing Defense Module",
                priority="HIGH" if current_score < 80 else "MEDIUM",
                action_items=[
                    "Complete 15-minute micro-learning module on executive targeting.",
                    "Take adaptive quiz to earn Phishing Defense Champion certification.",
                ],
            )
        ]

        security_logger.info(f"TrainingRecommendationEngine: Generated {len(recs)} training recommendations for employee '{employee_id}'.")
        return recs


# Global TrainingRecommendationEngine instance
training_recommendation_engine = TrainingRecommendationEngine()
