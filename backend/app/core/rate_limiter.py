"""
Abstract Rate Limiter Interface and In-Memory Token Bucket Implementation.

Paves the way for distributed multi-worker rate limiting (Redis token bucket) in future stages.
"""

from abc import ABC, abstractmethod
import time
from typing import Dict, Tuple


class IRateLimiter(ABC):
    """Abstract interface for rate limiting strategies."""

    @abstractmethod
    def is_allowed(self, client_id: str, limit: int = 60, window_seconds: float = 60.0) -> bool:
        """Determines if a request from client_id is allowed under rate limits."""
        pass


class InMemoryRateLimiter(IRateLimiter):
    """Sliding window token bucket rate limiter implementation."""

    def __init__(self):
        self._history: Dict[str, Tuple[int, float]] = {}

    def is_allowed(self, client_id: str, limit: int = 60, window_seconds: float = 60.0) -> bool:
        now = time.time()
        if client_id not in self._history:
            self._history[client_id] = (1, now)
            return True

        count, first_seen = self._history[client_id]
        if now - first_seen > window_seconds:
            self._history[client_id] = (1, now)
            return True

        if count >= limit:
            return False

        self._history[client_id] = (count + 1, first_seen)
        return True


# Global default rate limiter instance
rate_limiter: IRateLimiter = InMemoryRateLimiter()
