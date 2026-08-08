"""
Thread-Safe In-Memory Operational Metrics Collector.

Tracks real-time performance indicators (API throughput, response latency, LLM provider metrics,
RAG retrieval time, tool execution counters, and document upload statistics).
"""

import threading
import time
from typing import Dict, Any, List


class MetricsCollector:
    """Thread-safe collector for internal operational metrics."""

    def __init__(self):
        self._lock = threading.Lock()
        self._http_requests_total: int = 0
        self._http_status_codes: Dict[int, int] = {}
        self._llm_calls_total: int = 0
        self._llm_errors_total: int = 0
        self._llm_latency_total_ms: float = 0.0
        self._vector_queries_total: int = 0
        self._vector_query_latency_total_ms: float = 0.0
        self._tool_executions_total: int = 0
        self._documents_uploaded_total: int = 0
        self._active_sse_connections: int = 0

    def record_http_request(self, status_code: int, duration_ms: float) -> None:
        """Records an HTTP request completion."""
        with self._lock:
            self._http_requests_total += 1
            self._http_status_codes[status_code] = self._http_status_codes.get(status_code, 0) + 1

    def record_llm_call(self, duration_ms: float, is_error: bool = False) -> None:
        """Records an LLM completion invocation."""
        with self._lock:
            self._llm_calls_total += 1
            self._llm_latency_total_ms += duration_ms
            if is_error:
                self._llm_errors_total += 1

    def record_vector_query(self, duration_ms: float) -> None:
        """Records a vector search query invocation."""
        with self._lock:
            self._vector_queries_total += 1
            self._vector_query_latency_total_ms += duration_ms

    def record_tool_execution(self) -> None:
        """Records a tool execution."""
        with self._lock:
            self._tool_executions_total += 1

    def record_document_upload(self) -> None:
        """Records a document upload."""
        with self._lock:
            self._documents_uploaded_total += 1

    def sse_connection_opened(self) -> None:
        """Increments active SSE connection count."""
        with self._lock:
            self._active_sse_connections += 1

    def sse_connection_closed(self) -> None:
        """Decrements active SSE connection count."""
        with self._lock:
            if self._active_sse_connections > 0:
                self._active_sse_connections -= 1

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Returns a snapshot summary of all aggregated operational metrics."""
        with self._lock:
            avg_llm_latency = (
                round(self._llm_latency_total_ms / self._llm_calls_total, 2)
                if self._llm_calls_total > 0
                else 0.0
            )
            avg_vector_latency = (
                round(self._vector_query_latency_total_ms / self._vector_queries_total, 2)
                if self._vector_queries_total > 0
                else 0.0
            )

            return {
                "http": {
                    "requests_total": self._http_requests_total,
                    "status_codes": dict(self._http_status_codes),
                },
                "llm": {
                    "calls_total": self._llm_calls_total,
                    "errors_total": self._llm_errors_total,
                    "avg_latency_ms": avg_llm_latency,
                },
                "vector_db": {
                    "queries_total": self._vector_queries_total,
                    "avg_latency_ms": avg_vector_latency,
                },
                "tools": {
                    "executions_total": self._tool_executions_total,
                },
                "documents": {
                    "uploads_total": self._documents_uploaded_total,
                },
                "streaming": {
                    "active_sse_connections": self._active_sse_connections,
                },
            }


# Global metrics collector instance
metrics_collector = MetricsCollector()
