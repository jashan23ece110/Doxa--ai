"""
Workflow Builder for Autonomous Workflow Execution Engine.

Converts planner DAGs into executable workflow DAGs supporting serial, parallel,
conditional execution, dynamic node generation, and nested workflows.
"""

from typing import Dict, Any, List
from app.core.planning.planning_models import Plan, Task
from app.core.workflows.workflow_models import Workflow, WorkflowNode, WorkflowState


class WorkflowBuilder:
    """Converts planner goals/DAGs into executable Workflow DAG objects."""

    @staticmethod
    def build_workflow_from_plan(plan: Plan, user_id: str = "default_user") -> Workflow:
        """Converts a Plan into an executable Workflow instance."""
        wf = Workflow(
            name=f"Workflow: {plan.goal.description[:40]}",
            user_id=user_id,
            status=WorkflowState.PENDING,
        )

        # Iterate objectives and tasks to construct workflow nodes
        for obj in plan.objectives:
            for task in obj.tasks:
                node = WorkflowNode(
                    node_id=task.task_id,
                    name=task.name,
                    node_type="task",
                    dependencies=task.dependencies,
                    status=WorkflowState.PENDING,
                    assigned_agent=task.required_tools[0] if task.required_tools else "ReasoningAgent",
                    input_data={"description": task.description},
                )
                wf.nodes[node.node_id] = node

        return wf


# Global WorkflowBuilder instance
workflow_builder = WorkflowBuilder()
