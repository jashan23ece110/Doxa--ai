"""
Metrics Engine for Enterprise Observability Platform.

Collects system metrics and calculates P50, P90, P95, P99 latency percentiles across API,
LLM, Tool, Embedding, Retrieval, Memory, Reasoning, and Agent executions.
"""

import math
import threading
from typing import Dict, Any, List, Optional
from app.core.observability.observability_models import MetricRecord


class MetricsEngine:
    """Thread-safe latency percentile calculation and metrics storage."""

    def __init__(self):
        self._lock = threading.Lock()
        self._latencies: List[float] = []
        self._records: Dict[str, List[MetricRecord]] = {}

    def record_latency(self, latency_ms: float, component: str = "general") -> None:
        """Records a latency measurement."""
        with self._lock:
            self._latencies.append(latency_ms)
            if len(self._latencies) > 10000:
                self._latencies = self._latencies[-10000:]

            rec = MetricRecord(metric_name=f"{component}_latency", value=latency_ms)
            if component not in self._records:
                self._records[component] = []
            self._records[component].append(rec)
            if len(self._records[component]) > 1000:
                self._records[component] = self._records[component][-1000:]

    def _calculate_percentile(self, sorted_vals: List[float], percentile: float) -> float:
        """Calculates exact percentile from sorted float array."""
        if not sorted_vals:
            return 0.0
        k = (len(sorted_vals) - 1) * (percentile / 100.0)
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return round(sorted_vals[int(k)], 2)
        d0 = sorted_vals[int(f)] * (c - k)
        d1 = sorted_vals[int(c)] * (k - f)
        return round(d0 + d1, 2)

    def get_percentiles(self) -> Dict[str, float]:
        """Returns P50, P90, P95, and P99 latency percentiles."""
        with self._lock:
            if not self._latencies:
                return {"p50": 0.0, "p90": 0.0, "p95": 0.0, "p99": 0.0}

            s = sorted(self._latencies)
            return {
                "p50": self._calculate_percentile(s, 50.0),
                "p90": self._calculate_percentile(s, 90.0),
                "p95": self._calculate_percentile(s, 95.0),
                "p99": self._calculate_percentile(s, 99.0),
            }


# Global MetricsEngine instance
metrics_engine = MetricsEngine()
