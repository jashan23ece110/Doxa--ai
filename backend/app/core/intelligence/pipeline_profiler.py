"""
Pipeline Profiler for Doxa AI Operating System.

Measures fine-grained component latency, worker/queue delays, token consumption,
RAM memory utilization, and cost estimations to generate complete execution traces.
"""

import threading
import time
from typing import Dict, Any, List, Optional
from app.core.logging import logger
from app.core.config import settings
from app.core.intelligence.intelligence_types import (
    ComponentLatencyTrace,
    PipelineTrace,
)


class PipelineProfiler:
    """Enterprise Pipeline Profiler for end-to-end telemetry and tracing."""

    def __init__(self):
        self._lock = threading.Lock()
        self._completed_traces: List[PipelineTrace] = []

    def start_trace(self, request_id: str = "req_default") -> PipelineTrace:
        """Initializes a new PipelineTrace."""
        return PipelineTrace(
            request_id=request_id,
            started_at=time.time(),
        )

    def record_component_latency(
        self,
        trace: PipelineTrace,
        component_name: str,
        duration_ms: float,
        tokens_consumed: int = 0,
        memory_used_mb: float = 0.0,
        estimated_cost_usd: float = 0.0,
        success: bool = True,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Appends a ComponentLatencyTrace to the pipeline trace.

        Args:
            trace: Active PipelineTrace.
            component_name: Name of subsystem ('pipeline', 'tool', 'planner', 'reasoning', 'memory', 'retrieval', 'cross_encoder', 'worker', 'queue').
            duration_ms: Latency duration in milliseconds.
            tokens_consumed: Tokens processed.
            memory_used_mb: Memory footprint MB.
            estimated_cost_usd: Cost estimation USD.
            success: Execution outcome boolean.
            metadata: Custom details.
        """
        if not settings.PIPELINE_PROFILER_ENABLED:
            return

        now = time.time()
        comp_trace = ComponentLatencyTrace(
            component_name=component_name,
            duration_ms=round(duration_ms, 2),
            start_time=now - (duration_ms / 1000.0),
            end_time=now,
            tokens_consumed=tokens_consumed,
            memory_used_mb=memory_used_mb,
            estimated_cost_usd=estimated_cost_usd,
            success=success,
            metadata=metadata or {},
        )

        trace.component_traces.append(comp_trace)
        trace.total_tokens += tokens_consumed
        trace.total_cost_usd += estimated_cost_usd

    def finalize_trace(
        self,
        trace: PipelineTrace,
        cache_hits: int = 0,
        cache_misses: int = 0,
    ) -> PipelineTrace:
        """
        Finalizes the pipeline trace with overall duration and stores in memory.
        """
        trace.completed_at = time.time()
        trace.total_duration_ms = round((trace.completed_at - trace.started_at) * 1000.0, 2)
        trace.cache_hits = cache_hits
        trace.cache_misses = cache_misses

        if settings.PIPELINE_PROFILER_ENABLED:
            with self._lock:
                self._completed_traces.append(trace)
                if len(self._completed_traces) > 1000:
                    self._completed_traces = self._completed_traces[-800:]

        logger.info(
            f"PipelineProfiler trace '{trace.trace_id}': Request={trace.request_id}, "
            f"TotalDuration={trace.total_duration_ms:.1f}ms, Components={len(trace.component_traces)}, "
            f"Tokens={trace.total_tokens}, Cost=${trace.total_cost_usd:.6f}"
        )

        return trace

    def get_average_latency_ms(self) -> float:
        """Calculates rolling average pipeline latency in milliseconds."""
        with self._lock:
            if not self._completed_traces:
                return 0.0
            recent = self._completed_traces[-100:]
            return round(sum(t.total_duration_ms for t in recent) / len(recent), 2)

    def get_token_consumption_rate(self) -> float:
        """Calculates recent token consumption rate (tokens per second)."""
        with self._lock:
            if not self._completed_traces:
                return 0.0
            recent = self._completed_traces[-50:]
            total_time_s = sum(t.total_duration_ms for t in recent) / 1000.0
            if total_time_s == 0:
                return 0.0
            total_tokens = sum(t.total_tokens for t in recent)
            return round(total_tokens / total_time_s, 2)

    def get_recent_traces(self, limit: int = 50) -> List[PipelineTrace]:
        """Returns the most recent pipeline traces."""
        with self._lock:
            return list(self._completed_traces[-limit:])


# Global PipelineProfiler instance
pipeline_profiler = PipelineProfiler()
