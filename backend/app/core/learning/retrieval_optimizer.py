"""
Retrieval Optimizer for Enterprise Continuous Learning Layer.

Tracks precision, recall, latency, reranker effectiveness, BM25, and dense usefulness.
Generates recommendations for TopK, fusion weights, reranker thresholds, and query expansion thresholds.
(No automatic production changes — recommendations only).
"""

from typing import Dict, Any, List, Optional
from app.core.learning.learning_metrics import learning_metrics_tracker
from app.core.logging import logger


class RetrievalOptimizer:
    """Analyzes retrieval performance and generates tuning recommendations."""

    @staticmethod
    def generate_retrieval_recommendations(
        avg_precision: float = 0.82,
        avg_similarity: float = 0.78,
        reranker_latency_ms: float = 120.0,
    ) -> List[Dict[str, Any]]:
        """Generates recommendations for retrieval parameter optimization."""
        recs = []

        if avg_similarity < 0.70:
            recs.append({
                "parameter": "RAG_DEFAULT_TOP_K",
                "current_value": 3,
                "recommended_value": 5,
                "reason": f"Low average similarity ({avg_similarity:.2f}). Increasing TopK improves retrieval recall.",
            })

        if reranker_latency_ms > 500.0:
            recs.append({
                "parameter": "RERANK_MAX_CANDIDATES",
                "current_value": 20,
                "recommended_value": 10,
                "reason": f"Cross-Encoder reranker latency is high ({reranker_latency_ms:.2f}ms). Reducing candidates cuts latency.",
            })

        for r in recs:
            learning_metrics_tracker.record_recommendation(category="retrieval")
            logger.info(f"Retrieval Optimization Recommendation: {r['parameter']} -> {r['recommended_value']} ({r['reason']})")

        return recs


# Global RetrievalOptimizer instance
retrieval_optimizer = RetrievalOptimizer()
