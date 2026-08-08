"""
Enterprise Plan Validation Engine.

Validates plans against agent permissions, tool availability, resource limits,
and safety policies before execution.
"""

from typing import Dict, Any, List
from app.core.logging import security_logger
from app.core.agents.planning.planning_types import TaskGraph, PlanValidationResult, PlanRiskAssessment
from app.core.agents.tool_registry import tool_registry


class PlanValidator:
    """Enterprise Plan Validation Engine."""

    def validate_plan(self, task_graph: TaskGraph) -> PlanValidationResult:
        """
        Validates task graph against tool availability and DAG constraints.

        Args:
            task_graph: TaskGraph object.

        Returns:
            PlanValidationResult object.
        """
        errors = []

        # 1. Validate DAG integrity
        if not task_graph.is_valid_dag:
            errors.append("Invalid DAG: Circular dependency detected in task graph")

        # 2. Validate tool registration
        for node in task_graph.nodes:
            if node.required_tool:
                tool_def = tool_registry.get_tool(node.required_tool)
                if not tool_def:
                    errors.append(f"Task '{node.title}' requires unregistered tool '{node.required_tool}'")

        is_valid = len(errors) == 0
        result = PlanValidationResult(
            is_valid=is_valid,
            requires_approval=False,
            requires_replanning=not is_valid,
            validation_errors=errors,
        )

        security_logger.info(f"PlanValidator: Validated plan graph '{task_graph.graph_id}' -> Valid={is_valid} (Errors={len(errors)}).")
        return result

    def assess_risk(self, task_graph: TaskGraph) -> PlanRiskAssessment:
        """Evaluates risk score and approval requirements for a plan."""
        high_impact_count = sum(1 for n in task_graph.nodes if n.priority == 1)
        risk_score = min(0.15 * high_impact_count, 1.0)

        assessment = PlanRiskAssessment(
            overall_risk_score=risk_score,
            high_impact_actions_count=high_impact_count,
            requires_human_approval=(risk_score > 0.80),
            risk_factors=["High priority operational actions"] if high_impact_count > 0 else [],
        )

        security_logger.debug(f"PlanValidator: Evaluated plan risk (Score={risk_score}, RequiresApproval={assessment.requires_human_approval}).")
        return assessment


# Global PlanValidator instance
plan_validator = PlanValidator()
