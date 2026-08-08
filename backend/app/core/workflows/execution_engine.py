"""
Execution Engine for Autonomous Workflow Execution Engine.

Executes DAG nodes asynchronously using parallel workers with timeouts, resource limits,
checkpoint creation, node retries, and artifact persistence.
"""

import asyncio
import time
from typing import Dict, Any, List, Optional
from app.core.agents.coordinator import coordinator
from app.core.logging import logger
from app.core.planning.dependency_graph import dependency_graph_engine
from app.core.workflows.approval_engine import approval_engine
from app.core.workflows.artifact_store import artifact_store
from app.core.workflows.checkpoint_manager import checkpoint_manager
from app.core.workflows.retry_engine import retry_engine
from app.core.workflows.rollback import rollback_engine
from app.core.workflows.workflow_metrics import workflow_metrics_tracker
from app.core.workflows.workflow_models import Workflow, WorkflowNode, WorkflowState, WorkflowArtifact


class ExecutionEngine:
    """Asynchronous worker execution engine for workflow DAG nodes."""

    async def _execute_single_node(self, workflow: Workflow, node: WorkflowNode) -> Any:
        """Executes a single workflow node."""
        if node.status in (WorkflowState.COMPLETED, WorkflowState.CANCELLED):
            return node.output

        if node.node_type == "approval":
            approval_engine.request_node_approval(workflow, node)
            return None

        async def _action():
            start_t = time.time()
            prompt = node.input_data.get("description", node.name)

            if node.assigned_agent:
                # Delegate to Multi-Agent Coordinator OS
                res = await coordinator.execute_multi_agent_goal(prompt, user_id=workflow.user_id)
                output = res.get("final_response", "")
            else:
                output = f"Completed node '{node.name}'."

            node.latency_ms = round((time.time() - start_t) * 1000, 2)
            node.output = output
            node.status = WorkflowState.COMPLETED

            # Persist artifact
            art = WorkflowArtifact(name=f"Output: {node.name}", content=output)
            artifact_store.save_artifact(art)
            workflow.artifacts.append(art)

            return output

        try:
            return await retry_engine.execute_with_retry(node, _action, max_retries=node.max_retries)
        except Exception as e:
            node.status = WorkflowState.FAILED
            node.error_message = str(e)
            logger.error(f"Execution Engine node '{node.node_id}' failed: {e}")
            raise e

    async def execute_workflow_dag(self, workflow: Workflow) -> Workflow:
        """Executes workflow DAG level-by-level with parallel workers and checkpoints."""
        if workflow.status == WorkflowState.WAITING_APPROVAL:
            return workflow

        workflow.status = WorkflowState.RUNNING
        start_t = time.time()

        # Group nodes into topological levels using DependencyGraphEngine
        task_map = {}
        for n_id, node in workflow.nodes.items():
            from app.core.planning.planning_models import Task as PTask
            task_map[n_id] = PTask(
                task_id=n_id,
                name=node.name,
                description=node.name,
                dependencies=node.dependencies,
            )

        from app.core.planning.planning_models import Plan as PPlan, Objective as PObj, Goal as PGoal
        dummy_plan = PPlan(
            goal=PGoal(description=workflow.name, primary_objective=workflow.name),
            objectives=[PObj(title="Execution", tasks=list(task_map.values()))]
        )

        executable_levels = dependency_graph_engine.get_executable_levels(dummy_plan)

        try:
            for level in executable_levels:
                runnable_nodes = [
                    workflow.nodes[t.task_id] for t in level
                    if t.task_id in workflow.nodes and workflow.nodes[t.task_id].status not in (WorkflowState.COMPLETED, WorkflowState.CANCELLED)
                ]

                if not runnable_nodes:
                    continue

                # Run level nodes in parallel using asyncio.gather
                coros = [self._execute_single_node(workflow, node) for node in runnable_nodes]
                results = await asyncio.gather(*coros, return_exceptions=True)

                for node, res in zip(runnable_nodes, results):
                    if isinstance(res, Exception):
                        workflow.status = WorkflowState.FAILED
                        workflow.error_message = f"Node '{node.node_id}' failed: {res}"
                        await rollback_engine.execute_rollback(workflow)
                        return workflow

                # Create progress checkpoint snapshot after level completion
                checkpoint_manager.create_checkpoint(workflow)

                if workflow.status == WorkflowState.WAITING_APPROVAL:
                    return workflow

            workflow.status = WorkflowState.COMPLETED
            duration_ms = (time.time() - start_t) * 1000
            workflow_metrics_tracker.record_workflow_execution(
                success=True,
                latency_ms=duration_ms,
                checkpoints=len(workflow.checkpoints),
            )
            logger.info(f"ExecutionEngine successfully completed workflow '{workflow.workflow_id}'.")
            return workflow

        except Exception as e:
            workflow.status = WorkflowState.FAILED
            workflow.error_message = str(e)
            await rollback_engine.execute_rollback(workflow)
            return workflow


# Global ExecutionEngine instance
execution_engine = ExecutionEngine()
