"""
Improvement Recommendation Engine for Enterprise Self-Optimization Platform.

Generates actionable improvement recommendations across architecture, performance,
security, reliability, cost, and developer productivity dimensions.
"""

import time
import threading
from typing import Dict, Any, List
from app.core.logging import logger
from app.core.evolution.evolution_models import (
    SystemRecommendation,
    RecommendationCategory,
)


class ImprovementRecommendationEngine:
    """Generates prioritized system-wide improvement recommendations."""

    def __init__(self):
        self._lock = threading.Lock()
        self._generated_recommendations: List[SystemRecommendation] = []

    # Pre-built recommendation catalog
    _RECOMMENDATION_CATALOG: List[Dict[str, Any]] = [
        {
            "category": RecommendationCategory.ARCHITECTURE,
            "title": "Implement Event-Driven Decoupling for Workflow Steps",
            "description": "Replace synchronous workflow step chaining with async event bus to improve fault isolation and horizontal scalability.",
            "impact_score": 0.85,
            "effort_score": 0.60,
        },
        {
            "category": RecommendationCategory.PERFORMANCE,
            "title": "Enable Speculative Prefetching for Knowledge Graph Traversals",
            "description": "Pre-fetch likely next-hop nodes during graph traversal based on historical access patterns to reduce traversal latency by ~35%.",
            "impact_score": 0.78,
            "effort_score": 0.45,
        },
        {
            "category": RecommendationCategory.SECURITY,
            "title": "Rotate Encryption Keys on 90-Day Cadence",
            "description": "Implement automated key rotation for all data-at-rest encryption keys with zero-downtime re-encryption pipeline.",
            "impact_score": 0.90,
            "effort_score": 0.55,
        },
        {
            "category": RecommendationCategory.RELIABILITY,
            "title": "Add Multi-Region Failover for Critical Data Stores",
            "description": "Deploy cross-region replication with automatic failover for evolution store, decision memory, and knowledge graph persistence layers.",
            "impact_score": 0.92,
            "effort_score": 0.75,
        },
        {
            "category": RecommendationCategory.COST,
            "title": "Implement Tiered Storage for Historical Evolution Data",
            "description": "Move evolution snapshots older than 30 days to compressed cold storage, reducing storage costs by ~60%.",
            "impact_score": 0.65,
            "effort_score": 0.30,
        },
        {
            "category": RecommendationCategory.DEVELOPER_PRODUCTIVITY,
            "title": "Auto-Generate OpenAPI Specs from Evolution Orchestrator",
            "description": "Automatically generate and publish OpenAPI documentation for all evolution platform endpoints to accelerate integration development.",
            "impact_score": 0.60,
            "effort_score": 0.25,
        },
        {
            "category": RecommendationCategory.PERFORMANCE,
            "title": "Implement Connection Pooling for External API Integrations",
            "description": "Replace per-request HTTP connections with persistent connection pools (pool_size=20, keepalive=30s) for tool and integration endpoints.",
            "impact_score": 0.72,
            "effort_score": 0.35,
        },
        {
            "category": RecommendationCategory.ARCHITECTURE,
            "title": "Introduce CQRS Pattern for Evolution Analytics",
            "description": "Separate read and write paths for evolution analytics to allow independent scaling of query and ingestion workloads.",
            "impact_score": 0.70,
            "effort_score": 0.65,
        },
    ]

    def generate_recommendations(
        self,
        focus_categories: List[RecommendationCategory] = None,
        max_recommendations: int = 10,
    ) -> List[SystemRecommendation]:
        """
        Generates prioritized improvement recommendations.

        Args:
            focus_categories: Optional list of categories to focus on. None = all.
            max_recommendations: Maximum number of recommendations to return.

        Returns:
            List of SystemRecommendation sorted by priority rank.
        """
        start = time.time()

        catalog = self._RECOMMENDATION_CATALOG
        if focus_categories:
            catalog = [r for r in catalog if r["category"] in focus_categories]

        # Sort by impact/effort ratio (higher = better ROI)
        sorted_catalog = sorted(
            catalog,
            key=lambda x: x["impact_score"] / max(x["effort_score"], 0.01),
            reverse=True,
        )

        recommendations: List[SystemRecommendation] = []
        for rank, entry in enumerate(sorted_catalog[:max_recommendations], start=1):
            rec = SystemRecommendation(
                category=entry["category"],
                title=entry["title"],
                description=entry["description"],
                impact_score=entry["impact_score"],
                effort_score=entry["effort_score"],
                priority_rank=rank,
            )
            recommendations.append(rec)

        with self._lock:
            self._generated_recommendations.extend(recommendations)

        elapsed = (time.time() - start) * 1000
        logger.info(
            f"ImprovementRecommendationEngine generated {len(recommendations)} recommendations "
            f"from catalog of {len(catalog)} entries, Duration={elapsed:.1f}ms"
        )
        return recommendations

    def get_all_recommendations(self) -> List[SystemRecommendation]:
        """Returns all generated recommendations."""
        with self._lock:
            return list(self._generated_recommendations)

    def mark_recommendation_status(
        self, recommendation_id: str, status: str
    ) -> bool:
        """Updates the status of a recommendation."""
        with self._lock:
            for rec in self._generated_recommendations:
                if rec.recommendation_id == recommendation_id:
                    rec.status = status
                    logger.info(
                        f"Recommendation '{recommendation_id}' status updated to '{status}'."
                    )
                    return True
        return False


# Global ImprovementRecommendationEngine instance
improvement_recommendation_engine = ImprovementRecommendationEngine()
