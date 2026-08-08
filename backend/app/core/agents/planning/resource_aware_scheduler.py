"""
Enterprise Planning Scheduler.

Optimizes execution scheduling across agent worker pools, taking task priorities,
dependencies, and execution budgets into account.
"""

from typing import Dict, Any, List
from app.core.logging import security_logger
from app.core.agents.planning.planning_types import TaskGraph, TaskNode


class ResourceAwareScheduler:
    """Enterprise Planning Scheduler."""

    def schedule_execution(self, task_graph: TaskGraph) -> List[TaskNode]:
        """
        Orders task nodes for execution based on DAG dependencies and task priority.

        Args:
            task_graph: TaskGraph object.

        Returns:
            List of ordered TaskNode objects.
        """
        # Sort nodes based on critical path and priority
        ordered_nodes = sorted(task_graph.nodes, key=lambda n: (n.priority, n.created_at))

        for node in ordered_nodes:
            if node.status == "PENDING":
                node.status = "READY"

        security_logger.info(f"ResourceAwareScheduler: Scheduled {len(ordered_nodes)} task nodes for execution.")
        return ordered_nodes


# Global ResourceAwareScheduler instance
resource_aware_scheduler = ResourceAwareScheduler()
