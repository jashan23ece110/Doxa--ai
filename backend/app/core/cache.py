"""
Abstract Cache Provider Interface and In-Memory Implementation.

Paves the way for distributed Redis or semantic prompt caching in multi-worker deployments.
"""

from abc import ABC, abstractmethod
import time
from typing import Any, Dict, Optional, Tuple


class ICacheProvider(ABC):
    """Abstract interface for key-value caching providers."""

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Retrieves a value by key from the cache."""
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl_seconds: Optional[float] = None) -> None:
        """Stores a key-value pair in the cache with optional TTL."""
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """Deletes a key from the cache."""
        pass


class InMemoryCacheProvider(ICacheProvider):
    """Thread-safe in-memory cache provider implementation."""

    def __init__(self):
        self._store: Dict[str, Tuple[Any, Optional[float]]] = {}

    def get(self, key: str) -> Optional[Any]:
        if key not in self._store:
            return None
        val, expire_at = self._store[key]
        if expire_at is not None and time.time() > expire_at:
            del self._store[key]
            return None
        return val

    def set(self, key: str, value: Any, ttl_seconds: Optional[float] = None) -> None:
        expire_at = (time.time() + ttl_seconds) if ttl_seconds is not None else None
        self._store[key] = (value, expire_at)

    def delete(self, key: str) -> None:
        self._store.pop(key, None)


# Global default cache provider instance
cache_provider: ICacheProvider = InMemoryCacheProvider()
