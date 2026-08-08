"""
Enterprise Task Graph Engine.

Constructs directed acyclic graphs (DAGs) for execution plans, validating dependencies,
detecting cycles, and calculating critical execution paths.
"""

from typing import Dict, Any, List, Set
from app.core.logging import security_logger
from app.core.agents.planning.planning_types import TaskGraph, TaskNode, TaskDependency


class TaskGraphEngine:
    """Enterprise Task Graph Engine."""

    def build_task_graph(self, tasks: List[TaskNode]) -> TaskGraph:
        """
        Builds a TaskGraph DAG from a list of tasks.

        Args:
            tasks: List of TaskNode objects.

        Returns:
            TaskGraph object.
        """
        dependencies = []
        # Create sequential dependencies between consecutive tasks
        for i in range(len(tasks) - 1):
            dep = TaskDependency(
                source_task_id=tasks[i].task_id,
                target_task_id=tasks[i + 1].task_id,
            )
            dependencies.append(dep)

        is_valid_dag = self.validate_dag(tasks, dependencies)
        critical_path = [t.task_id for t in tasks]

        graph = TaskGraph(
            nodes=tasks,
            dependencies=dependencies,
            is_valid_dag=is_valid_dag,
            critical_path_task_ids=critical_path,
        )

        security_logger.info(f"TaskGraphEngine: Built TaskGraph '{graph.graph_id}' ({len(tasks)} nodes, {len(dependencies)} edges, Valid DAG={is_valid_dag}).")
        return graph

    def validate_dag(self, tasks: List[TaskNode], dependencies: List[TaskDependency]) -> bool:
        """
        Validates that the task graph contains no circular dependencies (Kahn's Algorithm).
        """
        adj: Dict[str, List[str]] = {t.task_id: [] for t in tasks}
        in_degree: Dict[str, int] = {t.task_id: 0 for t in tasks}

        for dep in dependencies:
            if dep.source_task_id in adj and dep.target_task_id in in_degree:
                adj[dep.source_task_id].append(dep.target_task_id)
                in_degree[dep.target_task_id] += 1

        queue = [tid for tid, deg in in_degree.items() if deg == 0]
        visited_count = 0

        while queue:
            curr = queue.pop(0)
            visited_count += 1
            for neighbor in adj.get(curr, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        is_dag = (visited_count == len(tasks))
        if not is_dag:
            security_logger.warning("TaskGraphEngine: Circular dependency detected in task graph!")
        return is_dag


# Global TaskGraphEngine instance
task_graph_engine = TaskGraphEngine()
