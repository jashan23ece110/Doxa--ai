"""
Goal Manager for Autonomous Mission Control System.

Manages primary goals, secondary goals, sub-goals, dependencies, completion criteria,
and goal hierarchy trees.
"""

from typing import Dict, Any, List, Optional
from app.core.missions.goal_priority import goal_priority_engine
from app.core.missions.mission_models import GoalItem, Mission


class GoalManager:
    """Manages hierarchical goal trees and dependency linking."""

    @staticmethod
    def build_goal_hierarchy_from_prompt(prompt: str) -> Dict[str, GoalItem]:
        """Constructs a structured goal hierarchy map from a mission prompt."""
        goals: Dict[str, GoalItem] = {}

        # 1. Primary Goal Node
        g1 = GoalItem(
            title="Primary Mission Objective",
            description=prompt,
            business_value=1.0,
            urgency=0.80,
            risk_score=0.10,
        )
        g1.priority_score = goal_priority_engine.calculate_priority(g1)
        goals[g1.goal_id] = g1

        # 2. Sub-Goal 1: Information & Architectural Research
        g2 = GoalItem(
            title="Domain Research & Architectural Specification",
            description=f"Gather knowledge and define spec for '{prompt[:30]}'",
            parent_goal_id=g1.goal_id,
            business_value=0.80,
            urgency=0.70,
            risk_score=0.10,
        )
        g2.priority_score = goal_priority_engine.calculate_priority(g2)
        goals[g2.goal_id] = g2
        g1.sub_goal_ids.append(g2.goal_id)

        # 3. Sub-Goal 2: Core Implementation & Autonomous Execution
        g3 = GoalItem(
            title="Autonomous Execution & Implementation",
            description=f"Execute workflows for '{prompt[:30]}'",
            parent_goal_id=g1.goal_id,
            dependencies=[g2.goal_id],
            business_value=0.90,
            urgency=0.60,
            risk_score=0.15,
        )
        g3.priority_score = goal_priority_engine.calculate_priority(g3)
        goals[g3.goal_id] = g3
        g1.sub_goal_ids.append(g3.goal_id)

        return goals


# Global GoalManager instance
goal_manager = GoalManager()
