"""
Enterprise Memory Engine Orchestrator.

Orchestrates non-blocking automatic extraction, 5-factor relevance ranking,
user profile synthesis, and prompt personalization within token budget constraints (1200 max tokens).
"""

import asyncio
import time
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.logging import logger
from app.core.memory.forgetting import forgetting_engine
from app.core.memory.memory_classifier import memory_classifier
from app.core.memory.memory_extractor import memory_extractor
from app.core.memory.memory_metrics import memory_metrics_tracker
from app.core.memory.memory_ranker import memory_ranker
from app.core.memory.memory_store import memory_store
from app.core.memory.profile_builder import profile_builder


class EnterpriseMemoryEngine:
    """Orchestrates enterprise long-term memory operations."""

    @staticmethod
    def _extract_and_store_sync(user_text: str, user_id: str = "default_user") -> None:
        """Synchronous memory extraction, classification, merging, and decay pass."""
        candidates = memory_extractor.extract_memories_from_text(user_text, user_id=user_id)

        for candidate in candidates:
            action, item = memory_classifier.classify_and_process(candidate)
            if action == "store":
                memory_metrics_tracker.record_stored()
                logger.info(f"Stored long-term memory item '{candidate.title}'")
            elif action == "merge":
                memory_metrics_tracker.record_merged()
                logger.info(f"Merged duplicate long-term memory item '{candidate.title}'")

        # Run periodic decay pass
        forgetting_engine.run_decay_pass(user_id=user_id)

    @classmethod
    async def process_conversation_async(cls, user_text: str, user_id: str = "default_user") -> None:
        """Schedules background memory extraction without delaying LLM completion."""
        if not settings.MEMORY_ENABLED:
            return

        try:
            asyncio.create_task(
                asyncio.to_thread(cls._extract_and_store_sync, user_text, user_id)
            )
        except Exception as e:
            logger.warning(f"Failed to launch non-blocking memory processing: {e}")

    @classmethod
    def get_personalized_context(cls, query: str, user_id: str = "default_user", max_items: int = 5) -> str:
        """Retrieves and formats top-ranked memory items into prompt context string."""
        if not settings.MEMORY_ENABLED:
            return ""

        start_time = time.time()
        memories = memory_store.list_memories(user_id=user_id)

        if not memories:
            memory_metrics_tracker.record_miss()
            return ""

        ranked_pairs = memory_ranker.rank_memories(memories, query=query, top_k=max_items)
        if not ranked_pairs:
            memory_metrics_tracker.record_miss()
            return ""

        memory_metrics_tracker.record_hit()
        user_profile = profile_builder.build_user_profile(user_id=user_id)

        lines = ["=== USER MEMORY & PERSONALIZATION PROFILE ==="]
        lines.append(f"Preferred Language: {user_profile['preferred_language']}")
        lines.append(f"Communication Style: {user_profile['communication_style']}")

        lines.append("\nRelevant Memories:")
        for item, score in ranked_pairs:
            # Update last accessed timestamp & access count
            memory_store.update_memory(item.id, {"last_accessed": time.time(), "access_count": item.access_count + 1})
            lines.append(f"- [{item.type.value.upper()}] {item.content} (score={score:.2f})")

        duration_ms = (time.time() - start_time) * 1000
        logger.debug(f"Retrieved personalized memory context in {duration_ms:.2f}ms")

        return "\n".join(lines)


# Global EnterpriseMemoryEngine instance
enterprise_memory_engine = EnterpriseMemoryEngine()
