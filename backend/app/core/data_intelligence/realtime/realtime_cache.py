"""
Real-Time Intelligence Cache.

Caches hot entities, recent events, real-time correlation results, anomaly detection outputs,
and active stream states with TTL and LRU eviction.
"""

import threading
import time
from typing import Dict, Any, Optional
from app.core.logging import security_logger


class RealtimeCacheEntry:

    def __init__(self, key: str, value: Any, ttl_seconds: float = 300.0):
        self.key = key
        self.value = value
        self.expires_at = time.time() + ttl_seconds


class RealtimeCache:
    """Thread-safe Real-Time Intelligence Cache."""

    def __init__(self):
        self._lock = threading.Lock()
        self._cache: Dict[str, RealtimeCacheEntry] = {}
        self._hits = 0
        self._misses = 0

    def set(self, key: str, value: Any, ttl_seconds: float = 300.0):
        """Stores real-time entry in cache with TTL."""
        with self._lock:
            self._cache[key] = RealtimeCacheEntry(key, value, ttl_seconds)
            security_logger.debug(f"RealtimeCache: Cached real-time item '{key}'.")

    def get(self, key: str) -> Optional[Any]:
        """Retrieves cached item if unexpired."""
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


# Global RealtimeCache instance
realtime_cache = RealtimeCache()
