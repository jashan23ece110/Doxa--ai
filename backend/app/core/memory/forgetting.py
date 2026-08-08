"""
Memory Decay & Forgetting Engine.

Calculates memory decay over elapsed time, access frequency, and importance. Pinned memories never decay.
"""

import time
from typing import List
from app.core.logging import logger
from app.core.memory.memory_store import memory_store


class MemoryForgettingEngine:
    """Executes background decay passes to prune obsolete memories."""

    @staticmethod
    def run_decay_pass(user_id: str = "default_user", decay_threshold_days: float = 30.0) -> int:
        """Removes expired or deeply decayed non-pinned memories."""
        memories = memory_store.list_memories(user_id=user_id)
        now = time.time()
        expired_count = 0

        for item in memories:
            if item.pinned:
                continue

            # Check explicit expiration timestamp
            if item.expires_at and now >= item.expires_at:
                memory_store.delete_memory(item.id)
                expired_count += 1
                logger.info(f"Memory '{item.id}' expired and deleted.")
                continue

            # Check elapsed decay (> 30 days unaccessed with low importance)
            elapsed_days = (now - item.last_accessed) / 86400.0
            if elapsed_days >= decay_threshold_days and item.importance_score < 0.40:
                memory_store.delete_memory(item.id)
                expired_count += 1
                logger.info(f"Memory '{item.id}' decayed and pruned.")

        return expired_count


# Global MemoryForgettingEngine instance
forgetting_engine = MemoryForgettingEngine()
