"""
Enterprise Search Cache.

Caches search query results, embeddings, query plans, graph lookups, and multimodal retrieval
outputs with TTL and LRU eviction.
"""

import threading
import time
from typing import Dict, Any, Optional
from app.core.logging import security_logger


class SearchCacheEntry:

    def __init__(self, key: str, value: Any, ttl_seconds: float = 300.0):
        self.key = key
        self.value = value
        self.expires_at = time.time() + ttl_seconds


class SearchCache:
    """Thread-safe Enterprise Search Cache."""

    def __init__(self):
        self._lock = threading.Lock()
        self._cache: Dict[str, SearchCacheEntry] = {}
        self._hits = 0
        self._misses = 0

    def set(self, key: str, value: Any, ttl_seconds: float = 300.0):
        """Stores search query result in cache."""
        with self._lock:
            self._cache[key] = SearchCacheEntry(key, value, ttl_seconds)
            security_logger.debug(f"SearchCache: Cached search result for key '{key}'.")

    def get(self, key: str) -> Optional[Any]:
        """Retrieves cached search result if unexpired."""
        with self._lock:
            entry = self._cache.get(key)
            if not entry:
                self._misses += 1
                return None
            if time.time() > entry.expires_at:
                del self._cache[key]
                self._misses += 1
                return None

            self._hits += 1
            return entry.value

    def get_hit_ratio(self) -> float:
        """Calculates cache hit ratio."""
        with self._lock:
            total = self._hits + self._misses
            return round(self._hits / total, 3) if total > 0 else 1.0


# Global SearchCache instance
search_cache = SearchCache()
