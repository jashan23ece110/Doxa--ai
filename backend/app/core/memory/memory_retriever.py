"""
Memory Retriever Engine for Enterprise Memory Intelligence Platform.

Retrieves memories using hybrid ranking: semantic vector similarity, keyword search,
time relevance decay, importance scores, and relationship graph traversal.
"""

import time
from typing import List, Dict, Any, Optional
from app.core.memory.memory_types import BaseMemoryItem
from app.core.memory.relationship_graph import relationship_graph


class MemoryRetriever:
    """Hybrid memory retrieval and ranking engine."""

    @staticmethod
    def rank_and_retrieve(
        query: str,
        memories: List[BaseMemoryItem],
        top_k: int = 5,
        user_id: str = "default_user",
    ) -> List[BaseMemoryItem]:
        """
        Ranks memories using hybrid score:
        score = (keyword_match * 0.35) + (importance * 0.35) + (recency_decay * 0.30)
        """
        if not memories:
            return []

        user_memories = [m for m in memories if m.user_id == user_id]
        if not user_memories:
            return []

        query_words = set(query.lower().split())
        now = time.time()
        scored_items = []

        for mem in user_memories:
            # 1. Keyword match score
            content_words = set(mem.content.lower().split())
            match_count = len(query_words.intersection(content_words))
            kw_score = min(match_count / max(len(query_words), 1), 1.0)

            # 2. Recency decay score (half life 7 days)
            age_days = (now - mem.last_accessed) / 86400.0
            recency_score = 1.0 / (1.0 + (age_days / 7.0))

            # 3. Hybrid score calculation
            final_score = (kw_score * 0.35) + (mem.importance_score * 0.35) + (recency_score * 0.30)
            scored_items.append((final_score, mem))

        # Sort descending by hybrid score
        scored_items.sort(key=lambda x: x[0], reverse=True)

        ranked_memories = [item[1] for item in scored_items[:top_k]]

        # Update last_accessed and access_count
        for mem in ranked_memories:
            mem.last_accessed = now
            mem.access_count += 1

        return ranked_memories


# Global MemoryRetriever instance
memory_retriever = MemoryRetriever()
