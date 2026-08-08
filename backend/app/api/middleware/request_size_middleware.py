"""
Request Payload Body Size Limit Middleware.

Enforces MAX_REQUEST_BODY_SIZE caps on non-upload HTTP requests, rejecting oversized
payloads with HTTP 413 Payload Too Large before processing.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from app.core.logging import security_logger


class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    """Enforces body size limits on standard HTTP requests."""

    async def dispatch(self, request: Request, call_next):
        # Multipart uploads handle their own chunked validation in document_service
        if request.headers.get("content-type", "").startswith("multipart/form-data"):
            return await call_next(request)

        content_length = request.headers.get("content-length")
        if content_length:
            try:
                length_bytes = int(content_length)
                if length_bytes > settings.MAX_REQUEST_BODY_SIZE:
                    max_mb = settings.MAX_REQUEST_BODY_SIZE // (1024 * 1024)
                    request_id = getattr(request.state, "request_id", "N/A")
                    security_logger.warning(
                        f"[PAYLOAD BLOCKED] {request.method} {request.url.path} "
                        f"content-length {length_bytes} bytes exceeds {max_mb}MB limit (ReqId: {request_id})"
                    )
                    return JSONResponse(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        content={
                            "error": f"Request body payload size exceeds limit of {max_mb}MB.",
                            "code": "PAYLOAD_TOO_LARGE",
                            "status_code": status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        },
                    )
            except ValueError:
                pass

        return await call_next(request)
