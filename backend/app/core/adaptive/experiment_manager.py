"""
Experiment Manager for Enterprise Self-Learning & Adaptive Intelligence Engine.

Manages runtime A/B variant experiments comparing retrieval strategies, rerankers, prompts, and routing policies.
"""

import random
import time
from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel, Field
from app.core.adaptive.adaptive_metrics import adaptive_metrics_tracker


class ABExperiment(BaseModel):
    """Definition of an A/B experiment variant configuration."""

    experiment_id: str
    name: str
    variant_a: Dict[str, Any]
    variant_b: Dict[str, Any]
    active: bool = True
    variant_a_count: int = 0
    variant_b_count: int = 0


class ExperimentManager:
    """Manages runtime A/B experiments across retrieval and routing parameters."""

    def __init__(self):
        self._experiments: Dict[str, ABExperiment] = {}
        self._create_default_experiments()

    def _create_default_experiments(self) -> None:
        """Registers default A/B testing experiments."""
        exp = ABExperiment(
            experiment_id="exp_reranker_depth",
            name="Reranker Top-K Depth Comparison",
            variant_a={"rerank_top_k": 3},
            variant_b={"rerank_top_k": 5},
        )
        self._experiments[exp.experiment_id] = exp

    def select_variant(self, experiment_id: str = "exp_reranker_depth") -> Tuple[str, Dict[str, Any]]:
        """
        Selects variant A or variant B pseudo-randomly for an experiment.
        Returns: (variant_name, variant_config)
        """
        exp = self._experiments.get(experiment_id)
        if not exp or not exp.active:
            return "variant_a", {"rerank_top_k": 3}

        adaptive_metrics_tracker.record_experiment()
        if random.random() < 0.5:
            exp.variant_a_count += 1
            return "variant_a", exp.variant_a
        else:
            exp.variant_b_count += 1
            return "variant_b", exp.variant_b

    def list_experiments(self) -> List[ABExperiment]:
        """Lists active A/B experiments."""
        return list(self._experiments.values())


# Global ExperimentManager instance
experiment_manager = ExperimentManager()
