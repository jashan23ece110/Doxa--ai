"""
Request Logging Middleware for API Performance Monitoring.
"""

import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Logs incoming API request paths, HTTP methods, and execution latency."""

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000

        logger.info(
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Latency: {process_time:.2f}ms"
        )
        return response
