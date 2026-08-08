"""
Correlation ID, Performance Tracing, and Operational Metrics Middleware.

Generates or propagates unique request IDs (X-Request-ID) for end-to-end log correlation,
monitors request duration, logs slow endpoints, and records metrics.
"""

import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging import logger
from app.core.metrics import metrics_collector


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Trace requests with X-Request-ID, measure latency, and record operational metrics."""

    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.request_id = request_id

        start_time = time.time()
        response = await call_next(request)
        duration_ms = (time.time() - start_time) * 1000

        # Record HTTP metrics
        metrics_collector.record_http_request(response.status_code, duration_ms)

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time-MS"] = f"{duration_ms:.2f}"

        if duration_ms > 500:
            logger.warning(
                f"[SLOW ENDPOINT] {request.method} {request.url.path} "
                f"took {duration_ms:.2f}ms (ReqId: {request_id})"
            )

        return response
