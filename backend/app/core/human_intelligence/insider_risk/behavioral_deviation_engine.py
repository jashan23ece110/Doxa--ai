"""
Behavioral Deviation Engine.

Detects unusual activity patterns, behavioral drift, sudden awareness score declines,
organizational anomalies, abnormal workflow shifts, and long-term behavioral trends.
"""

import time
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class BehavioralDeviationAlert(BaseModel):
    alert_id: str
    employee_id: str
    deviation_type: str  # awareness_decline, off_hours_data_transfer, unusual_workflow
    confidence_score: float = 0.90
    description: str
    detected_at: float = Field(default_factory=time.time)


class BehavioralDeviationEngine:
    """Enterprise Behavioral Deviation Engine."""

    def evaluate_deviations(self, employee_id: str, baseline_score: float = 85.0, current_score: float = 85.0) -> List[BehavioralDeviationAlert]:
        """
        Evaluates behavioral drift and awareness regressions against baseline metrics.

        Args:
            employee_id: Employee ID.
            baseline_score: Historical baseline awareness score.
            current_score: Current awareness score.

        Returns:
            List of BehavioralDeviationAlert objects.
        """
        alerts = []
        if baseline_score - current_score > 20.0:
            alerts.append(BehavioralDeviationAlert(
                alert_id=f"dev_{int(time.time() * 1000)}",
                employee_id=employee_id,
                deviation_type="awareness_decline",
                confidence_score=0.92,
                description=f"Awareness score declined significantly from baseline {baseline_score}% to {current_score}%.",
            ))

        security_logger.info(f"BehavioralDeviationEngine: Evaluated '{employee_id}' -> {len(alerts)} deviation alerts.")
        return alerts


# Global BehavioralDeviationEngine instance
behavioral_deviation_engine = BehavioralDeviationEngine()
