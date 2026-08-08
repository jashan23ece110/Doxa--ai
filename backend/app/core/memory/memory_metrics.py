"""
Memory Metrics Tracker.

Tracks memory hits, misses, retrieval latency, stored memories, merged memories, and profile updates.
"""

import threading
from typing import Dict, Any


class MemoryMetricsTracker:
    """Thread-safe metrics tracker for memory operations."""

    def __init__(self):
        self._lock = threading.Lock()
        self.hits: int = 0
        self.misses: int = 0
        self.stored: int = 0
        self.merged: int = 0
        self.expired: int = 0
        self.profile_updates: int = 0

    def record_hit(self) -> None:
        with self._lock:
            self.hits += 1

    def record_miss(self) -> None:
        with self._lock:
            self.misses += 1

    def record_stored(self) -> None:
        with self._lock:
            self.stored += 1

    def record_merged(self) -> None:
        with self._lock:
            self.merged += 1

    def record_expired(self, count: int = 1) -> None:
        with self._lock:
            self.expired += count

    def get_metrics_summary(self) -> Dict[str, Any]:
        with self._lock:
            total_requests = self.hits + self.misses
            hit_rate = round(self.hits / total_requests, 4) if total_requests > 0 else 0.0
            return {
                "hits": self.hits,
                "misses": self.misses,
                "hit_rate": hit_rate,
                "stored": self.stored,
                "merged": self.merged,
                "expired": self.expired,
            }


# Global MemoryMetricsTracker instance
memory_metrics_tracker = MemoryMetricsTracker()
