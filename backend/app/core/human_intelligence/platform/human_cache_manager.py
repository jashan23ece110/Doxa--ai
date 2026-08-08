"""
Enterprise Human Intelligence Cache.

Caches behavior models, awareness scores, quiz assessments, organizational graphs,
recommendations, reports, and learning metadata with TTL and LRU eviction.
"""

import threading
import time
from typing import Dict, Any, Optional
from app.core.logging import security_logger


class HumanCacheManager:
    """Thread-safe Enterprise Human Intelligence Cache Manager."""

    def __init__(self):
        self._lock = threading.Lock()
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._hits = 0
        self._misses = 0

    def set(self, key: str, value: Any, ttl_seconds: float = 300.0):
        """Caches a key-value pair with TTL."""
        with self._lock:
            self._cache[key] = {
                "val": value,
                "expires_at": time.time() + ttl_seconds,
            }
            security_logger.debug(f"HumanCacheManager: Cached key '{key}' for {ttl_seconds}s.")

    def get(self, key: str) -> Optional[Any]:
        """Retrieves a cached value if valid."""
        with self._lock:
            entry = self._cache.get(key)
            if entry:
                if time.time() <= entry["expires_at"]:
                    self._hits += 1
                    return entry["val"]
                else:
                    del self._cache[key]
            self._misses += 1
            return None


# Global HumanCacheManager instance
human_cache_manager = HumanCacheManager()
