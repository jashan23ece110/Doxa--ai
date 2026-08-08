"""
Policy Manager for Enterprise Self-Learning & Adaptive Intelligence Engine.

Manages switchable runtime execution policies (low_latency, maximum_quality, low_cost, balanced_mode).
"""

import threading
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import logger


class AdaptivePolicy(BaseModel):
    """Configuration profile for a runtime execution policy."""

    name: str
    description: str
    max_reasoning_depth: str = "balanced"  # fast, balanced, deep, research
    dense_weight: float = 0.50
    bm25_weight: float = 0.50
    enable_reranker: bool = True
    rerank_top_k: int = 3
    enable_hyde: bool = False
    preferred_model_tier: str = "standard"  # fast, standard, premium


class PolicyManager:
    """Manages active runtime policy and switching."""

    PREDEFINED_POLICIES: Dict[str, AdaptivePolicy] = {
        "balanced_mode": AdaptivePolicy(
            name="balanced_mode",
            description="Balanced trade-off between latency, cost, and quality.",
            max_reasoning_depth="balanced",
            dense_weight=0.50,
            bm25_weight=0.50,
            enable_reranker=True,
            rerank_top_k=3,
            enable_hyde=False,
            preferred_model_tier="standard",
        ),
        "low_latency": AdaptivePolicy(
            name="low_latency",
            description="Optimizes for ultra-low latency response times.",
            max_reasoning_depth="fast",
            dense_weight=0.60,
            bm25_weight=0.40,
            enable_reranker=False,
            rerank_top_k=2,
            enable_hyde=False,
            preferred_model_tier="fast",
        ),
        "maximum_quality": AdaptivePolicy(
            name="maximum_quality",
            description="Optimizes for maximum retrieval recall and verification quality.",
            max_reasoning_depth="deep",
            dense_weight=0.55,
            bm25_weight=0.45,
            enable_reranker=True,
            rerank_top_k=5,
            enable_hyde=True,
            preferred_model_tier="premium",
        ),
        "low_cost": AdaptivePolicy(
            name="low_cost",
            description="Minimizes model token usage and computational cost.",
            max_reasoning_depth="fast",
            dense_weight=0.50,
            bm25_weight=0.50,
            enable_reranker=False,
            rerank_top_k=2,
            enable_hyde=False,
            preferred_model_tier="fast",
        ),
    }

    def __init__(self):
        self._lock = threading.Lock()
        self._active_policy_name: str = "balanced_mode"

    def get_active_policy(self) -> AdaptivePolicy:
        """Returns the currently active runtime policy."""
        with self._lock:
            return self.PREDEFINED_POLICIES.get(self._active_policy_name, self.PREDEFINED_POLICIES["balanced_mode"])

    def set_active_policy(self, policy_name: str) -> bool:
        """Switches the active runtime policy without restarting the server."""
        with self._lock:
            if policy_name in self.PREDEFINED_POLICIES:
                self._active_policy_name = policy_name
                logger.info(f"Switched active adaptive policy to '{policy_name}'.")
                return True
            logger.warning(f"Unknown policy name '{policy_name}'. Policy switch ignored.")
            return False

    def list_policies(self) -> List[AdaptivePolicy]:
        """Lists all predefined runtime policies."""
        return list(self.PREDEFINED_POLICIES.values())


# Global PolicyManager instance
policy_manager = PolicyManager()
