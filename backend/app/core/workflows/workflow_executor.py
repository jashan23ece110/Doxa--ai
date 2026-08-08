"""
Workflow Executor Engine for Enterprise Autonomous Workflow Engine.

Executes workflow DAG tasks level-by-level asynchronously, managing checkpoints, approvals, retries, and compensation rollbacks.
"""

import asyncio
import time
from typing import Dict, Any, List, Optional
from app.core.agents.collaboration_manager import collaboration_manager
from app.core.diagnostics import DiagnosticSpan
from app.core.logging import logger
from app.core.workflows.approval_engine import approval_engine
from app.core.workflows.checkpoint_manager import checkpoint_manager
from app.core.workflows.compensation_engine import compensation_engine
from app.core.workflows.dependency_graph import DependencyGraph
from app.core.workflows.retry_engine import retry_engine
from app.core.workflows.workflow_repository import workflow_repository
from app.core.workflows.workflow_state import WorkflowInstance, WorkflowTask, WorkflowState


class WorkflowExecutor:
    """Executes workflow DAG tasks level-by-level asynchronously."""

    async def _execute_single_task(
        self,
        workflow: WorkflowInstance,
        task: WorkflowTask,
    ) -> Any:
        """Executes a single workflow task."""
        if task.status in (WorkflowState.COMPLETED, WorkflowState.CANCELLED):
            return task.output

        # Handle Human Approval Checkpoint
        if task.requires_approval or task.type == "approval_checkpoint":
            approval_engine.request_approval(workflow, task)
            return None

        async def _run_task():
            start_t = time.time()
            prompt = workflow.state_variables.get("goal", workflow.name)

            if task.assigned_agent:
                # Execute via Multi-Agent Collaboration Engine
                agent_res = await collaboration_manager.execute_multi_agent_workflow(
                    prompt, user_id=workflow.user_id
                )
                output = agent_res.get("final_response", "")
            else:
                output = f"Completed task '{task.name}' for workflow '{workflow.workflow_id}'."

            task.latency_ms = round((time.time() - start_t) * 1000, 2)
            task.output = output
            return output

        try:
            res = await retry_engine.execute_with_retry(task, _run_task)
            return res
        except Exception as e:
            logger.error(f"Task '{task.task_id}' failed permanently: {e}")
            raise e

    async def execute_workflow(self, workflow: WorkflowInstance) -> WorkflowInstance:
        """Executes full workflow DAG tasks with checkpoints, retries, and compensation."""
        if workflow.status == WorkflowState.WAITING:
            logger.info(f"Workflow '{workflow.workflow_id}' is waiting for human approval. Pausing execution.")
            return workflow

        workflow.status = WorkflowState.RUNNING
        workflow_repository.save(workflow)

        dep_graph = DependencyGraph(workflow.tasks)
        executable_levels = dep_graph.get_executable_levels()

        try:
            with DiagnosticSpan(span_name="workflow_execution", slow_threshold_ms=1000.0, category="general"):
                for level_idx, level_tasks in enumerate(executable_levels):
                    # Filter executable tasks
                    runnable = [
                        t for t in level_tasks
                        if t.status not in (WorkflowState.COMPLETED, WorkflowState.CANCELLED)
                    ]

                    if not runnable:
                        continue

                    # Execute level tasks in parallel using asyncio.gather
                    level_coros = [
                        self._execute_single_task(workflow, task)
                        for task in runnable
                    ]
                    results = await asyncio.gather(*level_coros, return_exceptions=True)

                    for task, res in zip(runnable, results):
                        if isinstance(res, Exception):
                            workflow.status = WorkflowState.FAILED
                            workflow.error_message = f"Task '{task.task_id}' failed: {res}"
                            # Execute rollback compensation
                            await compensation_engine.execute_compensation(workflow)
                            workflow_repository.save(workflow)
                            return workflow

                    # Save checkpoint snapshot after each level
                    checkpoint_manager.create_checkpoint(workflow)

                    # If workflow hit an approval checkpoint, break execution loop cleanly
                    if workflow.status == WorkflowState.WAITING:
                        return workflow

            workflow.status = WorkflowState.COMPLETED
            workflow_repository.save(workflow)
            logger.info(f"Successfully completed workflow '{workflow.workflow_id}'.")
            return workflow

        except Exception as e:
            logger.error(f"Workflow '{workflow.workflow_id}' execution error: {e}")
            workflow.status = WorkflowState.FAILED
            workflow.error_message = str(e)
            await compensation_engine.execute_compensation(workflow)
            workflow_repository.save(workflow)
            return workflow


# Global WorkflowExecutor instance
workflow_executor = WorkflowExecutor()
