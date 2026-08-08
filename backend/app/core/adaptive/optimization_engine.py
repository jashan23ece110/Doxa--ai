"""
Optimization Engine for Enterprise Self-Learning & Adaptive Intelligence Engine.

Dynamically tunes Dense/BM25 weights, RRF parameters, reranker depth, HyDE, and multi-query counts based on learning stats.
"""

from typing import Dict, Any
from app.core.adaptive.learning_engine import learning_engine
from app.core.adaptive.policy_manager import policy_manager


class OptimizationEngine:
    """Dynamically calculates optimized retrieval and execution parameters."""

    @staticmethod
    def get_optimized_retrieval_params() -> Dict[str, Any]:
        """Calculates optimized retrieval weights and parameters."""
        policy = policy_manager.get_active_policy()
        stats = learning_engine.stats

        # Blend learned weights with active policy baseline
        dense_w = round((policy.dense_weight + stats.get("learned_dense_weight", 0.50)) / 2.0, 2)
        bm25_w = round((policy.bm25_weight + stats.get("learned_bm25_weight", 0.50)) / 2.0, 2)

        return {
            "dense_weight": dense_w,
            "bm25_weight": bm25_w,
            "rrf_k": 60,
            "enable_reranker": policy.enable_reranker,
            "rerank_top_k": policy.rerank_top_k,
            "enable_hyde": policy.enable_hyde,
        }


# Global OptimizationEngine instance
optimization_engine = OptimizationEngine()
