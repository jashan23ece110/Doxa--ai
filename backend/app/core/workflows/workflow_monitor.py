"""
Workflow Monitor for Autonomous Workflow Execution Engine.

Tracks progress, ETA, active nodes, failed nodes, resource usage, and execution graphs.
"""

from typing import Dict, Any
from app.core.workflows.workflow_models import Workflow, WorkflowExecution, WorkflowState


class WorkflowMonitor:
    """Monitors active workflow execution state and progress."""

    @staticmethod
    def inspect_workflow(workflow: Workflow) -> WorkflowExecution:
        """Inspects and returns live workflow execution metrics."""
        total = len(workflow.nodes)
        completed = sum(1 for n in workflow.nodes.values() if n.status == WorkflowState.COMPLETED)
        failed = sum(1 for n in workflow.nodes.values() if n.status == WorkflowState.FAILED)
        active_ids = [n.node_id for n in workflow.nodes.values() if n.status == WorkflowState.RUNNING]

        progress = round((completed / max(total, 1)) * 100.0, 2)

        return WorkflowExecution(
            workflow_id=workflow.workflow_id,
            active_node_ids=active_ids,
            progress_percentage=progress,
        )


# Global WorkflowMonitor instance
workflow_monitor = WorkflowMonitor()
