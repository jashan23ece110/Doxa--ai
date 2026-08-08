"""
Decision Orchestrator for Enterprise Decision Platform.

Coordinates long-horizon planning, goal decomposition, constraint solving, risk assessment,
scenario simulation, decision scoring, and resource optimization.
"""

from typing import Dict, Any
from app.core.logging import logger
from app.core.decision.constraint_solver import constraint_solver
from app.core.decision.decision_memory import decision_memory
from app.core.decision.decision_models import DecisionMemoryRecord, DecisionScoreCard, GoalDecomposition, RiskAssessmentReport, ScenarioSimulation, StrategicRoadmap
from app.core.decision.decision_score import decision_scoring_engine
from app.core.decision.goal_decomposer import goal_decomposition_engine
from app.core.decision.opportunity_engine import opportunity_discovery_engine
from app.core.decision.resource_optimizer import resource_optimizer
from app.core.decision.risk_engine import risk_assessment_engine
from app.core.decision.scenario_simulator import scenario_simulator
from app.core.decision.strategic_planner import strategic_planner


class DecisionOrchestrator:
    """Central Orchestrator for Enterprise Decision Intelligence."""

    @staticmethod
    def execute_strategic_decision(goal: str) -> Dict[str, Any]:
        """
        Executes end-to-end goal decomposition, strategic planning, risk assessment, scenario simulation, and decision memory logging.
        """
        logger.info(f"DecisionOrchestrator formulating decision strategy for goal: '{goal}'")

        # 1. Goal Decomposition & Strategic Planning
        decomp = goal_decomposition_engine.decompose_goal(goal)
        roadmap = strategic_planner.create_roadmap(goal)
        constraints_ok = constraint_solver.evaluate_constraints()

        # 2. Risk Assessment & Scenario Simulation
        risk_report = risk_assessment_engine.assess_risk(goal)
        simulation = scenario_simulator.run_simulation(goal)
        scorecard = decision_scoring_engine.score_decision()

        # 3. Resource Optimization & Opportunity Discovery
        res_plan = resource_optimizer.optimize_resources()
        opportunities = opportunity_discovery_engine.discover_opportunities(goal)

        # 4. Decision Memory Logging
        mem_rec = decision_memory.record_decision(
            topic=goal,
            action=f"Deployed roadmap '{roadmap.roadmap_id}' across {len(decomp.milestones)} milestones.",
        )

        return {
            "goal_decomposition": decomp.model_dump(),
            "strategic_roadmap": roadmap.model_dump(),
            "constraints_satisfied": constraints_ok,
            "risk_assessment": risk_report.model_dump(),
            "scenario_simulation": simulation.model_dump(),
            "scorecard": scorecard.model_dump(),
            "resource_plan": res_plan.model_dump(),
            "opportunities": [o.model_dump() for o in opportunities],
            "decision_memory_record": mem_rec.model_dump(),
        }


# Global DecisionOrchestrator instance
decision_orchestrator = DecisionOrchestrator()
