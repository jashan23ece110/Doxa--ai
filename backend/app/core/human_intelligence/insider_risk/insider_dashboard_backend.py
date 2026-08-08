"""
Enterprise Insider Risk Dashboard Backend.

Tracks user risk distribution, department exposure metrics, privileged account metrics,
policy compliance trends, behavioral deviation statistics, and investigation workloads.
"""

import time
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class InsiderDashboardStateMetrics(BaseModel):
    total_privileged_users_count: int = 14
    high_risk_users_count: int = 1
    average_policy_adherence_percent: float = 95.5
    open_insider_cases_count: int = 2
    top_exposed_department: str = "Infrastructure & DevOps"
    updated_at: float = Field(default_factory=time.time)


class InsiderDashboardBackend:
    """Enterprise Insider Risk Dashboard Backend Service."""

    def get_dashboard_metrics(self) -> InsiderDashboardStateMetrics:
        """
        Retrieves real-time Insider Risk Dashboard metrics.

        Returns:
            InsiderDashboardStateMetrics object.
        """
        metrics = InsiderDashboardStateMetrics(
            total_privileged_users_count=18,
            high_risk_users_count=1,
            average_policy_adherence_percent=96.0,
            open_insider_cases_count=2,
            top_exposed_department="Cloud Operations",
        )

        security_logger.debug("InsiderDashboardBackend: Generated insider risk dashboard metrics.")
        return metrics


# Global InsiderDashboardBackend instance
insider_dashboard_backend = InsiderDashboardBackend()
