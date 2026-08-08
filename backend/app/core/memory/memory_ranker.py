"""
5-Factor Memory Ranker Engine.

Ranks candidate memories using:
45% Semantic Similarity, 20% Importance, 15% Recency, 10% Access Frequency, 10% Confidence.
Pinned memories receive maximum priority score (1.0).
"""

import time
from typing import List, Dict, Any, Tuple
from app.core.memory.memory_types import MemoryItem


class MemoryRanker:
    """Calculates 5-factor relevance score for memory items."""

    @staticmethod
    def _compute_recency_score(last_accessed: float) -> float:
        """Calculates recency score (decaying over days)."""
        elapsed_hours = (time.time() - last_accessed) / 3600.0
        return max(0.0, 1.0 - (elapsed_hours / 168.0))  # 7 days scale

    @staticmethod
    def _compute_access_freq_score(access_count: int) -> float:
        """Calculates normalized access frequency score."""
        return min(access_count / 10.0, 1.0)

    @classmethod
    def calculate_memory_score(
        cls,
        item: MemoryItem,
        similarity_score: float = 0.5,
    ) -> float:
        """Calculates unified 5-factor memory score (0.0 to 1.0)."""
        if item.pinned:
            return 1.0

        recency = cls._compute_recency_score(item.last_accessed)
        access_freq = cls._compute_access_freq_score(item.access_count)

        score = (
            (similarity_score * 0.45)
            + (item.importance_score * 0.20)
            + (recency * 0.15)
            + (access_freq * 0.10)
            + (item.confidence * 0.10)
        )

        return round(min(max(score, 0.0), 1.0), 4)

    @classmethod
    def rank_memories(
        cls,
        memories: List[MemoryItem],
        query: str = "",
        top_k: int = 5,
    ) -> List[Tuple[MemoryItem, float]]:
        """Ranks list of memories and returns Top-K scored pairs."""
        scored_pairs = []
        for item in memories:
            sim = 0.5
            if query and query.lower() in item.content.lower():
                sim = 0.95
            score = cls.calculate_memory_score(item, similarity_score=sim)
            scored_pairs.append((item, score))

        scored_pairs.sort(key=lambda x: x[1], reverse=True)
        return scored_pairs[:top_k]


# Global MemoryRanker instance
memory_ranker = MemoryRanker()
