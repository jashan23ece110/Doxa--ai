"""
Dependency Graph Engine for Enterprise Autonomous Workflow Engine.

Resolves task dependencies, checks for cyclic dependencies, and generates topological execution levels.
"""

from typing import List, Dict, Any, Set, Tuple
from app.core.workflows.workflow_state import WorkflowTask, WorkflowState


class DependencyGraph:
    """DAG engine for workflow tasks."""

    def __init__(self, tasks: Dict[str, WorkflowTask]):
        self.tasks = tasks

    def has_cycles(self) -> bool:
        """Checks if the dependency graph contains cyclic dependencies."""
        visited: Set[str] = set()
        rec_stack: Set[str] = set()

        def dfs(node_id: str) -> bool:
            visited.add(node_id)
            rec_stack.add(node_id)

            task = self.tasks.get(node_id)
            if task:
                for dep in task.dependencies:
                    if dep not in visited:
                        if dfs(dep):
                            return True
                    elif dep in rec_stack:
                        return True

            rec_stack.remove(node_id)
            return False

        for task_id in self.tasks:
            if task_id not in visited:
                if dfs(task_id):
                    return True
        return False

    def get_executable_levels(self) -> List[List[WorkflowTask]]:
        """Groups tasks into topological levels executable in parallel."""
        completed: Set[str] = {
            t_id for t_id, t in self.tasks.items()
            if t.status == WorkflowState.COMPLETED
        }
        remaining = {
            t_id: t for t_id, t in self.tasks.items()
            if t.status not in (WorkflowState.COMPLETED, WorkflowState.CANCELLED)
        }
        levels: List[List[WorkflowTask]] = []

        while remaining:
            ready_level = [
                task for task in remaining.values()
                if set(task.dependencies).issubset(completed)
            ]

            if not ready_level:
                # Break stuck state
                ready_level = list(remaining.values())

            levels.append(ready_level)
            for task in ready_level:
                del remaining[task.task_id]
                completed.add(task.task_id)

        return levels
