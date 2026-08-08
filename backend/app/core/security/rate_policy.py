"""
Rate Policy Engine for Enterprise Zero-Trust Security Platform.

Enterprise rate limiting per user, per tenant, per API key with burst limits and sliding windows.
"""

import time
import threading
from typing import Dict, Any, List
from app.core.logging import security_logger


class RatePolicyEngine:
    """Sliding-window rate limiter for enterprise rate plans."""

    def __init__(self):
        self._lock = threading.Lock()
        self._window_history: Dict[str, List[float]] = {}

    def check_rate_limit(
        self,
        identifier: str,
        limit_per_minute: int = 120,
        window_seconds: float = 60.0,
    ) -> bool:
        """
        Sliding-window rate limit checker. Returns True if allowed, False if limit exceeded.
        """
        now = time.time()
        with self._lock:
            if identifier not in self._window_history:
                self._window_history[identifier] = []

            # Filter out timestamps outside window
            cutoff = now - window_seconds
            self._window_history[identifier] = [
                t for t in self._window_history[identifier] if t > cutoff
            ]

            if len(self._window_history[identifier]) >= limit_per_minute:
                security_logger.warning(f"Rate limit exceeded for identifier '{identifier}' ({limit_per_minute}/min).")
                return False

            self._window_history[identifier].append(now)
            return True


# Global RatePolicyEngine instance
rate_policy_engine = RatePolicyEngine()
