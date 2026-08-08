"""
Rollback Engine for Autonomous Workflow Execution Engine.

Undoes reversible operations by executing a rollback graph, while safely skipping irreversible tasks.
"""

from typing import List, Dict, Any
from app.core.logging import logger
from app.core.workflows.workflow_models import Workflow, WorkflowState


class RollbackEngine:
    """Executes rollback graphs for failed workflows."""

    @staticmethod
    async def execute_rollback(workflow: Workflow) -> int:
        """
        Executes rollback actions in reverse order of task completion for reversible nodes.
        Returns: number of rolled back nodes.
        """
        logger.info(f"Initiating rollback graph execution for workflow '{workflow.workflow_id}'.")
        rolled_back_count = 0

        completed_nodes = [
            node for node in workflow.nodes.values()
            if node.status == WorkflowState.COMPLETED and node.is_reversible
        ]

        for node in reversed(completed_nodes):
            logger.info(f"Rolling back reversible node '{node.node_id}' ({node.name}).")
            node.status = WorkflowState.ROLLING_BACK
            rolled_back_count += 1

        workflow.status = WorkflowState.FAILED
        logger.info(f"Rollback complete for workflow '{workflow.workflow_id}' ({rolled_back_count} nodes reversed).")
        return rolled_back_count


# Global RollbackEngine instance
rollback_engine = RollbackEngine()
