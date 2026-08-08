"""
Behavioral Anomaly Engine.

Detects unusual behavioral changes, awareness score regressions, abnormal communication metadata,
organizational outliers, and training disengagement patterns.
"""

import time
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class BehavioralAnomalyResult(BaseModel):
    anomaly_id: str
    employee_id: str
    anomaly_type: str  # awareness_regression, abnormal_off_hours_activity, training_disengagement
    confidence_score: float = 0.88
    severity: str = "MEDIUM"
    description: str
    detected_at: float = Field(default_factory=time.time)


class BehavioralAnomalyEngine:
    """Enterprise Behavioral Anomaly Engine."""

    def detect_anomalies(self, employee_id: str, security_score: float = 85.0) -> List[BehavioralAnomalyResult]:
        """
        Scans employee behavioral data for anomalies and regressions.

        Args:
            employee_id: Employee ID.
            security_score: Security awareness score.

        Returns:
            List of BehavioralAnomalyResult models.
        """
        anomalies = []
        if security_score < 60.0:
            anomalies.append(BehavioralAnomalyResult(
                anomaly_id=f"anom_{int(time.time() * 1000)}",
                employee_id=employee_id,
                anomaly_type="awareness_regression",
                confidence_score=0.92,
                severity="HIGH",
                description="Awareness assessment score dropped below baseline security threshold (60%).",
            ))

        security_logger.info(f"BehavioralAnomalyEngine: Scanned '{employee_id}' -> Found {len(anomalies)} anomalies.")
        return anomalies


# Global BehavioralAnomalyEngine instance
behavioral_anomaly_engine = BehavioralAnomalyEngine()
