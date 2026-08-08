"""
Layer 3: Persistent Long-Term Semantic Memory Manager.

Manages persistent user facts, preferences, skills, tech stack, and goals with
importance scoring, category tagging, deduplication, and disk persistence.
"""

import json
import os
import threading
import time
import uuid
from pathlib import Path
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.logging import logger


class LongTermMemory:
    """Persistent Long-Term Semantic Memory Store."""

    def __init__(self, persistence_path: Optional[str] = None):
        self.persistence_path = persistence_path or settings.MEMORY_STORE_PATH
        self._lock = threading.Lock()
        self.memories: Dict[str, Dict[str, Any]] = {}
        self._load_from_disk()

    def _save_to_disk(self) -> None:
        """Persists long-term memories to disk."""
        if not self.persistence_path:
            return
        try:
            parent_dir = Path(self.persistence_path).parent
            parent_dir.mkdir(parents=True, exist_ok=True)
            with open(self.persistence_path, "w", encoding="utf-8") as f:
                json.dump(self.memories, f, ensure_ascii=False)
            logger.debug(f"Saved {len(self.memories)} long-term memories to disk.")
        except Exception as e:
            logger.error(f"Failed to save long-term memories to disk: {e}")

    def _load_from_disk(self) -> None:
        """Loads long-term memories from disk."""
        if not self.persistence_path or not os.path.exists(self.persistence_path):
            return
        try:
            with open(self.persistence_path, "r", encoding="utf-8") as f:
                self.memories = json.load(f)
            logger.info(f"Loaded {len(self.memories)} long-term memories from disk.")
        except Exception as e:
            logger.warning(f"Failed to load long-term memories from disk: {e}")

    @staticmethod
    def calculate_importance(content: str, category: str) -> float:
        """Calculates memory importance score (0.0 - 1.0)."""
        cat_lower = category.lower()
        if cat_lower in ("instruction", "goal"):
            return 0.95
        if cat_lower in ("preference", "project", "skill", "education"):
            return 0.85
        if cat_lower in ("fact", "career"):
            return 0.70

        # Heuristic length / keyword inspection
        c_lower = content.lower()
        if any(kw in c_lower for kw in ["always", "never", "must", "prefer", "my name is", "i work as"]):
            return 0.80
        return 0.50

    def add_memory(
        self,
        content: str,
        category: str = "fact",
        importance_score: Optional[float] = None,
        ttl_days: Optional[int] = settings.MEMORY_TTL_DAYS,
    ) -> Dict[str, Any]:
        """Adds a new memory with automatic importance scoring and deduplication."""
        with self._lock:
            score = importance_score if importance_score is not None else self.calculate_importance(content, category)

            # Ignore low importance memories below threshold
            if score < settings.MEMORY_IMPORTANCE_THRESHOLD:
                logger.debug(f"Rejected low importance memory ({score:.2f} < {settings.MEMORY_IMPORTANCE_THRESHOLD}): '{content[:30]}...'")
                return {}

            # Deduplication: Check if identical memory content exists
            for m_id, item in self.memories.items():
                if item["content"].strip().lower() == content.strip().lower():
                    # Update timestamp & score
                    item["timestamp"] = time.time()
                    item["importance_score"] = max(item["importance_score"], score)
                    self._save_to_disk()
                    return item

            mem_id = str(uuid.uuid4())
            now = time.time()
            expires_at = (now + ttl_days * 86400) if ttl_days else None

            memory_item = {
                "memory_id": mem_id,
                "content": content,
                "category": category,
                "importance_score": score,
                "timestamp": now,
                "expires_at": expires_at,
            }
            self.memories[mem_id] = memory_item
            self._save_to_disk()

            logger.info(f"Stored long-term memory [{category}] (Score: {score:.2f}): '{content[:40]}...'")
            return memory_item

    def get_all_valid_memories(self) -> List[Dict[str, Any]]:
        """Returns all non-expired memories."""
        with self._lock:
            now = time.time()
            valid = []
            for item in self.memories.values():
                if item.get("expires_at") is not None and now > item["expires_at"]:
                    continue
                valid.append(item)
            return valid


# Global LongTermMemory instance
long_term_memory = LongTermMemory()
