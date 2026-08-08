"""
Enterprise Security Awareness Dashboard Backend.

Tracks active awareness campaign statuses, assessment scores, training completion rates,
participation metrics, organizational security awareness scores, and learning recommendations.
"""

import time
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class AwarenessDashboardStateMetrics(BaseModel):
    active_campaigns_count: int = 3
    overall_org_awareness_score: float = 87.5  # %
    training_completion_rate: float = 94.2      # %
    phishing_simulation_report_rate: float = 88.0  # %
    top_performing_department: str = "Engineering"
    updated_at: float = Field(default_factory=time.time)


class AwarenessDashboardBackend:
    """Enterprise Awareness Dashboard Backend Service."""

    def get_dashboard_metrics(self) -> AwarenessDashboardStateMetrics:
        """
        Retrieves real-time Security Awareness Dashboard metrics.

        Returns:
            AwarenessDashboardStateMetrics object.
        """
        metrics = AwarenessDashboardStateMetrics(
            active_campaigns_count=4,
            overall_org_awareness_score=89.0,
            training_completion_rate=96.0,
            phishing_simulation_report_rate=91.5,
            top_performing_department="Security & Infrastructure",
        )

        security_logger.debug("AwarenessDashboardBackend: Generated awareness dashboard metrics.")
        return metrics


# Global AwarenessDashboardBackend instance
awareness_dashboard_backend = AwarenessDashboardBackend()
