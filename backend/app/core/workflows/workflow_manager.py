"""
Workflow Manager for Enterprise Autonomous Workflow Engine.

High-level lifecycle manager for creating, pausing, resuming, approving, and querying workflows.
"""

import time
from typing import Dict, Any, List, Optional
from app.core.logging import logger
from app.core.workflows.approval_engine import approval_engine
from app.core.workflows.checkpoint_manager import checkpoint_manager
from app.core.workflows.workflow_executor import workflow_executor
from app.core.workflows.workflow_metrics import workflow_metrics_tracker
from app.core.workflows.workflow_repository import workflow_repository
from app.core.workflows.workflow_state import WorkflowInstance, WorkflowState, WorkflowTask
from app.core.workflows.workflow_templates import workflow_templates
from app.core.workflows.workflow_validator import workflow_validator


class WorkflowManager:
    """Manages workflow creation, lifecycle, pause/resume, and approval flows."""

    async def create_and_start_workflow(
        self,
        goal: str,
        user_id: str = "default_user",
        template_name: Optional[str] = None,
    ) -> WorkflowInstance:
        """Creates a workflow from goal or template and begins async execution."""
        start_t = time.time()

        if template_name:
            workflow = workflow_templates.get_template(template_name, user_id, goal)
        else:
            workflow = workflow_templates.create_research_report_template(user_id, goal)

        # Validate workflow integrity
        is_valid, errors = workflow_validator.validate_workflow(workflow)
        if not is_valid:
            workflow.status = WorkflowState.FAILED
            workflow.error_message = f"Validation failed: {', '.join(errors)}"
            workflow_repository.save(workflow)
            return workflow

        workflow_repository.save(workflow)
        logger.info(f"Created workflow '{workflow.workflow_id}' (Template: {workflow.template_name}).")

        # Execute workflow DAG
        updated_wf = await workflow_executor.execute_workflow(workflow)

        duration_ms = (time.time() - start_t) * 1000
        workflow_metrics_tracker.record_workflow_execution(
            success=updated_wf.status == WorkflowState.COMPLETED,
            latency_ms=duration_ms,
            retries=sum(t.retries for t in updated_wf.tasks.values()),
            checkpoints=len(updated_wf.checkpoints),
            cancelled=updated_wf.status == WorkflowState.CANCELLED,
        )

        return updated_wf

    async def resume_workflow(self, workflow_id: str) -> Optional[WorkflowInstance]:
        """Resumes execution of a paused or waiting workflow."""
        workflow = workflow_repository.get(workflow_id)
        if not workflow:
            logger.warning(f"Workflow '{workflow_id}' not found.")
            return None

        if workflow.status in (WorkflowState.COMPLETED, WorkflowState.CANCELLED):
            logger.info(f"Workflow '{workflow_id}' is already in terminal state '{workflow.status}'.")
            return workflow

        logger.info(f"Resuming execution of workflow '{workflow_id}'.")
        return await workflow_executor.execute_workflow(workflow)

    def pause_workflow(self, workflow_id: str) -> Optional[WorkflowInstance]:
        """Pauses execution of a running workflow."""
        workflow = workflow_repository.get(workflow_id)
        if not workflow:
            return None

        if workflow.status == WorkflowState.RUNNING:
            workflow.status = WorkflowState.PAUSED
            workflow_repository.save(workflow)
            logger.info(f"Paused workflow '{workflow_id}'.")

        return workflow

    def approve_workflow_checkpoint(self, workflow_id: str, task_id: str, approver: str = "user") -> Optional[WorkflowInstance]:
        """Approves a human approval checkpoint task."""
        return approval_engine.approve_checkpoint(workflow_id, task_id, approver)

    def reject_workflow_checkpoint(self, workflow_id: str, task_id: str, reason: str = "User rejected") -> Optional[WorkflowInstance]:
        """Rejects a human approval checkpoint task."""
        return approval_engine.reject_checkpoint(workflow_id, task_id, reason)

    def get_workflow_status(self, workflow_id: str) -> Optional[WorkflowInstance]:
        """Retrieves workflow status by ID."""
        return workflow_repository.get(workflow_id)


# Global WorkflowManager instance
workflow_manager = WorkflowManager()
