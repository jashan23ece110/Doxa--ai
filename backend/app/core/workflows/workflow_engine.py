"""
Autonomous Workflow Engine Orchestrator.

Central lifecycle manager for workflow creation, execution, pause, resume, cancel,
restart, retry, rollback, and completion.
"""

import time
from typing import Dict, Any, List, Optional
from app.core.config import settings
from app.core.planning.planning_engine import planning_engine
from app.core.workflows.approval_engine import approval_engine
from app.core.workflows.execution_engine import execution_engine
from app.core.workflows.rollback import rollback_engine
from app.core.workflows.workflow_builder import workflow_builder
from app.core.workflows.workflow_models import Workflow, WorkflowResult, WorkflowState


class WorkflowEngine:
    """Central orchestrator for Autonomous Workflow Execution Platform."""

    async def execute_goal_workflow(
        self,
        goal_prompt: str,
        user_id: str = "default_user",
        policy: str = "balanced",
    ) -> WorkflowResult:
        """
        Full workflow lifecycle execution:
        Prompt -> Enterprise Plan -> Workflow DAG -> Exec Engine -> Checkpoints & Artifacts.
        """
        start_t = time.time()

        # 1. Create Enterprise Plan
        plan = planning_engine.create_enterprise_plan(goal_prompt, policy=policy)

        # 2. Build Executable Workflow DAG
        workflow = workflow_builder.build_workflow_from_plan(plan, user_id=user_id)

        # 3. Execute Workflow DAG via ExecutionEngine
        updated_wf = await execution_engine.execute_workflow_dag(workflow)

        duration_s = round(time.time() - start_t, 2)

        final_output = ""
        for n in reversed(list(updated_wf.nodes.values())):
            if n.output and isinstance(n.output, str):
                final_output = n.output
                break

        return WorkflowResult(
            workflow_id=updated_wf.workflow_id,
            status=updated_wf.status,
            output=final_output or f"Workflow '{updated_wf.name}' completed with status '{updated_wf.status.value}'.",
            artifacts=updated_wf.artifacts,
            execution_duration_s=duration_s,
        )

    def pause_workflow(self, workflow: Workflow) -> Workflow:
        """Pauses a running workflow."""
        if workflow.status == WorkflowState.RUNNING:
            workflow.status = WorkflowState.PAUSED
        return workflow

    async def resume_workflow(self, workflow: Workflow) -> Workflow:
        """Resumes a paused or waiting workflow."""
        if workflow.status in (WorkflowState.PAUSED, WorkflowState.WAITING_APPROVAL):
            return await execution_engine.execute_workflow_dag(workflow)
        return workflow

    def approve_checkpoint_node(self, workflow: Workflow, node_id: str, approver: str = "user") -> Optional[Workflow]:
        """Approves a waiting approval checkpoint node."""
        return approval_engine.approve_node(workflow, node_id, approver)


# Global WorkflowEngine instance
workflow_engine = WorkflowEngine()
