"""
Enterprise Autonomous Planning Engine.

Main planning facade orchestrating end-to-end transformation:
High-Level Goal -> Goal Analysis -> Constraint Extraction -> Task Decomposition -> Dependency Graph -> Agent Assignment -> Execution Plan.
"""

import time
from typing import Dict, Any, List, Optional
from app.core.logging import security_logger
from app.core.agents.planning.planning_types import (
    ExecutionPlan, TaskGraph, TaskNode, PlanValidationResult,
    PlanRiskAssessment, PlanningContext
)
from app.core.agents.planning.goal_decomposer import goal_decomposer
from app.core.agents.planning.task_graph_engine import task_graph_engine
from app.core.agents.planning.plan_validator import plan_validator
from app.core.agents.planning.agent_assignment_engine import agent_assignment_engine
from app.core.agents.planning.resource_aware_scheduler import resource_aware_scheduler


class AutonomousPlanningEngine:
    """Enterprise Autonomous Planning Engine Facade."""

    async def create_execution_plan(self, goal_id: str, goal_title: str) -> ExecutionPlan:
        """
        Transforms a high-level goal into a validated, scheduled, agent-assigned ExecutionPlan.

        Args:
            goal_id: Target goal ID string.
            goal_title: High-level goal title string.

        Returns:
            ExecutionPlan object.
        """
        t0 = time.time()
        security_logger.info(f"AutonomousPlanningEngine: Generating plan for goal '{goal_title}' ({goal_id}).")

        # 1. Goal Decomposition
        decomp = goal_decomposer.decompose_goal(goal_id, goal_title)

        # 2. Build Task Graph (DAG)
        graph = task_graph_engine.build_task_graph(decomp.tasks)

        # 3. Validate Plan Safety and Tools
        val_res = plan_validator.validate_plan(graph)
        risk_assess = plan_validator.assess_risk(graph)

        # 4. Agent Assignment
        assignments = agent_assignment_engine.assign_agents(graph.nodes)

        # 5. Resource-Aware Scheduling
        scheduled_nodes = resource_aware_scheduler.schedule_execution(graph)
        graph.nodes = scheduled_nodes

        plan = ExecutionPlan(
            goal_id=goal_id,
            task_graph=graph,
            assignments=assignments,
            risk_assessment=risk_assess,
            version=1,
            status="APPROVED" if val_res.is_valid else "INVALID",
        )

        security_logger.info(f"AutonomousPlanningEngine: Created ExecutionPlan '{plan.plan_id}' for goal '{goal_id}' in {round((time.time() - t0)*1000, 2)}ms.")
        return plan


# Global AutonomousPlanningEngine instance
autonomous_planning_engine = AutonomousPlanningEngine()
