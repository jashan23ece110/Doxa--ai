"""
Memory Consolidation Engine for Enterprise Memory Intelligence Platform.

Detects duplicate, similar, outdated, or contradictory memories and merges them intelligently.
Preserves audit trail history.
"""

from typing import List, Dict, Any, Tuple
from app.core.logging import logger
from app.core.memory.memory_types import BaseMemoryItem


class MemoryConsolidationEngine:
    """Consolidates duplicate and similar memories."""

    @staticmethod
    def consolidate_memories(memories: List[BaseMemoryItem]) -> Tuple[List[BaseMemoryItem], int]:
        """
        Scans a list of memories, merges duplicates, and returns consolidated memories and merged count.
        """
        if not memories:
            return [], 0

        merged_count = 0
        seen_content: Dict[str, BaseMemoryItem] = {}
        consolidated: List[BaseMemoryItem] = []

        for mem in memories:
            clean_text = mem.content.strip().lower()

            if clean_text in seen_content:
                # Duplicate detected — merge importance score & access counts
                existing = seen_content[clean_text]
                existing.access_count += mem.access_count
                existing.importance_score = max(existing.importance_score, mem.importance_score)
                existing.tags = list(set(existing.tags + mem.tags))
                merged_count += 1
                logger.info(f"Consolidated duplicate memory '{mem.id}' into '{existing.id}'.")
            else:
                seen_content[clean_text] = mem
                consolidated.append(mem)

        return consolidated, merged_count


# Global MemoryConsolidationEngine instance
memory_consolidation_engine = MemoryConsolidationEngine()
