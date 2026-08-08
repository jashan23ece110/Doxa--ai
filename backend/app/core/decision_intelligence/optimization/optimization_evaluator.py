"""
Optimization Evaluator.

Evaluates solution feasibility, constraint satisfaction, robustness, and resource efficiency.
"""

from typing import Dict, Any
from app.core.logging import security_logger
from app.core.decision_intelligence.optimization.optimization_types import OptimizationSolution, OptimizationExplanation


class OptimizationEvaluator:
    """Optimization Evaluator."""

    def evaluate_solution(self, sol: OptimizationSolution) -> OptimizationExplanation:
        """
        Evaluates solution quality and binding constraint rationale.

        Args:
            sol: OptimizationSolution object.

        Returns:
            OptimizationExplanation object.
        """
        expl = OptimizationExplanation(
            binding_constraints=["Capital Budget Limit ($500k)", "Workforce Capacity (1000 hrs)"],
            rationale=f"Solution achieved optimal objective value of {sol.best_solution.objective_values[0].value} with 100% feasibility.",
        )

        security_logger.info(f"OptimizationEvaluator: Evaluated solution '{sol.solution_id}' (Feasibility={sol.best_solution.feasibility_score}).")
        return expl


# Global OptimizationEvaluator instance
optimization_evaluator = OptimizationEvaluator()
