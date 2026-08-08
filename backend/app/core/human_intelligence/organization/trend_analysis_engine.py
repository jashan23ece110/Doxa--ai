"""
Enterprise Trend Analytics Engine.

Tracks security awareness evolution, organizational maturity growth, resilience progression,
learning effectiveness trends, and enterprise intelligence KPIs over time.
"""

import time
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class TrendSnapshot(BaseModel):
    metric_name: str
    historical_value: float
    current_value: float
    percentage_change: float
    trend_direction: str = "IMPROVING"  # IMPROVING, STABLE, DECLINING
    measured_at: float = Field(default_factory=time.time)


class TrendAnalysisEngine:
    """Enterprise Trend Analytics Engine."""

    def analyze_trend(self, metric_name: str, historical: float = 80.0, current: float = 89.0) -> TrendSnapshot:
        """
        Analyzes historical vs current metric trend evolution.

        Args:
            metric_name: Name of metric.
            historical: Historical baseline value.
            current: Current value.

        Returns:
            TrendSnapshot model.
        """
        change = round(((current - historical) / historical) * 100.0, 1)
        direction = "IMPROVING" if change > 0 else ("STABLE" if change == 0 else "DECLINING")

        snapshot = TrendSnapshot(
            metric_name=metric_name,
            historical_value=historical,
            current_value=current,
            percentage_change=change,
            trend_direction=direction,
        )

        security_logger.info(f"TrendAnalysisEngine: Analyzed trend for '{metric_name}': Change=+{change}%, Direction={direction}.")
        return snapshot


# Global TrendAnalysisEngine instance
trend_analysis_engine = TrendAnalysisEngine()
