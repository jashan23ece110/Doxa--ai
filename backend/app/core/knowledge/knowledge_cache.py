"""
Knowledge Cache for Enterprise Knowledge Platform.

Caches research results, knowledge graphs, evidence, fact verification, and source reliability
with TTL and invalidation support.
"""

import time
import threading
from typing import Dict, Any, Optional


class KnowledgeCache:
    """Thread-safe TTL knowledge cache."""

    def __init__(self, ttl_seconds: int = 3600):
        self.ttl_seconds = ttl_seconds
        self._lock = threading.Lock()
        self._cache: Dict[str, Dict[str, Any]] = {}

    def set(self, key: str, value: Any) -> None:
        """Sets a cache entry with timestamp."""
        with self._lock:
            self._cache[key] = {
                "value": value,
                "timestamp": time.time(),
            }

    def get(self, key: str) -> Optional[Any]:
        """Gets a cache entry if not expired."""
        with self._lock:
            entry = self._cache.get(key)
            if entry:
                if time.time() - entry["timestamp"] < self.ttl_seconds:
                    return entry["value"]
                else:
                    del self._cache[key]
        return None


# Global KnowledgeCache instance
knowledge_cache = KnowledgeCache()
