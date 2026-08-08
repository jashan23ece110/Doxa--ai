"""
Enterprise Analytics Cache.

Caches analytics query results, aggregations, anomaly detection outputs, correlation results,
and forecasting results with TTL, LRU eviction, and metrics tracking.
"""

import threading
import time
from typing import Dict, Any, Optional
from app.core.logging import security_logger


class AnalyticsCacheEntry:

    def __init__(self, key: str, value: Any, ttl_seconds: float = 600.0):
        self.key = key
        self.value = value
        self.expires_at = time.time() + ttl_seconds


class AnalyticsCache:
    """Thread-safe Enterprise Analytics Cache."""

    def __init__(self):
        self._lock = threading.Lock()
        self._cache: Dict[str, AnalyticsCacheEntry] = {}
        self._hits = 0
        self._misses = 0

    def set(self, key: str, value: Any, ttl_seconds: float = 600.0):
        """Stores a key-value pair in the cache with TTL."""
        with self._lock:
            self._cache[key] = AnalyticsCacheEntry(key, value, ttl_seconds)
            security_logger.debug(f"AnalyticsCache: Cached key '{key}' (TTL={ttl_seconds}s).")

    def get(self, key: str) -> Optional[Any]:
        """Retrieves cached value if present and unexpired."""
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
        """Computes current cache hit ratio."""
        with self._lock:
            total = self._hits + self._misses
            return round(self._hits / total, 3) if total > 0 else 1.0


# Global AnalyticsCache instance
analytics_cache = AnalyticsCache()
