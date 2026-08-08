"""
Optimization Scenario Engine.

Evaluates mathematical optimization solutions under resource shortages and demand spikes.
"""

from typing import Dict, Any, List
from app.core.logging import security_logger
from app.core.decision_intelligence.optimization.optimization_types import OptimizationScenario


class OptimizationScenarioEngine:
    """Optimization Scenario Engine."""

    def evaluate_optimization_scenarios(self, base_objective_val: float) -> List[OptimizationScenario]:
        """
        Evaluates optimization outcome under baseline, resource shortage, and demand spike scenarios.

        Args:
            base_objective_val: Baseline objective value float.

        Returns:
            List of OptimizationScenario objects.
        """
        scenarios = [
            OptimizationScenario(name="BASELINE", delta_capacity_pct=0.0, projected_objective_value=base_objective_val),
            OptimizationScenario(name="RESOURCE_SHORTAGE", delta_capacity_pct=-0.20, projected_objective_value=round(base_objective_val * 0.85, 2)),
            OptimizationScenario(name="DEMAND_SPIKE", delta_capacity_pct=0.30, projected_objective_value=round(base_objective_val * 1.15, 2)),
        ]

        security_logger.info(f"OptimizationScenarioEngine: Evaluated {len(scenarios)} scenarios from base objective value {base_objective_val}.")
        return scenarios


# Global OptimizationScenarioEngine instance
optimization_scenario_engine = OptimizationScenarioEngine()
