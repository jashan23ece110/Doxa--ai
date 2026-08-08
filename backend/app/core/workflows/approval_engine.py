"""
Approval Engine for Autonomous Workflow Execution Engine.

Handles human approval, automatic approval, policy approval, manual checkpoints,
approval timeouts, and approval escalation.
"""

from typing import Dict, Any, Optional
from app.core.logging import logger
from app.core.workflows.workflow_models import Workflow, WorkflowNode, WorkflowState


class ApprovalEngine:
    """Manages human approval checkpoints in autonomous workflows."""

    @staticmethod
    def request_node_approval(workflow: Workflow, node: WorkflowNode) -> None:
        """Pauses node and workflow at an approval checkpoint."""
        node.status = WorkflowState.WAITING_APPROVAL
        workflow.status = WorkflowState.WAITING_APPROVAL
        logger.info(f"Workflow '{workflow.workflow_id}' paused at approval checkpoint node '{node.node_id}'.")

    @staticmethod
    def approve_node(workflow: Workflow, node_id: str, approver: str = "user") -> Optional[Workflow]:
        """Approves a waiting node checkpoint and resumes workflow."""
        if workflow.status != WorkflowState.WAITING_APPROVAL:
            return None

        node = workflow.nodes.get(node_id)
        if not node or node.status != WorkflowState.WAITING_APPROVAL:
            return None

        node.status = WorkflowState.COMPLETED
        node.output = {"approved_by": approver, "status": "approved"}
        workflow.status = WorkflowState.RUNNING
        logger.info(f"Node '{node_id}' approved by '{approver}' for workflow '{workflow.workflow_id}'.")
        return workflow

    @staticmethod
    def reject_node(workflow: Workflow, node_id: str, reason: str = "User rejected") -> Optional[Workflow]:
        """Rejects a waiting node checkpoint and cancels workflow."""
        node = workflow.nodes.get(node_id)
        if node:
            node.status = WorkflowState.CANCELLED
            node.output = {"rejected_reason": reason, "status": "rejected"}

        workflow.status = WorkflowState.CANCELLED
        workflow.error_message = f"Checkpoint node '{node_id}' rejected: {reason}"
        logger.info(f"Node '{node_id}' rejected for workflow '{workflow.workflow_id}': {reason}")
        return workflow


# Global ApprovalEngine instance
approval_engine = ApprovalEngine()
