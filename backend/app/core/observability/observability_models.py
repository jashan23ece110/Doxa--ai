"""
Observability Models for Enterprise Observability & Diagnostics Platform.

Defines Pydantic data models for TraceSpan, MetricRecord, HealthCheckStatus, AlertRecord,
DiagnosticReport, RecoveryResult, CapacityForecast, and DashboardSummary.
"""

import time
import uuid
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class HealthState(str, Enum):
    """Health check state enum."""

    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    OFFLINE = "offline"


class AlertSeverity(str, Enum):
    """Alert severity enum."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class TraceSpan(BaseModel):
    """OpenTelemetry-compatible distributed trace span."""

    span_id: str = Field(default_factory=lambda: f"span_{uuid.uuid4().hex[:8]}")
    trace_id: str
    parent_span_id: Optional[str] = None
    name: str
    component: str = "general"
    start_time: float = Field(default_factory=time.time)
    end_time: Optional[float] = None
    duration_ms: float = 0.0
    status: str = "ok"  # ok, error
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MetricRecord(BaseModel):
    """Single metric measurement record."""

    metric_name: str
    value: float
    unit: str = "ms"  # ms, bytes, count, percent
    labels: Dict[str, str] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=time.time)


class HealthCheckStatus(BaseModel):
    """Health check snapshot for a system component."""

    component_name: str
    state: HealthState = HealthState.HEALTHY
    latency_ms: float = 0.0
    error_message: Optional[str] = None
    last_check_time: float = Field(default_factory=time.time)


class AlertRecord(BaseModel):
    """Operational alert log entry."""

    alert_id: str = Field(default_factory=lambda: f"alt_{uuid.uuid4().hex[:8]}")
    title: str
    description: str
    severity: AlertSeverity = AlertSeverity.WARNING
    component: str
    timestamp: float = Field(default_factory=time.time)


class DiagnosticReport(BaseModel):
    """Root-cause diagnostic analysis report."""

    report_id: str = Field(default_factory=lambda: f"diag_{uuid.uuid4().hex[:8]}")
    primary_bottleneck: str
    root_cause_summary: str
    affected_components: List[str] = Field(default_factory=list)
    recommended_action: str
    timestamp: float = Field(default_factory=time.time)


class RecoveryResult(BaseModel):
    """Autonomous recovery attempt result."""

    recovery_id: str = Field(default_factory=lambda: f"rec_{uuid.uuid4().hex[:8]}")
    component_name: str
    action_taken: str
    success: bool = True
    message: str = "Successfully recovered component."
    timestamp: float = Field(default_factory=time.time)


class CapacityForecast(BaseModel):
    """Infrastructure capacity growth forecast."""

    forecast_id: str = Field(default_factory=lambda: f"cap_{uuid.uuid4().hex[:8]}")
    forecasted_cpu_usage_pct: float = 45.0
    forecasted_ram_mb: float = 1024.0
    recommended_worker_count: int = 16
    timestamp: float = Field(default_factory=time.time)


class DashboardSummary(BaseModel):
    """Aggregated dashboard telemetry overview."""

    system_status: HealthState = HealthState.HEALTHY
    p50_latency_ms: float = 0.0
    p90_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0
    healthy_components_count: int = 13
    total_alerts_count: int = 0
    active_traces_count: int = 0
    timestamp: float = Field(default_factory=time.time)
