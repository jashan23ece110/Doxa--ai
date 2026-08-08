"""
Evolution Analytics Tracker for Enterprise Self-Optimization Platform.

Tracks improvement rate, optimization success, capability growth,
and regression avoidance across the evolution lifecycle.
"""

import threading
from typing import Dict, Any, List
from app.core.logging import logger
from app.core.evolution.evolution_models import EvolutionAnalyticsSummary


class EvolutionAnalyticsTracker:
    """Tracks and reports evolution platform metrics."""

    def __init__(self):
        self._lock = threading.Lock()
        self._optimization_attempts: int = 0
        self._optimization_successes: int = 0
        self._experiments_completed: int = 0
        self._experiments_successful: int = 0
        self._total_recommendations: int = 0
        self._recommendations_implemented: int = 0
        self._tuning_cycles: int = 0
        self._insights_discovered: int = 0
        self._capability_scores_history: List[float] = []
        self._regressions_detected: int = 0
        self._regressions_avoided: int = 0

    def record_optimization(self, success: bool) -> None:
        """Records an optimization attempt and its outcome."""
        with self._lock:
            self._optimization_attempts += 1
            if success:
                self._optimization_successes += 1

    def record_experiment(self, successful: bool) -> None:
        """Records an experiment completion."""
        with self._lock:
            self._experiments_completed += 1
            if successful:
                self._experiments_successful += 1

    def record_recommendation(self, implemented: bool = False) -> None:
        """Records a recommendation generation."""
        with self._lock:
            self._total_recommendations += 1
            if implemented:
                self._recommendations_implemented += 1

    def record_tuning_cycle(self) -> None:
        """Records a tuning cycle completion."""
        with self._lock:
            self._tuning_cycles += 1

    def record_insights(self, count: int) -> None:
        """Records discovered insights."""
        with self._lock:
            self._insights_discovered += count

    def record_capability_score(self, score: float) -> None:
        """Records a capability score for trend tracking."""
        with self._lock:
            self._capability_scores_history.append(score)

    def record_regression(self, avoided: bool) -> None:
        """Records a regression detection event."""
        with self._lock:
            self._regressions_detected += 1
            if avoided:
                self._regressions_avoided += 1

    def get_summary(self) -> EvolutionAnalyticsSummary:
        """Returns aggregated evolution analytics summary."""
        with self._lock:
            opt_success_rate = (
                round(self._optimization_successes / max(self._optimization_attempts, 1), 4)
            )

            # Compute capability growth rate from score history
            growth_rate = 0.0
            if len(self._capability_scores_history) >= 2:
                first = self._capability_scores_history[0]
                last = self._capability_scores_history[-1]
                if first > 0:
                    growth_rate = round((last - first) / first, 4)

            # Compute improvement rate
            improvement_rate = round(opt_success_rate * 100, 2)

            # Regression avoidance rate
            regression_avoidance = (
                round(self._regressions_avoided / max(self._regressions_detected, 1), 4)
            )

            summary = EvolutionAnalyticsSummary(
                improvement_rate_pct=improvement_rate,
                optimization_success_rate=opt_success_rate,
                capability_growth_rate=growth_rate,
                regression_avoidance_rate=regression_avoidance,
                experiments_completed=self._experiments_completed,
                experiments_successful=self._experiments_successful,
                total_recommendations=self._total_recommendations,
                recommendations_implemented=self._recommendations_implemented,
                total_tuning_cycles=self._tuning_cycles,
                insights_discovered=self._insights_discovered,
            )

            logger.info(
                f"EvolutionAnalytics: ImprovementRate={improvement_rate}%, "
                f"OptSuccess={opt_success_rate}, Growth={growth_rate}, "
                f"Experiments={self._experiments_completed}, "
                f"Tuning={self._tuning_cycles}"
            )
            return summary


# Global EvolutionAnalyticsTracker instance
evolution_analytics_tracker = EvolutionAnalyticsTracker()
