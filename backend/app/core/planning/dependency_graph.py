"""
Dependency Graph Engine for Enterprise Planning & Reasoning Engine.

Represents plans as Directed Acyclic Graphs (DAGs) supporting parallel branches,
serial branches, cycle detection, critical path calculation, and dependency resolution.
"""

from typing import List, Dict, Any, Set, Tuple
from app.core.planning.planning_models import Plan, Task, Dependency, TaskStatus


class DependencyGraphEngine:
    """DAG engine for plan dependency resolution and critical path calculation."""

    @staticmethod
    def extract_tasks_from_plan(plan: Plan) -> Dict[str, Task]:
        """Flattens all tasks across plan objectives into a map by task_id."""
        task_map = {}
        for obj in plan.objectives:
            for task in obj.tasks:
                task_map[task.task_id] = task
        return task_map

    @classmethod
    def check_for_cycles(cls, plan: Plan) -> bool:
        """Detects cycles in plan dependency graph. Returns True if cycle found."""
        tasks = cls.extract_tasks_from_plan(plan)
        visited = set()
        rec_stack = set()

        def _dfs(task_id: str) -> bool:
            visited.add(task_id)
            rec_stack.add(task_id)

            task = tasks.get(task_id)
            if task:
                for dep_id in task.dependencies:
                    if dep_id not in visited:
                        if _dfs(dep_id):
                            return True
                    elif dep_id in rec_stack:
                        return True

            rec_stack.remove(task_id)
            return False

        for t_id in tasks:
            if t_id not in visited:
                if _dfs(t_id):
                    return True
        return False

    @classmethod
    def get_executable_levels(cls, plan: Plan) -> List[List[Task]]:
        """
        Groups tasks into topological levels for parallel branch execution.
        Level 0 = independent tasks, Level 1 = tasks depending on Level 0, etc.
        """
        tasks = cls.extract_tasks_from_plan(plan)
        if not tasks:
            return []

        resolved: Set[str] = set()
        levels: List[List[Task]] = []
        remaining = set(tasks.keys())

        while remaining:
            current_level = []
            for t_id in list(remaining):
                t = tasks[t_id]
                # Task is ready if all dependencies are resolved
                if all(dep in resolved for dep in t.dependencies):
                    current_level.append(t)

            if not current_level:
                # Cycle or unresolved dependency safeguard
                current_level = [tasks[t_id] for t_id in remaining]
                levels.append(current_level)
                break

            levels.append(current_level)
            for t in current_level:
                resolved.add(t.task_id)
                remaining.remove(t.task_id)

        return levels

    @classmethod
    def calculate_critical_path(cls, plan: Plan) -> Tuple[int, float]:
        """Calculates critical path length (depth) and total estimated duration."""
        levels = cls.get_executable_levels(plan)
        depth = len(levels)
        total_duration = sum(
            max(t.estimated_duration_s for t in lvl) if lvl else 0.0
            for lvl in levels
        )
        return depth, round(total_duration, 2)


# Global DependencyGraphEngine instance
dependency_graph_engine = DependencyGraphEngine()
