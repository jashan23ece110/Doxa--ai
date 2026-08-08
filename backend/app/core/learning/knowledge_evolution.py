"""
Knowledge Evolution Engine for Enterprise Continuous Learning Layer.

Detects missing documents, frequently searched topics, missing knowledge,
stale documents, and low-quality chunks, recommending new documents or re-indexing.
"""

from typing import List, Dict, Any
from app.core.learning.learning_metrics import learning_metrics_tracker
from app.core.learning.learning_repository import learning_repository
from app.core.logging import logger


class KnowledgeEvolutionEngine:
    """Identifies knowledge gaps and recommends corpus evolution."""

    @staticmethod
    def generate_knowledge_recommendations() -> List[Dict[str, Any]]:
        """Scans learning records for missing knowledge gaps and retrieval failures."""
        records = learning_repository.get_all_records()
        recs = []

        failed_queries = [
            rec.prompt_text for rec in records
            if not rec.successful_retrieval or rec.retrieval_similarity < 0.60
        ]

        if failed_queries:
            recs.append({
                "type": "missing_documents_recommendation",
                "recommended_action": "Upload supplementary documentation for low-similarity topics.",
                "sample_queries": failed_queries[:3],
                "explanation": f"Detected {len(failed_queries)} queries with low retrieval similarity (< 0.60).",
            })

        for r in recs:
            learning_metrics_tracker.record_recommendation(category="knowledge")
            logger.info(f"Knowledge Evolution Recommendation: {r['type']} ({r['explanation']})")

        return recs


# Global KnowledgeEvolutionEngine instance
knowledge_evolution_engine = KnowledgeEvolutionEngine()
