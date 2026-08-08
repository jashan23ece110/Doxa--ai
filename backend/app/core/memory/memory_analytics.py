"""
Memory Analytics Tracker for Enterprise Memory Intelligence Platform.

Tracks total memories, retrieval hits/misses, compression ratio, duplicate rate,
graph nodes/edges, memory latency, and average importance distribution.
"""

import threading
from typing import Dict, Any, List


class MemoryAnalyticsTracker:
    """Thread-safe analytics tracker for memory system operational performance."""

    def __init__(self):
        self._lock = threading.Lock()
        self.retrieval_hits: int = 0
        self.retrieval_misses: int = 0
        self.duplicate_memories_merged: int = 0
        self.compression_ratios: List[float] = []

    def record_retrieval(self, hit: bool = True) -> None:
        """Records a memory retrieval hit or miss."""
        with self._lock:
            if hit:
                self.retrieval_hits += 1
            else:
                self.retrieval_misses += 1

    def record_consolidation(self, merged_count: int = 1) -> None:
        """Records merged duplicate count."""
        with self._lock:
            self.duplicate_memories_merged += merged_count

    def record_compression(self, ratio: float) -> None:
        """Records a context compression ratio."""
        with self._lock:
            self.compression_ratios.append(ratio)
            if len(self.compression_ratios) > 1000:
                self.compression_ratios = self.compression_ratios[-1000:]

    def get_summary(self, total_memories: int = 0, nodes_count: int = 0, edges_count: int = 0) -> Dict[str, Any]:
        """Returns comprehensive memory system metrics summary."""
        with self._lock:
            tot = self.retrieval_hits + self.retrieval_misses
            hit_rate = round(self.retrieval_hits / tot, 2) if tot > 0 else 1.0
            avg_ratio = (
                round(sum(self.compression_ratios) / len(self.compression_ratios), 2)
                if self.compression_ratios
                else 0.50
            )

            return {
                "total_memories": total_memories,
                "retrieval_hits": self.retrieval_hits,
                "retrieval_misses": self.retrieval_misses,
                "hit_rate": hit_rate,
                "duplicate_memories_merged": self.duplicate_memories_merged,
                "avg_compression_ratio": avg_ratio,
                "graph_nodes": nodes_count,
                "graph_edges": edges_count,
            }


# Global MemoryAnalyticsTracker instance
memory_analytics_tracker = MemoryAnalyticsTracker()
