"""
Reasoning Metrics Tracker for Enterprise Cognitive Reasoning Engine.

Tracks reasoning latency, planning time, verification time, reasoning depth,
revision count, confidence scores, retry counts, hallucination rate, and success rate.
"""

import threading
import time
from typing import Dict, Any, List


class ReasoningMetricsTracker:
    """Thread-safe metrics tracker for cognitive reasoning operations."""

    def __init__(self):
        self._lock = threading.Lock()
        self.total_runs: int = 0
        self.successful_runs: int = 0
        self.failed_runs: int = 0
        self.revisions_triggered: int = 0
        self.hallucinations_detected: int = 0
        self.confidence_sum: float = 0.0
        self.latencies_ms: List[float] = []

    def record_run(
        self,
        success: bool = True,
        latency_ms: float = 0.0,
        confidence: float = 0.85,
        revisions: int = 0,
        hallucination_found: bool = False,
    ) -> None:
        """Records a completed cognitive reasoning run."""
        with self._lock:
            self.total_runs += 1
            if success:
                self.successful_runs += 1
            else:
                self.failed_runs += 1
            
            self.revisions_triggered += revisions
            if hallucination_found:
                self.hallucinations_detected += 1
            
            self.confidence_sum += confidence
            self.latencies_ms.append(latency_ms)
            if len(self.latencies_ms) > 1000:
                self.latencies_ms = self.latencies_ms[-1000:]

    def get_summary(self) -> Dict[str, Any]:
        """Returns summary statistics across reasoning executions."""
        with self._lock:
            avg_latency = (
                round(sum(self.latencies_ms) / len(self.latencies_ms), 2)
                if self.latencies_ms
                else 0.0
            )
            avg_confidence = (
                round(self.confidence_sum / self.total_runs, 2)
                if self.total_runs > 0
                else 0.0
            )
            success_rate = (
                round(self.successful_runs / self.total_runs, 4)
                if self.total_runs > 0
                else 1.0
            )
            hallucination_rate = (
                round(self.hallucinations_detected / self.total_runs, 4)
                if self.total_runs > 0
                else 0.0
            )

            return {
                "total_runs": self.total_runs,
                "successful_runs": self.successful_runs,
                "failed_runs": self.failed_runs,
                "success_rate": success_rate,
                "revisions_triggered": self.revisions_triggered,
                "hallucinations_detected": self.hallucinations_detected,
                "hallucination_rate": hallucination_rate,
                "avg_confidence": avg_confidence,
                "avg_latency_ms": avg_latency,
            }


# Global ReasoningMetricsTracker instance
reasoning_metrics_tracker = ReasoningMetricsTracker()
