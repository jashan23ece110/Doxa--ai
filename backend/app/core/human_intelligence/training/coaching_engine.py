"""
AI Security Coaching Engine.

Provides personalized 1-on-1 AI security coaching, learning recommendations,
awareness guidance, skill development plans, and constructive progress feedback.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class SecurityCoachingSession(BaseModel):
    session_id: str
    employee_id: str
    coaching_topic: str
    guidance_summary: str
    suggested_habits: List[str] = Field(default_factory=list)
    confidence_score: float = 0.95


class SecurityCoachingEngine:
    """Enterprise AI Security Coaching Engine."""

    def generate_coaching_feedback(self, employee_id: str, topic: str = "Phishing Awareness") -> SecurityCoachingSession:
        """
        Generates personalized AI security coaching guidance.

        Args:
            employee_id: Employee ID.
            topic: Focus coaching topic.

        Returns:
            SecurityCoachingSession object.
        """
        habits = [
            "Verify unexpected password reset links via corporate intranet before clicking.",
            "Report suspicious external emails using the 1-click SecOps reporting extension.",
        ]

        session = SecurityCoachingSession(
            session_id=f"coach_{employee_id[:6]}",
            employee_id=employee_id,
            coaching_topic=topic,
            guidance_summary=f"Great progress on '{topic}' assessments! Keep reinforcing verification habits for unverified external links.",
            suggested_habits=habits,
            confidence_score=0.96,
        )

        security_logger.info(f"SecurityCoachingEngine: Generated coaching guidance for '{employee_id}' on topic '{topic}'.")
        return session


# Global SecurityCoachingEngine instance
security_coaching_engine = SecurityCoachingEngine()
