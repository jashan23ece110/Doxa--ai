"""
Connector Metrics Tracker for Universal Integration Platform.

Tracks latency, availability, success/failure rates, auth failures, retries, and rate limit hits.
"""

import threading
from typing import Dict, Any, List


class ConnectorMetricsTracker:
    """Thread-safe metrics tracker for integration connectors."""

    def __init__(self):
        self._lock = threading.Lock()
        self.total_requests_count: int = 0
        self.successful_requests_count: int = 0
        self.failed_requests_count: int = 0
        self.auth_failures_count: int = 0
        self.rate_limit_hits_count: int = 0
        self.latencies_ms: List[float] = []

    def record_request(self, success: bool, latency_ms: float = 0.0, is_auth_failure: bool = False, is_rate_limit: bool = False) -> None:
        """Records an integration request execution."""
        with self._lock:
            self.total_requests_count += 1
            if success:
                self.successful_requests_count += 1
            else:
                self.failed_requests_count += 1

            if is_auth_failure:
                self.auth_failures_count += 1
            if is_rate_limit:
                self.rate_limit_hits_count += 1

            self.latencies_ms.append(latency_ms)
            if len(self.latencies_ms) > 1000:
                self.latencies_ms = self.latencies_ms[-1000:]

    def get_summary(self) -> Dict[str, Any]:
        """Returns summary metrics across all connectors."""
        with self._lock:
            rate = (
                round(self.successful_requests_count / self.total_requests_count, 2)
                if self.total_requests_count > 0
                else 1.0
            )
            avg_lat = (
                round(sum(self.latencies_ms) / len(self.latencies_ms), 2)
                if self.latencies_ms
                else 0.0
            )

            return {
                "total_requests": self.total_requests_count,
                "successful_requests": self.successful_requests_count,
                "failed_requests": self.failed_requests_count,
                "auth_failures": self.auth_failures_count,
                "rate_limit_hits": self.rate_limit_hits_count,
                "success_rate": rate,
                "average_latency_ms": avg_lat,
            }


# Global ConnectorMetricsTracker instance
connector_metrics_tracker = ConnectorMetricsTracker()
