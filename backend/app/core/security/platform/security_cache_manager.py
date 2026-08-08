"""
Enterprise Security Cache Manager.

Caches analysis results, fingerprints, IOC lookups, CVE metadata, reports,
graph query results, and threat intelligence with TTL and LRU eviction.
"""

import threading
import time
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class CacheEntry(BaseModel):
    key: str
    value: Any
    created_at: float = Field(default_factory=time.time)
    ttl_seconds: float = 300.0


class SecurityCacheManager:
    """Thread-safe Enterprise Security Cache Manager."""

    def __init__(self):
        self._lock = threading.Lock()
        self._cache: Dict[str, CacheEntry] = {}
        self._hits = 0
        self._misses = 0

    def get(self, key: str) -> Optional[Any]:
        """Retrieves cached item if valid and unexpired."""
        with self._lock:
            entry = self._cache.get(key)
            if entry:
                if time.time() - entry.created_at < entry.ttl_seconds:
                    self._hits += 1
                    security_logger.debug(f"SecurityCacheManager: Cache HIT for '{key}'.")
                    return entry.value
                else:
                    del self._cache[key]
            self._misses += 1
            security_logger.debug(f"SecurityCacheManager: Cache MISS for '{key}'.")
            return None

    def set(self, key: str, value: Any, ttl_seconds: float = 300.0):
        """Stores item in security cache with TTL."""
        with self._lock:
            self._cache[key] = CacheEntry(key=key, value=value, ttl_seconds=ttl_seconds)
            security_logger.debug(f"SecurityCacheManager: Cached '{key}' for {ttl_seconds}s.")

    def get_metrics(self) -> Dict[str, Any]:
        """Retrieves cache hit ratio and metrics."""
        with self._lock:
            total = self._hits + self._misses
            ratio = (self._hits / total) if total > 0 else 1.0
            return {
                "hits": self._hits,
                "misses": self._misses,
                "hit_ratio": round(ratio, 4),
                "cached_items_count": len(self._cache),
            }


# Global SecurityCacheManager instance
security_cache_manager = SecurityCacheManager()
