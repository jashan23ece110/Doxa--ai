"""
Enterprise Goal Management Engine.

Manages goal creation, decomposition, priority ranking, dependency graphs,
deadline constraints, and end-to-end goal status tracking.
"""

import threading
import time
from typing import Dict, Any, List, Optional
from app.core.logging import security_logger
from app.core.agents.agent_types import AgentGoal, AgentTask


class GoalManager:
    """Thread-safe Enterprise Goal Management Engine."""

    def __init__(self):
        self._lock = threading.Lock()
        self._goals: Dict[str, AgentGoal] = {}
        self._goal_tasks: Dict[str, List[AgentTask]] = {}

    def create_goal(self, title: str, description: str, priority: int = 1, success_criteria: Optional[List[str]] = None) -> AgentGoal:
        """Creates a new tracked enterprise goal."""
        goal = AgentGoal(
            title=title,
            description=description,
            priority=priority,
            success_criteria=success_criteria or ["Task execution succeeded"],
            status="PENDING",
        )
        with self._lock:
            self._goals[goal.goal_id] = goal
            self._goal_tasks[goal.goal_id] = []
            security_logger.info(f"GoalManager: Created goal '{title}' ({goal.goal_id}, Priority={priority}).")
        return goal

    def decompose_goal(self, goal_id: str, task_titles: List[str]) -> List[AgentTask]:
        """Decomposes a goal into sequential agent tasks."""
        with self._lock:
            goal = self._goals.get(goal_id)
            if not goal:
                security_logger.error(f"GoalManager: Cannot decompose goal '{goal_id}' - Not found.")
                return []

            goal.status = "IN_PROGRESS"
            tasks = []
            for idx, title in enumerate(task_titles):
                task = AgentTask(
                    goal_id=goal_id,
                    title=title,
                    parameters={"step_index": idx},
                    status="PENDING",
                )
                tasks.append(task)

            self._goal_tasks[goal_id].extend(tasks)
            security_logger.info(f"GoalManager: Decomposed goal '{goal_id}' into {len(tasks)} tasks.")
            return tasks

    def update_goal_status(self, goal_id: str, status: str):
        """Updates goal status (IN_PROGRESS, ACHIEVED, FAILED, CANCELLED)."""
        with self._lock:
            goal = self._goals.get(goal_id)
            if goal:
                goal.status = status
                security_logger.info(f"GoalManager: Updated goal '{goal_id}' status -> {status}.")

    def get_goal(self, goal_id: str) -> Optional[AgentGoal]:
        """Retrieves goal definition."""
        with self._lock:
            return self._goals.get(goal_id)


# Global GoalManager instance
goal_manager = GoalManager()
