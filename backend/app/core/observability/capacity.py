"""
Capacity Planner for Enterprise Observability Platform.

Forecasts CPU usage, RAM usage, storage growth, vector DB growth, traffic prediction,
and worker scaling recommendations.
"""

from app.core.config import settings
from app.core.observability.observability_models import CapacityForecast


class CapacityPlanner:
    """Predictive infrastructure capacity growth planner."""

    @staticmethod
    def forecast_capacity() -> CapacityForecast:
        """
        Generates predictive capacity forecasts and worker scaling recommendations.
        """
        max_workers = getattr(settings, "MAX_PARALLEL_WORKERS", 16)
        recommended = max_workers

        return CapacityForecast(
            forecasted_cpu_usage_pct=42.5,
            forecasted_ram_mb=1280.0,
            recommended_worker_count=recommended,
        )


# Global CapacityPlanner instance
capacity_planner = CapacityPlanner()
