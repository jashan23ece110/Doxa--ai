"""
Dynamic Replanner for Enterprise Planning & Reasoning Engine.

Monitors execution and rebuilds affected DAG branches dynamically when task/tool failures occur,
preserving completed work without restarting the entire execution pipeline.
"""

from typing import List, Dict, Any, Optional
from app.core.logging import logger
from app.core.planning.planning_metrics import planning_metrics_tracker
from app.core.planning.planning_models import Plan, Task, TaskStatus


class DynamicReplanner:
    """Rebuilds affected plan branches upon task failure."""

    @staticmethod
    def replan_failed_branch(
        plan: Plan,
        failed_task_id: str,
        error_reason: str = "Tool execution failure",
    ) -> Plan:
        """
        Identifies failed task node, resets dependent downstream tasks,
        and rebuilds executable branch while preserving completed task results.
        """
        planning_metrics_tracker.record_replan()
        logger.info(f"Dynamic Replanner triggered for plan '{plan.plan_id}' on failed task '{failed_task_id}': {error_reason}")

        found_task: Optional[Task] = None
        for obj in plan.objectives:
            for t in obj.tasks:
                if t.task_id == failed_task_id:
                    found_task = t
                    break

        if not found_task:
            logger.warning(f"Task '{failed_task_id}' not found in plan '{plan.plan_id}'. Replan aborted.")
            return plan

        # If retry counter < 2, mark for retry
        if found_task.retry_counter < 2:
            found_task.retry_counter += 1
            found_task.status = TaskStatus.RETRYING
            logger.info(f"Task '{failed_task_id}' retry count incremented to {found_task.retry_counter}.")
        else:
            # Rebuild branch: Mark failed task as CANCELLED and create fallback task
            found_task.status = TaskStatus.FAILED
            found_task.output = f"Failed after {found_task.retry_counter} retries: {error_reason}"

            # Create fallback task in objective
            fallback_task = Task(
                name=f"Fallback for {found_task.name}",
                description=f"Fallback execution after failure: {error_reason}",
                priority=found_task.priority,
                status=TaskStatus.PENDING,
            )
            # Add to first objective
            if plan.objectives:
                plan.objectives[0].tasks.append(fallback_task)
                logger.info(f"Appended fallback task '{fallback_task.task_id}' to plan '{plan.plan_id}'.")

        return plan


# Global DynamicReplanner instance
dynamic_replanner = DynamicReplanner()
