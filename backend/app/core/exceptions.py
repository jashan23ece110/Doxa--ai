"""
Custom Exception Classes and Standardized Global Exception Handlers.

Provides domain exceptions and maps them to clean, consistent JSON error responses:
{
    "error": "Human readable message",
    "code": "ERROR_CODE",
    "timestamp": "ISO timestamp",
    "request_id": "UUID",
    "status_code": 400
}
"""

from datetime import datetime, timezone
from typing import Any, Dict, Optional
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.core.logging import logger, security_logger


class DoxaException(Exception):
    """Base exception for all Doxa domain errors."""

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}


class NotFoundError(DoxaException):
    """Raised when a requested resource is not found."""

    def __init__(self, message: str = "Resource not found", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND, details=details)


class BadRequestError(DoxaException):
    """Raised when request payload or parameters are invalid."""

    def __init__(self, message: str = "Invalid request", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="BAD_REQUEST", status_code=status.HTTP_400_BAD_REQUEST, details=details)


class UnauthorizedError(DoxaException):
    """Raised when authentication or authorization check fails."""

    def __init__(self, message: str = "Unauthorized access", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="UNAUTHORIZED", status_code=status.HTTP_401_UNAUTHORIZED, details=details)


class PayloadTooLargeError(DoxaException):
    """Raised when uploaded file or request body exceeds limit."""

    def __init__(self, message: str = "Payload size exceeds maximum allowed limit", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="PAYLOAD_TOO_LARGE", status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, details=details)


class RateLimitError(DoxaException):
    """Raised when rate limit is hit."""

    def __init__(self, message: str = "Rate limit exceeded. Please try again shortly.", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="RATE_LIMIT_EXCEEDED", status_code=status.HTTP_429_TOO_MANY_REQUESTS, details=details)


class PromptInjectionError(DoxaException):
    """Raised when malicious prompt injection pattern is detected."""

    def __init__(self, message: str = "Security Violation: Malicious instruction sequence detected.", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="PROMPT_INJECTION_DETECTED", status_code=status.HTTP_400_BAD_REQUEST, details=details)


class ExternalServiceError(DoxaException):
    """Raised when an external API or service fails."""

    def __init__(self, message: str = "External service error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="EXTERNAL_SERVICE_ERROR", status_code=status.HTTP_502_BAD_GATEWAY, details=details)


def register_exception_handlers(app: FastAPI) -> None:
    """Registers global exception handlers returning standardized error payloads."""

    @app.exception_handler(DoxaException)
    async def doxa_exception_handler(request: Request, exc: DoxaException) -> JSONResponse:
        request_id = getattr(request.state, "request_id", "N/A")
        logger.warning(f"Domain exception [{exc.code}] on {request.url.path}: {exc.message} (ReqId: {request_id})")

        if isinstance(exc, PromptInjectionError):
            security_logger.warning(f"[SECURITY EVENT] Prompt injection blocked on {request.url.path} (ReqId: {request_id})")

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.message,
                "code": exc.code,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "request_id": request_id,
                "status_code": exc.status_code,
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        request_id = getattr(request.state, "request_id", "N/A")
        logger.error(f"Unhandled system exception on {request.url.path}: {exc} (ReqId: {request_id})", exc_info=True)

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "An unexpected internal server error occurred.",
                "code": "INTERNAL_SERVER_ERROR",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "request_id": request_id,
                "status_code": 500,
            },
        )
