"""
Security Context Middleware for Enterprise Zero-Trust Security Platform.

Injects Request ID, Tenant Context, User Context, Permission Context, and Security Context
into FastAPI request processing loops.
"""

import uuid
from typing import Dict, Any
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from app.core.security.tenant_security import tenant_security


class SecurityContextMiddleware(BaseHTTPMiddleware):
    """Injects Request ID, Tenant Context, and User Context into request scope."""

    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-ID") or f"req_{uuid.uuid4().hex[:12]}"
        tenant_id = request.headers.get("X-Tenant-ID", "default_tenant")
        user_id = request.headers.get("X-User-ID", "default_user")
        role_str = request.headers.get("X-User-Role", "developer")

        # Create tenant context
        context = tenant_security.create_tenant_context(user_id, tenant_id, role_str)
        request.state.security_context = context
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
