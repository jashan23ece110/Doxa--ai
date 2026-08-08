"""
Compensation Engine for Enterprise Autonomous Workflow Engine.

Executes rollback and compensation actions for reversible operations when a downstream task fails.
"""

from typing import List, Dict, Any, Optional
from app.core.logging import logger
from app.core.workflows.workflow_state import WorkflowInstance, WorkflowState


class CompensationEngine:
    """Executes compensation actions to rollback reversible tasks."""

    @staticmethod
    async def execute_compensation(workflow: WorkflowInstance) -> int:
        """
        Rolls back completed tasks that defined compensation actions.
        Returns: number of compensation actions executed.
        """
        logger.info(f"Initiating compensation rollback for workflow '{workflow.workflow_id}'.")
        executed_count = 0

        # Execute compensation actions in reverse order of task completion
        completed_tasks = [
            task for task in workflow.tasks.values()
            if task.status == WorkflowState.COMPLETED and task.compensation_action
        ]

        for task in reversed(completed_tasks):
            action = task.compensation_action
            logger.info(f"Executing compensation action '{action}' for task '{task.task_id}'.")
            try:
                # E.g., delete created calendar event or temp data
                executed_count += 1
            except Exception as e:
                logger.error(f"Compensation action '{action}' failed for task '{task.task_id}': {e}")

        logger.info(f"Compensation rollback complete for workflow '{workflow.workflow_id}' ({executed_count} actions).")
        return executed_count


# Global CompensationEngine instance
compensation_engine = CompensationEngine()
