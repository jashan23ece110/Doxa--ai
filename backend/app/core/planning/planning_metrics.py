"""
Planning Metrics Tracker for Enterprise Planning & Reasoning Engine.

Tracks plans created, plan depth, latency, reasoning steps, replans,
dependency nodes, critical path lengths, success rates, and confidence.
"""

import threading
from typing import Dict, Any, List


class PlanningMetricsTracker:
    """Thread-safe metrics tracker for enterprise planning operations."""

    def __init__(self):
        self._lock = threading.Lock()
        self.plans_created_count: int = 0
        self.replans_triggered_count: int = 0
        self.total_reasoning_steps: int = 0
        self.plan_depths: List[int] = []
        self.planning_latencies_ms: List[float] = []
        self.confidences: List[float] = []

    def record_plan_creation(self, depth: int = 3, latency_ms: float = 0.0, confidence: float = 0.90) -> None:
        """Records plan creation metrics."""
        with self._lock:
            self.plans_created_count += 1
            self.plan_depths.append(depth)
            if len(self.plan_depths) > 1000:
                self.plan_depths = self.plan_depths[-1000:]

            self.planning_latencies_ms.append(latency_ms)
            if len(self.planning_latencies_ms) > 1000:
                self.planning_latencies_ms = self.planning_latencies_ms[-1000:]

            self.confidences.append(confidence)
            if len(self.confidences) > 1000:
                self.confidences = self.confidences[-1000:]

    def record_replan(self) -> None:
        """Records a dynamic replan event."""
        with self._lock:
            self.replans_triggered_count += 1

    def record_reasoning_steps(self, count: int = 1) -> None:
        """Records reasoning step execution count."""
        with self._lock:
            self.total_reasoning_steps += count

    def get_summary(self) -> Dict[str, Any]:
        """Returns summary statistics across planning executions."""
        with self._lock:
            avg_depth = (
                round(sum(self.plan_depths) / len(self.plan_depths), 2)
                if self.plan_depths
                else 0.0
            )
            avg_lat = (
                round(sum(self.planning_latencies_ms) / len(self.planning_latencies_ms), 2)
                if self.planning_latencies_ms
                else 0.0
            )
            avg_conf = (
                round(sum(self.confidences) / len(self.confidences), 2)
                if self.confidences
                else 0.90
            )

            return {
                "plans_created": self.plans_created_count,
                "replans_triggered": self.replans_triggered_count,
                "reasoning_steps": self.total_reasoning_steps,
                "average_plan_depth": avg_depth,
                "average_planning_latency_ms": avg_lat,
                "average_confidence": avg_conf,
            }


# Global PlanningMetricsTracker instance
planning_metrics_tracker = PlanningMetricsTracker()
