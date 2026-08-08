"""
Adaptive Goal Engine for Autonomous Mission Control System.

Dynamically adapts goals, adds sub-goals, removes obsolete tasks,
and recalculates dependencies when execution context or environment changes.
"""

from typing import Dict, Any, List
from app.core.logging import logger
from app.core.missions.goal_priority import goal_priority_engine
from app.core.missions.mission_models import Mission, GoalItem


class AdaptiveGoalEngine:
    """Dynamically recalculates priorities and adapts goal tree nodes."""

    @staticmethod
    def adapt_mission_goals(mission: Mission, new_context: str = "") -> bool:
        """
        Scans mission goals, updates priorities, and appends adaptive sub-goals if needed.
        """
        logger.info(f"AdaptiveGoalEngine scanning goals for mission '{mission.mission_id}'.")
        adapted = False

        for goal in mission.goals.values():
            old_p = goal.priority_score
            new_p = goal_priority_engine.calculate_priority(goal)
            if old_p != new_p:
                goal.priority_score = new_p
                adapted = True

        # Append adaptive refinement goal if failed goals detected
        failed_goals = [g for g in mission.goals.values() if not g.completed and g.risk_score > 0.30]
        if failed_goals and len(mission.goals) < 10:
            adaptive_sub = GoalItem(
                title="Adaptive Failure Mitigation",
                description="Automatically added adaptive sub-goal to mitigate execution risks.",
                business_value=0.85,
                urgency=0.90,
            )
            adaptive_sub.priority_score = goal_priority_engine.calculate_priority(adaptive_sub)
            mission.goals[adaptive_sub.goal_id] = adaptive_sub
            adapted = True
            logger.info(f"Appended adaptive mitigation sub-goal '{adaptive_sub.goal_id}' to mission '{mission.mission_id}'.")

        return adapted


# Global AdaptiveGoalEngine instance
adaptive_goal_engine = AdaptiveGoalEngine()
