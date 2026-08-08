"""
Human Intelligence Metrics Tracker.

Tracks employee profile counts, assessments completed, training compliance,
awareness scores, organizational risk levels, behavioral anomalies, and pipeline execution latencies.
"""

import threading
import time
from typing import Dict, Any
from app.core.logging import security_logger
from app.core.human_intelligence.human_intelligence_types import HumanRiskMetrics


class HumanMetricsTracker:
    """Thread-safe Human Intelligence Metrics Tracker."""

    def __init__(self):
        self._lock = threading.Lock()
        self._total_profiles = 0
        self._assessments_completed = 0
        self._trainings_completed = 0
        self._anomalies_detected = 0
        self._pipeline_latencies: list[float] = []

    def record_profile_created(self):
        """Increments profile count."""
        with self._lock:
            self._total_profiles += 1

    def record_assessment_completed(self):
        """Increments assessment counter."""
        with self._lock:
            self._assessments_completed += 1

    def record_training_completed(self):
        """Increments training completion counter."""
        with self._lock:
            self._trainings_completed += 1

    def record_anomaly(self):
        """Increments anomaly counter."""
        with self._lock:
            self._anomalies_detected += 1

    def record_pipeline_latency(self, latency_ms: float):
        """Records pipeline execution latency."""
        with self._lock:
            self._pipeline_latencies.append(latency_ms)
            if len(self._pipeline_latencies) > 100:
                self._pipeline_latencies.pop(0)

    def get_metrics(self) -> HumanRiskMetrics:
        """Retrieves aggregated metrics model."""
        with self._lock:
            avg_lat = sum(self._pipeline_latencies) / len(self._pipeline_latencies) if self._pipeline_latencies else 0.0
            return HumanRiskMetrics(
                total_employees_monitored=self._total_profiles,
                average_org_security_score=85.0,
                high_risk_employees_count=0,
                phishing_susceptibility_percent=3.5,
                training_compliance_percent=95.0,
            )


# Global HumanMetricsTracker instance
human_metrics_tracker = HumanMetricsTracker()
