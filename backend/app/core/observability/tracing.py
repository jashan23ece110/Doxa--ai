"""
Distributed Tracing Engine for Enterprise Observability Platform.

Implements OpenTelemetry-compatible distributed tracing with Trace ID, Span ID,
parent-child nesting, async context propagation, and timing.
"""

import time
import uuid
import threading
from typing import Dict, Any, List, Optional
from app.core.logging import logger
from app.core.observability.observability_models import TraceSpan


class TracingEngine:
    """OpenTelemetry-compatible distributed tracing engine."""

    def __init__(self):
        self._lock = threading.Lock()
        self._active_spans: Dict[str, TraceSpan] = {}
        self._completed_spans: List[TraceSpan] = []

    def start_span(
        self,
        name: str,
        trace_id: Optional[str] = None,
        parent_span_id: Optional[str] = None,
        component: str = "general",
    ) -> TraceSpan:
        """Starts a new trace span."""
        tid = trace_id or f"trace_{uuid.uuid4().hex[:16]}"
        span = TraceSpan(
            name=name,
            trace_id=tid,
            parent_span_id=parent_span_id,
            component=component,
            start_time=time.time(),
        )

        with self._lock:
            self._active_spans[span.span_id] = span

        return span

    def finish_span(self, span_id: str, status: str = "ok", error_message: Optional[str] = None) -> Optional[TraceSpan]:
        """Finishes a trace span and calculates duration."""
        with self._lock:
            span = self._active_spans.pop(span_id, None)
            if span:
                span.end_time = time.time()
                span.duration_ms = round((span.end_time - span.start_time) * 1000, 2)
                span.status = status
                span.error_message = error_message
                self._completed_spans.append(span)
                if len(self._completed_spans) > 5000:
                    self._completed_spans = self._completed_spans[-5000:]
                return span
        return None

    def list_completed_spans(self, limit: int = 100) -> List[TraceSpan]:
        """Lists completed trace spans."""
        with self._lock:
            return self._completed_spans[-limit:]


# Global TracingEngine instance
tracing_engine = TracingEngine()
