"""
Diagnostics Spans and Performance Instrumentation Module.

Provides context managers for timing spans across repositories, LLM calls, and tools.
"""

import time
from typing import Optional
from app.core.logging import logger
from app.core.metrics import metrics_collector


class DiagnosticSpan:
    """Context manager for instrumenting diagnostic execution spans."""

    def __init__(self, span_name: str, slow_threshold_ms: float = 500.0, category: str = "general"):
        self.span_name = span_name
        self.slow_threshold_ms = slow_threshold_ms
        self.category = category
        self.start_time: float = 0.0
        self.duration_ms: float = 0.0

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.duration_ms = (time.time() - self.start_time) * 1000

        if self.category == "llm":
            metrics_collector.record_llm_call(self.duration_ms, is_error=(exc_type is not None))
        elif self.category == "vector":
            metrics_collector.record_vector_query(self.duration_ms)
        elif self.category == "tool":
            metrics_collector.record_tool_execution()

        if self.duration_ms > self.slow_threshold_ms:
            logger.warning(
                f"[DIAGNOSTIC SPAN] '{self.span_name}' ({self.category}) "
                f"took {self.duration_ms:.2f}ms (> {self.slow_threshold_ms}ms threshold)"
            )
