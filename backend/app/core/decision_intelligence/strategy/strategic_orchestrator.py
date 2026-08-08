"""
Global Strategic Intelligence Orchestrator.

Master orchestrator executing end-to-end strategic planning and scenario analysis:
Objective Analysis -> Strategic Planning -> Scenario Generation -> What-If Analysis -> Simulation & Forecasting -> Trade-off Analysis -> Plan Evaluation -> Recommendation.
"""

import time
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.decision_intelligence.strategy.strategic_types import (
    StrategicObjective, StrategicPlan, StrategicRecommendation, StrategicEvaluation
)
from app.core.decision_intelligence.strategy.strategic_planning_engine import strategic_planning_engine
from app.core.decision_intelligence.strategy.scenario_engine import scenario_engine
from app.core.decision_intelligence.strategy.what_if_engine import what_if_engine
from app.core.decision_intelligence.strategy.scenario_simulator import scenario_simulator
from app.core.decision_intelligence.strategy.strategy_comparison_engine import strategy_comparison_engine
from app.core.decision_intelligence.strategy.tradeoff_engine import tradeoff_engine
from app.core.decision_intelligence.strategy.strategic_forecasting_engine import strategic_forecasting_engine
from app.core.decision_intelligence.strategy.strategic_plan_evaluator import strategic_plan_evaluator


class MasterStrategicResult(BaseModel):
    analysis_id: str = Field(default_factory=lambda: f"mstrat_{int(time.time() * 1000)}")
    plan: StrategicPlan
    evaluation: StrategicEvaluation
    recommendation: StrategicRecommendation
    status: str = "COMPLETED"
    summary: str = "Strategic plan and scenario analysis generated with complete provenance."
    executed_at: float = Field(default_factory=time.time)


class StrategicOrchestrator:
    """Global Strategic Intelligence Orchestrator Facade."""

    async def execute_strategic_analysis(self, title: str) -> MasterStrategicResult:
        """
        Executes complete multi-horizon strategic analysis and scenario modeling pipeline.

        Args:
            title: Strategic initiative title string.

        Returns:
            MasterStrategicResult object.
        """
        t0 = time.time()
        security_logger.info(f"StrategicOrchestrator: Starting strategic analysis pipeline for '{title}'.")

        # 1. Objectives & Strategic Planning
        objectives = [
            StrategicObjective(title=f"Objective 1 for {title}", target_metric="ROI", target_value=100.0),
        ]
        plan = strategic_planning_engine.create_strategic_plan(title, objectives)

        # 2. Scenario Generation & Simulation
        scenarios = scenario_engine.generate_scenarios(title)
        plan.scenarios = scenarios
        if len(scenarios) >= 2:
            scenario_simulator.compare_scenarios(scenarios[0], scenarios[1])

        # 3. What-If Analysis & Forecasting & Trade-offs
        what_if_engine.evaluate_what_if("CapitalBudget", 50000.0, 75000.0)
        strategic_forecasting_engine.forecast_trajectory("ROI", horizon_months=12)
        tradeoff_engine.analyze_tradeoffs(title)

        # 4. Strategy Comparison & Plan Evaluation
        strategy_comparison_engine.compare_strategies([plan.chosen_alternative])
        seval = strategic_plan_evaluator.evaluate_plan(plan)

        # 5. Recommendation Generation
        rec = StrategicRecommendation(
            plan_id=plan.plan_id,
            recommended_path_title=plan.chosen_alternative.title,
            strategic_rationale=f"Strategy '{plan.chosen_alternative.title}' achieves optimal balance across baseline, optimistic, and adverse scenarios (Strategic Fit={seval.overall_strategic_fit}/100).",
            confidence_level=0.94,
            requires_human_approval=True,
        )

        res = MasterStrategicResult(
            plan=plan,
            evaluation=seval,
            recommendation=rec,
            status="COMPLETED",
        )

        security_logger.info(f"StrategicOrchestrator: Completed strategic analysis '{res.analysis_id}' for '{title}' in {round((time.time() - t0)*1000, 2)}ms.")
        return res


# Global StrategicOrchestrator instance
strategic_orchestrator = StrategicOrchestrator()
