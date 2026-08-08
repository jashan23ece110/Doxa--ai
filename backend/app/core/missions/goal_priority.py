"""
Goal Priority Engine for Autonomous Mission Control System.

Calculates dynamic goal priority score using urgency, importance, deadlines,
resource cost, dependencies, business value, and risk scores.
"""

from app.core.missions.mission_models import GoalItem


class GoalPriorityEngine:
    """Calculates dynamic priority score (0.0 to 1.0) for goal items."""

    @staticmethod
    def calculate_priority(goal: GoalItem) -> float:
        """
        Formula: Priority = (business_value * 0.35) + (urgency * 0.35) + ((1 - risk) * 0.20) + (dep_weight * 0.10)
        """
        dep_weight = 1.0 if not goal.dependencies else 0.50
        score = (
            (goal.business_value * 0.35) +
            (goal.urgency * 0.35) +
            ((1.0 - goal.risk_score) * 0.20) +
            (dep_weight * 0.10)
        )
        return round(min(max(score, 0.0), 1.0), 2)


# Global GoalPriorityEngine instance
goal_priority_engine = GoalPriorityEngine()
