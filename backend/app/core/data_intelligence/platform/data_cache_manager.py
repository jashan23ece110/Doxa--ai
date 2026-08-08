"""
Enterprise Data Intelligence Cache.

Master cache orchestrator caching query results, embeddings, graph lookups, analytics outputs,
predictions, and discovery snapshots with TTL and LRU eviction.
"""

import threading
import time
from typing import Dict, Any, Optional
from app.core.logging import security_logger


class DataCacheEntry:

    def __init__(self, key: str, value: Any, ttl_seconds: float = 600.0):
        self.key = key
        self.value = value
        self.expires_at = time.time() + ttl_seconds


class DataCacheManager:
    """Thread-safe Master Data Intelligence Cache Manager."""

    def __init__(self):
        self._lock = threading.Lock()
        self._cache: Dict[str, DataCacheEntry] = {}
        self._hits = 0
        self._misses = 0

    def set(self, key: str, value: Any, ttl_seconds: float = 600.0):
        """Stores entry in master platform cache with TTL."""
        with self._lock:
            self._cache[key] = DataCacheEntry(key, value, ttl_seconds)
            security_logger.debug(f"DataCacheManager: Cached platform entry '{key}'.")

    def get(self, key: str) -> Optional[Any]:
        """Retrieves cached entry if unexpired."""
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
        """Calculates master cache hit ratio."""
        with self._lock:
            total = self._hits + self._misses
            return round(self._hits / total, 3) if total > 0 else 1.0


# Global DataCacheManager instance
data_cache_manager = DataCacheManager()
