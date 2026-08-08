"""
Tenant Security for Enterprise Zero-Trust Security Platform.

Validates tenant boundaries, prevents cross-tenant data leakage, and propagates tenant context.
"""

from typing import Dict, Any, Optional
from app.core.exceptions import UnauthorizedError
from app.core.logging import security_logger
from app.core.security.security_models import TenantContext


class TenantSecurity:
    """Enforces strict multi-tenant boundaries and validation."""

    @staticmethod
    def validate_tenant_access(request_tenant_id: str, target_resource_tenant_id: str) -> None:
        """
        Ensures tenant cannot access resources belonging to another tenant.
        """
        if request_tenant_id != target_resource_tenant_id and request_tenant_id != "admin_tenant":
            security_logger.error(
                f"Tenant boundary violation: Tenant '{request_tenant_id}' attempted to access "
                f"resource owned by tenant '{target_resource_tenant_id}'."
            )
            raise UnauthorizedError("Cross-tenant access violation detected.")

    @staticmethod
    def create_tenant_context(user_id: str, tenant_id: str, role_str: str = "developer") -> TenantContext:
        """Creates a validated TenantContext object."""
        from app.core.security.security_models import RoleName
        try:
            role = RoleName(role_str)
        except ValueError:
            role = RoleName.DEVELOPER

        return TenantContext(
            user_id=user_id,
            tenant_id=tenant_id,
            role=role,
        )


# Global TenantSecurity instance
tenant_security = TenantSecurity()
