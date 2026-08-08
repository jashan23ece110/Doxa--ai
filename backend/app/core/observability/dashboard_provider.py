"""
Dashboard Data Provider for Enterprise Observability Platform.

Aggregates system overview, latency percentiles, health states, alert volumes, metrics,
and provider statistics for operational monitoring dashboards.
"""

from app.core.observability.alert_engine import alert_engine
from app.core.observability.health_monitor import health_monitor
from app.core.observability.metrics_engine import metrics_engine
from app.core.observability.observability_models import DashboardSummary, HealthState
from app.core.observability.tracing import tracing_engine


class DashboardProvider:
    """Aggregates telemetry data for operational dashboards."""

    @staticmethod
    def get_dashboard_summary() -> DashboardSummary:
        """Aggregates system overview statistics."""
        percentiles = metrics_engine.get_percentiles()
        health_statuses = health_monitor.check_all_components()
        alerts = alert_engine.list_alerts()
        spans = tracing_engine.list_completed_spans()

        healthy_count = sum(1 for h in health_statuses if h.state == HealthState.HEALTHY)

        return DashboardSummary(
            system_status=HealthState.HEALTHY if healthy_count == len(health_statuses) else HealthState.WARNING,
            p50_latency_ms=percentiles.get("p50", 0.0),
            p90_latency_ms=percentiles.get("p90", 0.0),
            p95_latency_ms=percentiles.get("p95", 0.0),
            p99_latency_ms=percentiles.get("p99", 0.0),
            healthy_components_count=healthy_count,
            total_alerts_count=len(alerts),
            active_traces_count=len(spans),
        )


# Global DashboardProvider instance
dashboard_provider = DashboardProvider()
