"""
Experiment Manager for Enterprise Self-Optimization Platform.

Manages A/B experiments, feature flag trials, safe rollouts,
and automatic rollbacks when experiments degrade performance.
"""

import time
import threading
from typing import Dict, Any, List, Optional
from app.core.logging import logger
from app.core.evolution.evolution_models import (
    ABExperiment,
    ExperimentVariant,
)


class ExperimentManager:
    """Manages A/B experiments with safe rollout and automatic rollback."""

    def __init__(self):
        self._lock = threading.Lock()
        self._experiments: Dict[str, ABExperiment] = {}

    def create_experiment(
        self,
        name: str,
        hypothesis: str,
        control_config: Dict[str, Any] = None,
        treatment_config: Dict[str, Any] = None,
        auto_rollback: bool = True,
        rollback_threshold: float = 0.1,
    ) -> ABExperiment:
        """
        Creates a new A/B experiment with control and treatment variants.

        Args:
            name: Experiment name.
            hypothesis: Hypothesis being tested.
            control_config: Configuration overrides for control variant.
            treatment_config: Configuration overrides for treatment variant.
            auto_rollback: Whether to enable automatic rollback on degradation.
            rollback_threshold: Minimum degradation percentage to trigger rollback.

        Returns:
            ABExperiment with two variants (control + treatment).
        """
        control = ExperimentVariant(
            name="control",
            config_overrides=control_config or {},
        )
        treatment = ExperimentVariant(
            name="treatment",
            config_overrides=treatment_config or {"optimized": True},
        )

        experiment = ABExperiment(
            name=name,
            hypothesis=hypothesis,
            variants=[control, treatment],
            auto_rollback_enabled=auto_rollback,
            rollback_threshold=rollback_threshold,
        )

        with self._lock:
            self._experiments[experiment.experiment_id] = experiment

        logger.info(
            f"ExperimentManager created experiment '{experiment.experiment_id}': "
            f"Name='{name}', Variants={len(experiment.variants)}, "
            f"AutoRollback={auto_rollback}"
        )
        return experiment

    def start_experiment(self, experiment_id: str) -> Optional[ABExperiment]:
        """Starts an experiment, transitioning from DRAFT to RUNNING."""
        with self._lock:
            exp = self._experiments.get(experiment_id)
            if exp and exp.status == "DRAFT":
                exp.status = "RUNNING"
                exp.started_at = time.time()
                logger.info(f"Experiment '{experiment_id}' started.")
                return exp
            logger.warning(f"Cannot start experiment '{experiment_id}': not found or not in DRAFT.")
            return None

    def record_variant_result(
        self,
        experiment_id: str,
        variant_name: str,
        success: bool,
        latency_ms: float = 0.0,
    ) -> bool:
        """
        Records a result for a specific variant in a running experiment.

        Args:
            experiment_id: The experiment to record against.
            variant_name: "control" or "treatment".
            success: Whether this trial was successful.
            latency_ms: Observed latency in milliseconds.

        Returns:
            True if recorded successfully.
        """
        with self._lock:
            exp = self._experiments.get(experiment_id)
            if not exp or exp.status != "RUNNING":
                return False

            for variant in exp.variants:
                if variant.name == variant_name:
                    variant.sample_size += 1
                    # Running average for success rate
                    n = variant.sample_size
                    variant.success_rate = round(
                        ((variant.success_rate * (n - 1)) + (1.0 if success else 0.0)) / n, 4
                    )
                    # Running average for latency
                    variant.avg_latency_ms = round(
                        ((variant.avg_latency_ms * (n - 1)) + latency_ms) / n, 2
                    )
                    return True
        return False

    def evaluate_experiment(self, experiment_id: str) -> Optional[ABExperiment]:
        """
        Evaluates experiment results, determines winner, and auto-rolls-back if degraded.

        Returns:
            Updated ABExperiment with status COMPLETED or ROLLED_BACK.
        """
        with self._lock:
            exp = self._experiments.get(experiment_id)
            if not exp or exp.status != "RUNNING":
                return None

            control = next((v for v in exp.variants if v.name == "control"), None)
            treatment = next((v for v in exp.variants if v.name == "treatment"), None)

            if not control or not treatment:
                return None

            # Check for degradation
            if control.success_rate > 0 and treatment.sample_size > 0:
                degradation = control.success_rate - treatment.success_rate
                if degradation > exp.rollback_threshold and exp.auto_rollback_enabled:
                    exp.status = "ROLLED_BACK"
                    exp.completed_at = time.time()
                    logger.warning(
                        f"Experiment '{experiment_id}' ROLLED BACK: "
                        f"Degradation={degradation:.4f} exceeds threshold={exp.rollback_threshold}"
                    )
                    return exp

            # Determine winner
            if treatment.success_rate >= control.success_rate:
                exp.winner_variant_id = treatment.variant_id
            else:
                exp.winner_variant_id = control.variant_id

            exp.status = "COMPLETED"
            exp.completed_at = time.time()
            logger.info(
                f"Experiment '{experiment_id}' COMPLETED: "
                f"Winner='{exp.winner_variant_id}', "
                f"Control SR={control.success_rate:.4f}, Treatment SR={treatment.success_rate:.4f}"
            )
            return exp

    def list_experiments(self, status: str = None) -> List[ABExperiment]:
        """Lists experiments, optionally filtered by status."""
        with self._lock:
            exps = list(self._experiments.values())
            if status:
                exps = [e for e in exps if e.status == status]
            return exps

    def get_experiment(self, experiment_id: str) -> Optional[ABExperiment]:
        """Gets a specific experiment by ID."""
        with self._lock:
            return self._experiments.get(experiment_id)


# Global ExperimentManager instance
experiment_manager = ExperimentManager()
