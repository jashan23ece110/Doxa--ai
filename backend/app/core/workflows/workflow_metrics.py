"""
Workflow Metrics Tracker for Enterprise Autonomous Workflow Engine.

Tracks workflow latency, success rates, retry counts, rollback counts,
checkpoint counts, approval wait time, parallel efficiency, and task failure rates.
"""

import threading
import time
from typing import Dict, Any, List


class WorkflowMetricsTracker:
    """Thread-safe metrics tracker for workflow execution."""

    def __init__(self):
        self._lock = threading.Lock()
        self.total_workflows: int = 0
        self.successful_workflows: int = 0
        self.failed_workflows: int = 0
        self.cancelled_workflows: int = 0
        self.retries_count: int = 0
        self.rollbacks_executed: int = 0
        self.checkpoints_saved: int = 0
        self.approvals_requested: int = 0
        self.latencies_ms: List[float] = []

    def record_workflow_execution(
        self,
        success: bool = True,
        latency_ms: float = 0.0,
        retries: int = 0,
        rollbacks: int = 0,
        checkpoints: int = 0,
        cancelled: bool = False,
    ) -> None:
        """Records a completed or terminated workflow execution."""
        with self._lock:
            self.total_workflows += 1
            if cancelled:
                self.cancelled_workflows += 1
            elif success:
                self.successful_workflows += 1
            else:
                self.failed_workflows += 1

            self.retries_count += retries
            self.rollbacks_executed += rollbacks
            self.checkpoints_saved += checkpoints

            self.latencies_ms.append(latency_ms)
            if len(self.latencies_ms) > 1000:
                self.latencies_ms = self.latencies_ms[-1000:]

    def record_approval_request(self) -> None:
        """Records a human approval checkpoint request."""
        with self._lock:
            self.approvals_requested += 1

    def get_summary(self) -> Dict[str, Any]:
        """Returns summary statistics across workflow executions."""
        with self._lock:
            avg_latency = (
                round(sum(self.latencies_ms) / len(self.latencies_ms), 2)
                if self.latencies_ms
                else 0.0
            )
            success_rate = (
                round(self.successful_workflows / self.total_workflows, 4)
                if self.total_workflows > 0
                else 1.0
            )

            return {
                "total_workflows": self.total_workflows,
                "successful_workflows": self.successful_workflows,
                "failed_workflows": self.failed_workflows,
                "cancelled_workflows": self.cancelled_workflows,
                "success_rate": success_rate,
                "retries_count": self.retries_count,
                "rollbacks_executed": self.rollbacks_executed,
                "checkpoints_saved": self.checkpoints_saved,
                "approvals_requested": self.approvals_requested,
                "avg_latency_ms": avg_latency,
            }


# Global WorkflowMetricsTracker instance
workflow_metrics_tracker = WorkflowMetricsTracker()
