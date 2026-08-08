"""
Strategy Manager for Enterprise Self-Learning & Adaptive Intelligence Engine.

Maintains execution strategies (Fast, Balanced, Deep, Research, Coding, Creative, Analytical)
and automatically selects the optimal strategy based on prompt intent and active policy.
"""

from typing import Dict, Any, List, Tuple
from app.core.adaptive.policy_manager import policy_manager


class StrategyManager:
    """Selects execution strategy based on query intent and active policy."""

    @staticmethod
    def select_strategy(prompt: str) -> Tuple[str, Dict[str, Any]]:
        """
        Selects optimal strategy name and configuration parameters for a prompt.
        Returns: (strategy_name, strategy_config)
        """
        policy = policy_manager.get_active_policy()

        # Respect explicit policy override if low_latency or low_cost
        if policy.name in ("low_latency", "low_cost"):
            return "fast", {
                "max_reasoning_depth": "fast",
                "dense_weight": policy.dense_weight,
                "bm25_weight": policy.bm25_weight,
                "enable_reranker": policy.enable_reranker,
            }

        clean = prompt.lower().strip()

        # Coding Strategy
        if any(kw in clean for kw in ["code", "python", "bug", "refactor", "api", "schema"]):
            return "coding", {
                "max_reasoning_depth": "deep",
                "dense_weight": 0.60,
                "bm25_weight": 0.40,
                "enable_reranker": True,
            }

        # Research Strategy
        if any(kw in clean for kw in ["research", "compare", "analyze", "benchmark", "tradeoffs"]):
            return "research", {
                "max_reasoning_depth": "research",
                "dense_weight": 0.55,
                "bm25_weight": 0.45,
                "enable_reranker": True,
            }

        # Default Balanced Strategy
        return "balanced", {
            "max_reasoning_depth": policy.max_reasoning_depth,
            "dense_weight": policy.dense_weight,
            "bm25_weight": policy.bm25_weight,
            "enable_reranker": policy.enable_reranker,
        }


# Global StrategyManager instance
strategy_manager = StrategyManager()
