"""
Dynamic Replanning Engine.

Triggers runtime plan revisions when task execution failures, dependency shifts,
or policy changes occur while preserving plan history.
"""

import time
from typing import Dict, Any, Optional
from app.core.logging import security_logger
from app.core.agents.planning.planning_types import ExecutionPlan, PlanRevision, ReplanningEvent, TaskNode
from app.core.agents.planning.task_graph_engine import task_graph_engine


class DynamicReplanner:
    """Dynamic Replanning Engine."""

    def replan_failed_task(self, original_plan: ExecutionPlan, failed_task_id: str, error_reason: str) -> ExecutionPlan:
        """
        Generates a revised execution plan to recover from a failed task.

        Args:
            original_plan: Original ExecutionPlan object.
            failed_task_id: ID of failing task node.
            error_reason: Error description.

        Returns:
            Revised ExecutionPlan object.
        """
        security_logger.warning(f"DynamicReplanner: Triggering replanning for plan '{original_plan.plan_id}' (Failed Task='{failed_task_id}', Reason='{error_reason}').")

        # 1. Clone nodes and mark failed task
        new_nodes = []
        for node in original_plan.task_graph.nodes:
            if node.task_id == failed_task_id:
                # Add recovery task replacement
                rec_node = TaskNode(
                    title=f"Recovery: {node.title}",
                    description=f"Fallback recovery for task '{node.title}' (Error: {error_reason})",
                    required_capability=node.required_capability,
                    priority=node.priority,
                )
                new_nodes.append(rec_node)
            else:
                new_nodes.append(node)

        # 2. Build revised graph
        rev_graph = task_graph_engine.build_task_graph(new_nodes)

        # 3. Construct revised plan
        revised_plan = ExecutionPlan(
            goal_id=original_plan.goal_id,
            task_graph=rev_graph,
            assignments=original_plan.assignments,
            risk_assessment=original_plan.risk_assessment,
            version=original_plan.version + 1,
            status="APPROVED",
        )

        event = ReplanningEvent(
            plan_id=original_plan.plan_id,
            trigger_reason=f"Task {failed_task_id} failed: {error_reason}",
        )

        original_plan.status = "REPLANNED"
        security_logger.info(f"DynamicReplanner: Created plan revision v{revised_plan.version} ({revised_plan.plan_id}).")
        return revised_plan


# Global DynamicReplanner instance
dynamic_replanner = DynamicReplanner()
