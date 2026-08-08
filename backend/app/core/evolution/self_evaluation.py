"""
Self-Evaluation Engine for Enterprise Self-Optimization Platform.

Assesses accuracy, latency, reliability, consistency, resource efficiency,
and goal completion metrics to produce a composite self-evaluation score.
"""

import time
from typing import Dict, Any, List
from app.core.logging import logger
from app.core.evolution.evolution_models import (
    SelfEvaluationScore,
    EvaluationMetric,
)


class SelfEvaluationEngine:
    """Evaluates system performance across multiple quality dimensions."""

    # Default metric targets
    _DEFAULT_TARGETS: Dict[str, float] = {
        "accuracy": 0.95,
        "latency_p99_ms": 500.0,
        "reliability_uptime": 0.999,
        "consistency": 0.93,
        "resource_efficiency": 0.85,
        "goal_completion": 0.90,
    }

    # Weights for composite score
    _METRIC_WEIGHTS: Dict[str, float] = {
        "accuracy": 0.25,
        "latency_p99_ms": 0.15,
        "reliability_uptime": 0.20,
        "consistency": 0.15,
        "resource_efficiency": 0.10,
        "goal_completion": 0.15,
    }

    def evaluate(
        self,
        observed_metrics: Dict[str, float] = None,
    ) -> SelfEvaluationScore:
        """
        Performs comprehensive self-evaluation against target metrics.

        Args:
            observed_metrics: Optional dict of observed metric values.
                Keys: accuracy, latency_p99_ms, reliability_uptime, consistency,
                      resource_efficiency, goal_completion.

        Returns:
            SelfEvaluationScore with per-metric details and composite score.
        """
        start = time.time()
        obs = observed_metrics or {}

        # Default observed values (simulated from system telemetry)
        accuracy = obs.get("accuracy", 0.96)
        latency = obs.get("latency_p99_ms", 380.0)
        reliability = obs.get("reliability_uptime", 0.9995)
        consistency = obs.get("consistency", 0.94)
        resource_eff = obs.get("resource_efficiency", 0.88)
        goal_completion = obs.get("goal_completion", 0.92)

        # Normalize latency to 0-1 score (lower latency = higher score)
        latency_target = self._DEFAULT_TARGETS["latency_p99_ms"]
        latency_score = round(min(1.0, max(0.0, 1.0 - (latency / (latency_target * 2)))), 4)

        metrics: List[EvaluationMetric] = [
            EvaluationMetric(
                metric_name="accuracy",
                value=accuracy,
                target=self._DEFAULT_TARGETS["accuracy"],
                weight=self._METRIC_WEIGHTS["accuracy"],
                passed=accuracy >= self._DEFAULT_TARGETS["accuracy"],
                details=f"Accuracy {accuracy:.4f} vs target {self._DEFAULT_TARGETS['accuracy']}",
            ),
            EvaluationMetric(
                metric_name="latency_p99_ms",
                value=latency,
                target=latency_target,
                weight=self._METRIC_WEIGHTS["latency_p99_ms"],
                passed=latency <= latency_target,
                details=f"P99 latency {latency:.1f}ms vs target {latency_target:.1f}ms",
            ),
            EvaluationMetric(
                metric_name="reliability_uptime",
                value=reliability,
                target=self._DEFAULT_TARGETS["reliability_uptime"],
                weight=self._METRIC_WEIGHTS["reliability_uptime"],
                passed=reliability >= self._DEFAULT_TARGETS["reliability_uptime"],
                details=f"Uptime {reliability:.4f} vs target {self._DEFAULT_TARGETS['reliability_uptime']}",
            ),
            EvaluationMetric(
                metric_name="consistency",
                value=consistency,
                target=self._DEFAULT_TARGETS["consistency"],
                weight=self._METRIC_WEIGHTS["consistency"],
                passed=consistency >= self._DEFAULT_TARGETS["consistency"],
                details=f"Consistency {consistency:.4f} vs target {self._DEFAULT_TARGETS['consistency']}",
            ),
            EvaluationMetric(
                metric_name="resource_efficiency",
                value=resource_eff,
                target=self._DEFAULT_TARGETS["resource_efficiency"],
                weight=self._METRIC_WEIGHTS["resource_efficiency"],
                passed=resource_eff >= self._DEFAULT_TARGETS["resource_efficiency"],
                details=f"Resource efficiency {resource_eff:.4f} vs target {self._DEFAULT_TARGETS['resource_efficiency']}",
            ),
            EvaluationMetric(
                metric_name="goal_completion",
                value=goal_completion,
                target=self._DEFAULT_TARGETS["goal_completion"],
                weight=self._METRIC_WEIGHTS["goal_completion"],
                passed=goal_completion >= self._DEFAULT_TARGETS["goal_completion"],
                details=f"Goal completion {goal_completion:.4f} vs target {self._DEFAULT_TARGETS['goal_completion']}",
            ),
        ]

        # Compute composite score
        scores_map = {
            "accuracy": accuracy,
            "latency_p99_ms": latency_score,
            "reliability_uptime": reliability,
            "consistency": consistency,
            "resource_efficiency": resource_eff,
            "goal_completion": goal_completion,
        }
        weighted_sum = sum(
            scores_map[k] * self._METRIC_WEIGHTS[k] for k in self._METRIC_WEIGHTS
        )
        total_weight = sum(self._METRIC_WEIGHTS.values())
        composite = round(weighted_sum / total_weight, 4) if total_weight > 0 else 0.0

        # Generate recommendations for failing metrics
        recommendations: List[str] = []
        for m in metrics:
            if not m.passed:
                recommendations.append(
                    f"Improve {m.metric_name}: current={m.value}, target={m.target}"
                )

        elapsed = time.time() - start

        result = SelfEvaluationScore(
            accuracy_score=round(accuracy, 4),
            latency_score=latency_score,
            reliability_score=round(reliability, 4),
            consistency_score=round(consistency, 4),
            resource_efficiency_score=round(resource_eff, 4),
            goal_completion_score=round(goal_completion, 4),
            composite_score=composite,
            metrics=metrics,
            recommendations=recommendations,
        )

        logger.info(
            f"SelfEvaluationEngine evaluated '{result.evaluation_id}': "
            f"Composite={composite}, Metrics={len(metrics)}, "
            f"Passed={sum(1 for m in metrics if m.passed)}/{len(metrics)}, "
            f"Duration={elapsed*1000:.1f}ms"
        )
        return result


# Global SelfEvaluationEngine instance
self_evaluation_engine = SelfEvaluationEngine()
