"""
Execution Monitor for Enterprise Planning & Reasoning Engine.

Tracks running tasks, completed tasks, failed tasks, blocked tasks, retry counts,
execution timeline, critical path progress, and estimated remaining time.
"""

from typing import Dict, Any
from app.core.planning.dependency_graph import dependency_graph_engine
from app.core.planning.planning_models import Plan, ExecutionState, TaskStatus


class ExecutionMonitor:
    """Monitors and updates plan execution progress and metrics."""

    @staticmethod
    def inspect_execution_state(plan: Plan) -> ExecutionState:
        """Calculates execution status counts and progress percentage."""
        tasks_map = dependency_graph_engine.extract_tasks_from_plan(plan)
        total = len(tasks_map)

        completed = 0
        failed = 0
        running = 0
        blocked = 0

        for t in tasks_map.values():
            if t.status == TaskStatus.COMPLETED:
                completed += 1
            elif t.status == TaskStatus.FAILED:
                failed += 1
            elif t.status == TaskStatus.RUNNING:
                running += 1
            elif t.status == TaskStatus.BLOCKED:
                blocked += 1

        crit_depth, _ = dependency_graph_engine.calculate_critical_path(plan)
        progress = round((completed / max(total, 1)) * 100.0, 2)

        return ExecutionState(
            plan_id=plan.plan_id,
            total_tasks=total,
            completed_tasks=completed,
            failed_tasks=failed,
            running_tasks=running,
            blocked_tasks=blocked,
            critical_path_length=crit_depth,
            progress_percentage=progress,
        )


# Global ExecutionMonitor instance
execution_monitor = ExecutionMonitor()
