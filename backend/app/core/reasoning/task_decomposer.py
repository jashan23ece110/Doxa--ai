"""
Task Decomposer for Enterprise Cognitive Reasoning Engine.

Splits complex goals into structured hierarchical subtasks for DAG planning and execution.
"""

import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class SubTask(BaseModel):
    """Subtask node definition in a cognitive decomposition plan."""

    task_id: str
    parent_id: Optional[str] = None
    type: str  # research, memory, execution, verification, synthesis
    description: str
    dependencies: List[str] = Field(default_factory=list)
    priority: int = 1
    status: str = "pending"  # pending, running, completed, failed
    output: Optional[Any] = None


class TaskDecomposer:
    """Decomposes complex goals into hierarchical subtasks."""

    @staticmethod
    def decompose_goal(goal: str, complexity_level: str = "medium") -> List[SubTask]:
        """Decomposes a user goal into an ordered list of dependent subtasks."""
        if not goal or not goal.strip():
            return []

        clean_goal = goal.strip()

        # If simple query, single task
        if complexity_level == "simple" or len(clean_goal.split()) <= 4:
            return [
                SubTask(
                    task_id="task_1",
                    type="synthesis",
                    description=f"Direct completion for query: {clean_goal}",
                    dependencies=[],
                    priority=1,
                )
            ]

        # Multi-step or Complex decomposition
        subtasks = [
            SubTask(
                task_id="task_1",
                type="research",
                description=f"Retrieve document knowledge and search context for '{clean_goal[:40]}'",
                dependencies=[],
                priority=1,
            ),
            SubTask(
                task_id="task_2",
                type="memory",
                description="Retrieve user long-term memory and personalization preferences",
                dependencies=[],
                priority=1,
            ),
        ]

        # Check if calculation/python execution is required
        if any(kw in clean_goal.lower() for kw in ["calculate", "compute", "python", "code", "date", "calendar"]):
            subtasks.append(
                SubTask(
                    task_id="task_3",
                    type="execution",
                    description="Execute auxiliary computation or tool integration",
                    dependencies=["task_1"],
                    priority=2,
                )
            )
            subtasks.append(
                SubTask(
                    task_id="task_4",
                    type="verification",
                    description="Audit retrieved evidence and tool outputs for factual consistency",
                    dependencies=["task_1", "task_2", "task_3"],
                    priority=3,
                )
            )
            subtasks.append(
                SubTask(
                    task_id="task_5",
                    type="synthesis",
                    description="Synthesize final verified answer",
                    dependencies=["task_4"],
                    priority=4,
                )
            )
        else:
            subtasks.append(
                SubTask(
                    task_id="task_3",
                    type="verification",
                    description="Audit retrieved evidence for factual consistency",
                    dependencies=["task_1", "task_2"],
                    priority=2,
                )
            )
            subtasks.append(
                SubTask(
                    task_id="task_4",
                    type="synthesis",
                    description="Synthesize final verified answer",
                    dependencies=["task_3"],
                    priority=3,
                )
            )

        return subtasks


# Global TaskDecomposer instance
task_decomposer = TaskDecomposer()
