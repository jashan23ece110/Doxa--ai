"""
Global Optimization Orchestrator.

Master orchestrator driving end-to-end mathematical optimization workflows:
Objective -> Constraints -> Resources -> Model Construction -> Solver Execution -> Feasibility -> Scenarios -> Sensitivity -> Trade-off Evaluation -> Recommendation.
"""

import time
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.decision_intelligence.optimization.optimization_types import (
    Resource, OptimizationSolution, AllocationPlan, OptimizationExplanation, OptimizationScenario, OptimizationTradeoff
)
from app.core.decision_intelligence.optimization.objective_engine import objective_engine
from app.core.decision_intelligence.optimization.constraint_engine import constraint_engine
from app.core.decision_intelligence.optimization.optimization_model_engine import optimization_model_engine, OptimizationModel
from app.core.decision_intelligence.optimization.resource_allocation_engine import resource_allocation_engine
from app.core.decision_intelligence.optimization.multi_objective_engine import multi_objective_engine
from app.core.decision_intelligence.optimization.optimization_scenario_engine import optimization_scenario_engine
from app.core.decision_intelligence.optimization.optimization_evaluator import optimization_evaluator
from app.core.decision_intelligence.optimization.sensitivity_engine import sensitivity_engine


class MasterOptimizationResult(BaseModel):
    analysis_id: str = Field(default_factory=lambda: f"mopt_{int(time.time() * 1000)}")
    request_title: str
    solution: OptimizationSolution
    allocation_plan: AllocationPlan
    explanation: OptimizationExplanation
    scenarios: List[OptimizationScenario] = Field(default_factory=list)
    tradeoff: OptimizationTradeoff
    requires_human_approval: bool = True
    status: str = "COMPLETED"
    summary: str = "Optimization analysis completed with optimal resource allocation plan."
    executed_at: float = Field(default_factory=time.time)


class OptimizationOrchestrator:
    """Global Optimization Orchestrator Facade."""

    async def execute_optimization_analysis(self, title: str) -> MasterOptimizationResult:
        """
        Executes end-to-end optimization analysis and resource allocation pipeline.

        Args:
            title: Request title string.

        Returns:
            MasterOptimizationResult object.
        """
        t0 = time.time()
        security_logger.info(f"OptimizationOrchestrator: Initiating optimization analysis for '{title}'.")

        # 1. Objectives, Constraints, and Resources
        objectives = objective_engine.build_objectives(title)
        cset = constraint_engine.build_constraint_set(title)
        resources = [
            Resource(name="COMPUTE", total_capacity=1000.0),
            Resource(name="WORKFORCE", total_capacity=500.0),
        ]

        # 2. Model Construction & Solver Execution
        model = OptimizationModel(
            name=f"OptimizationModel_{title}",
            paradigm="MIXED_INTEGER_PROGRAMMING",
            objectives=objectives,
            constraints=cset.constraints,
        )
        sol = optimization_model_engine.solve_optimization_model(model)

        # 3. Resource Allocation Plan & Multi-Objective Pareto Frontier
        aplan = resource_allocation_engine.allocate_resources(resources)
        tradeoff = multi_objective_engine.compute_pareto_frontier(objectives)

        # 4. Scenarios & Sensitivity Analysis & Solution Evaluation
        scenarios = optimization_scenario_engine.evaluate_optimization_scenarios(sol.best_solution.objective_values[0].value)
        sensitivity_engine.analyze_sensitivity(model.model_id)
        expl = optimization_evaluator.evaluate_solution(sol)

        res = MasterOptimizationResult(
            request_title=title,
            solution=sol,
            allocation_plan=aplan,
            explanation=expl,
            scenarios=scenarios,
            tradeoff=tradeoff,
            requires_human_approval=True,
            status="COMPLETED",
        )

        security_logger.info(f"OptimizationOrchestrator: Completed optimization analysis '{res.analysis_id}' for '{title}' in {round((time.time() - t0)*1000, 2)}ms (Efficiency={aplan.efficiency_score}).")
        return res


# Global OptimizationOrchestrator instance
optimization_orchestrator = OptimizationOrchestrator()
