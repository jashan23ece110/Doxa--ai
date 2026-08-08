"""
Enterprise Memory Intelligence Manager Orchestrator.

Acts as the central memory orchestrator providing async methods to store, update, delete,
merge, retrieve, rank, expire, and consolidate memories across 9 memory categories.
Supports graph linking, context compression, analytics, and GDPR privacy compliance (forgetting/export).
"""

import threading
import time
from typing import Dict, Any, List, Optional, Tuple
from app.core.config import settings
from app.core.logging import logger
from app.core.memory.consolidation import memory_consolidation_engine
from app.core.memory.context_compression import context_compression_engine
from app.core.memory.importance_engine import importance_engine
from app.core.memory.memory_analytics import memory_analytics_tracker
from app.core.memory.memory_retriever import memory_retriever
from app.core.memory.memory_types import BaseMemoryItem, MemoryCategory
from app.core.memory.relationship_graph import relationship_graph


class EnterpriseMemoryManager:
    """Central orchestrator for Enterprise Memory Intelligence Platform."""

    def __init__(self):
        self._lock = threading.Lock()
        self._memories: Dict[str, BaseMemoryItem] = {}

    def store_memory(
        self,
        content: str,
        category: MemoryCategory = MemoryCategory.LONG_TERM,
        user_id: str = "default_user",
        tags: Optional[List[str]] = None,
        source: str = "user_interaction",
        is_user_correction: bool = False,
        is_task_critical: bool = False,
    ) -> BaseMemoryItem:
        """Stores a new memory item with calculated importance score."""
        imp_score = importance_engine.calculate_importance(
            content=content,
            category=category,
            is_user_correction=is_user_correction,
            is_task_critical=is_task_critical,
        )

        mem = BaseMemoryItem(
            user_id=user_id,
            content=content,
            category=category,
            importance_score=imp_score,
            tags=tags or [],
            source=source,
        )

        with self._lock:
            self._memories[mem.id] = mem
            max_long = getattr(settings, "MAX_LONG_TERM_MEMORY", 50000)
            if len(self._memories) > max_long:
                # Evict lowest importance memory
                lowest_id = min(self._memories.keys(), key=lambda k: self._memories[k].importance_score)
                del self._memories[lowest_id]

        logger.info(f"Stored memory '{mem.id}' (Category: {category.value}, Importance: {imp_score}).")
        return mem

    def retrieve_memories(
        self,
        query: str,
        user_id: str = "default_user",
        top_k: int = 5,
    ) -> List[BaseMemoryItem]:
        """Retrieves relevant memories using hybrid ranking."""
        with self._lock:
            all_mems = list(self._memories.values())

        results = memory_retriever.rank_and_retrieve(query, all_mems, top_k=top_k, user_id=user_id)
        memory_analytics_tracker.record_retrieval(hit=len(results) > 0)
        return results

    def compress_context_for_prompt(
        self,
        query: str,
        user_id: str = "default_user",
        top_k: int = 5,
    ) -> Tuple[str, float]:
        """Retrieves and compresses memory context for LLM prompt."""
        mems = self.retrieve_memories(query, user_id=user_id, top_k=top_k)
        text, ratio = context_compression_engine.compress_memories_for_context(mems, max_items=top_k)
        memory_analytics_tracker.record_compression(ratio)
        return text, ratio

    def consolidate_memories(self, user_id: str = "default_user") -> int:
        """Consolidates duplicate memories for a user."""
        with self._lock:
            user_mems = [m for m in self._memories.values() if m.user_id == user_id]
            consolidated, merged_count = memory_consolidation_engine.consolidate_memories(user_mems)

            if merged_count > 0:
                # Update in-memory dict
                for m in user_mems:
                    if m.id in self._memories and m not in consolidated:
                        del self._memories[m.id]

                memory_analytics_tracker.record_consolidation(merged_count)

        return merged_count

    # GDPR Privacy & Security Compliance Functions
    def forget_user_data(self, user_id: str) -> int:
        """GDPR-style deletion of all memories for a user."""
        with self._lock:
            to_delete = [k for k, v in self._memories.items() if v.user_id == user_id]
            for k in to_delete:
                del self._memories[k]
            logger.info(f"GDPR Forgetting: Removed {len(to_delete)} memories for user '{user_id}'.")
            return len(to_delete)

    def export_user_data(self, user_id: str) -> List[Dict[str, Any]]:
        """Exports all memories for a user."""
        with self._lock:
            return [v.model_dump() for v in self._memories.values() if v.user_id == user_id]

    def get_analytics_summary(self) -> Dict[str, Any]:
        """Returns comprehensive memory system analytics."""
        graph_stats = relationship_graph.get_stats()
        with self._lock:
            tot = len(self._memories)
        return memory_analytics_tracker.get_summary(
            total_memories=tot,
            nodes_count=graph_stats["nodes_count"],
            edges_count=graph_stats["edges_count"],
        )


# Global EnterpriseMemoryManager instance
enterprise_memory_manager = EnterpriseMemoryManager()
