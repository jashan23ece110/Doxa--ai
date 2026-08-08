"""
Intelligent Memory Classifier & Deduplicator.

Classifies incoming candidate memories to decide whether to Store, Ignore, Update, Merge, Delete, or Pin.
"""

from typing import List, Tuple, Optional
from app.core.memory.memory_store import memory_store
from app.core.memory.memory_types import MemoryItem


class MemoryClassifier:
    """Classifies memories and handles duplicate merging."""

    @staticmethod
    def _compute_lexical_similarity(str1: str, str2: str) -> float:
        """Computes Jaccard word overlap similarity."""
        set1 = set(str1.lower().split())
        set2 = set(str2.lower().split())
        if not set1 or not set2:
            return 0.0
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        return len(intersection) / len(union)

    @classmethod
    def classify_and_process(cls, candidate: MemoryItem) -> Tuple[str, Optional[MemoryItem]]:
        """
        Determines action: 'store', 'ignore', 'merge', or 'update'.
        If duplicate exists, merges content into existing record.
        """
        existing_memories = memory_store.list_memories(user_id=candidate.user_id)

        for existing in existing_memories:
            sim = cls._compute_lexical_similarity(candidate.content, existing.content)
            if sim > 0.60 or candidate.title.lower() == existing.title.lower():
                # Merge duplicate
                merged_content = f"{existing.content} | {candidate.content}"
                updated_item = memory_store.update_memory(
                    existing.id,
                    {
                        "content": merged_content,
                        "importance_score": max(existing.importance_score, candidate.importance_score),
                        "access_count": existing.access_count + 1,
                    },
                )
                return "merge", updated_item

        # Store new unique memory
        saved_item = memory_store.add_memory(candidate)
        return "store", saved_item


# Global MemoryClassifier instance
memory_classifier = MemoryClassifier()
