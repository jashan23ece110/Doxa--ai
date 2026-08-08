"""
Enterprise Planning & Reasoning Engine Orchestrator.

Main entry point unifying Goal Analysis, Hierarchical Planning, DAG Dependency Resolution,
Decision Engine Scoring, Reasoning Validation, Execution Monitoring, and Dynamic Replanning.
Provides seamless fallback to legacy planning when disabled.
"""

import time
from typing import Dict, Any, List, Optional
from app.core.config import settings
from app.core.diagnostics import DiagnosticSpan
from app.core.logging import logger
from app.core.planning.decision_engine import decision_engine
from app.core.planning.dependency_graph import dependency_graph_engine
from app.core.planning.dynamic_replanner import dynamic_replanner
from app.core.planning.execution_monitor import execution_monitor
from app.core.planning.goal_analyzer import goal_analyzer
from app.core.planning.hierarchical_planner import hierarchical_planner
from app.core.planning.planning_metrics import planning_metrics_tracker
from app.core.planning.planning_models import Plan, Goal, DecisionNode
from app.core.planning.reasoning_engine import reasoning_engine


class PlanningEngine:
    """Main orchestrator for enterprise planning and reasoning."""

    @staticmethod
    def create_enterprise_plan(
        prompt: str,
        policy: str = "balanced",
    ) -> Plan:
        """
        Creates a complete hierarchical execution plan with reasoning traces and decision scoring.
        """
        start_t = time.time()

        with DiagnosticSpan(span_name="create_enterprise_plan", slow_threshold_ms=100.0, category="general"):
            # 1. Goal Analysis
            goal = goal_analyzer.analyze_goal(prompt)

            # 2. Hierarchical Plan Generation
            plan = hierarchical_planner.generate_hierarchical_plan(goal)

            # 3. Structured Reasoning Trace Generation
            plan.reasoning_trace = reasoning_engine.generate_reasoning_trace(goal)

            # 4. Multi-Strategy Decision Selection
            decision_engine.evaluate_and_select_decision(plan, policy=policy)

            # 5. DAG Validation & Critical Path Calculation
            depth, duration = dependency_graph_engine.calculate_critical_path(plan)

            duration_ms = (time.time() - start_t) * 1000
            planning_metrics_tracker.record_plan_creation(
                depth=depth,
                latency_ms=duration_ms,
                confidence=goal.confidence,
            )

            logger.info(
                f"Enterprise Plan '{plan.plan_id}' generated: Goal='{goal.complexity}', "
                f"Depth={depth}, Strategy='{plan.decision.strategy_name if plan.decision else 'balanced'}'"
            )

            return plan

    @staticmethod
    def get_public_plan_summary(plan: Plan) -> Dict[str, Any]:
        """
        Returns a sanitized, public plan summary.
        Keeps internal multi-step reasoning traces isolated from end users.
        """
        exec_state = execution_monitor.inspect_execution_state(plan)
        return {
            "plan_id": plan.plan_id,
            "goal": plan.goal.description,
            "complexity": plan.goal.complexity,
            "status": plan.status.value,
            "strategy": plan.decision.strategy_name if plan.decision else "balanced",
            "critical_path_depth": exec_state.critical_path_length,
            "progress_percentage": exec_state.progress_percentage,
            "objectives_count": len(plan.objectives),
        }


# Global PlanningEngine instance
planning_engine = PlanningEngine()
