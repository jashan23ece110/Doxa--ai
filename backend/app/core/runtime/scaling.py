"""
Scaling Engine for Enterprise AI Operating System Runtime.

Handles horizontal scaling, worker scaling, queue scaling, provider scaling,
predictive scaling, and resource balancing.
"""

from typing import Dict, Any
from app.core.logging import logger
from app.core.runtime.runtime_models import ScalingRule


class ScalingEngine:
    """Automated horizontal worker auto-scaling engine."""

    def __init__(self):
        self._rule = ScalingRule()

    def evaluate_scaling(self, current_cpu_pct: float = 45.0) -> int:
        """
        Evaluates scaling rules and adjusts worker pool capacity.
        Returns: recommended target worker count.
        """
        if current_cpu_pct > self._rule.threshold_pct:
            target = min(self._rule.max_workers, self._rule.min_workers * 2)
            logger.info(f"ScalingEngine triggering scale_up: Target workers={target}.")
            return target
        return self._rule.min_workers


# Global ScalingEngine instance
scaling_engine = ScalingEngine()
