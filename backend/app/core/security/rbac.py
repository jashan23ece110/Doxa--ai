"""
RBAC Engine for Enterprise Zero-Trust Security Platform.

Manages 7 enterprise roles (Admin, Owner, Developer, Operator, Researcher, Viewer, API Client),
wildcard permissions, role inheritance, and permission resolution caching.
"""

import threading
from typing import Dict, Any, List, Optional
from app.core.logging import security_logger
from app.core.security.security_metrics import security_metrics_tracker
from app.core.security.security_models import Permission, Role, RoleName


class RBACEngine:
    """Enterprise Role-Based Access Control authorization engine."""

    def __init__(self):
        self._lock = threading.Lock()
        self._roles: Dict[RoleName, Role] = {}
        self._cache: Dict[str, bool] = {}
        self._setup_default_roles()

    def _setup_default_roles(self) -> None:
        """Initializes the 7 default enterprise roles and permissions."""
        # 1. Admin: Full wildcard access
        self._roles[RoleName.ADMIN] = Role(
            name=RoleName.ADMIN,
            description="Full system administrator",
            permissions=[Permission(resource="*", action="*", is_wildcard=True)],
        )

        # 2. Owner: Full resource ownership
        self._roles[RoleName.OWNER] = Role(
            name=RoleName.OWNER,
            description="Tenant system owner",
            permissions=[Permission(resource="*", action="*", is_wildcard=True)],
        )

        # 3. Developer: Workflows, agents, RAG, and tools
        self._roles[RoleName.DEVELOPER] = Role(
            name=RoleName.DEVELOPER,
            description="Developer access to APIs and tools",
            permissions=[
                Permission(resource="workflows", action="*"),
                Permission(resource="agents", action="*"),
                Permission(resource="rag", action="*"),
                Permission(resource="tools", action="*"),
            ],
        )

        # 4. Operator: Workflow and agent execution
        self._roles[RoleName.OPERATOR] = Role(
            name=RoleName.OPERATOR,
            description="Operator access for workflow execution",
            permissions=[
                Permission(resource="workflows", action="execute"),
                Permission(resource="agents", action="execute"),
            ],
        )

        # 5. Researcher: RAG and evaluation platform
        self._roles[RoleName.RESEARCHER] = Role(
            name=RoleName.RESEARCHER,
            description="Research access to documents and eval",
            permissions=[
                Permission(resource="rag", action="read"),
                Permission(resource="eval", action="read"),
            ],
        )

        # 6. Viewer: Read-only access
        self._roles[RoleName.VIEWER] = Role(
            name=RoleName.VIEWER,
            description="Read-only system viewer",
            permissions=[Permission(resource="*", action="read")],
        )

        # 7. API Client: Service account API access
        self._roles[RoleName.API_CLIENT] = Role(
            name=RoleName.API_CLIENT,
            description="Automated API service client",
            permissions=[
                Permission(resource="api", action="execute"),
                Permission(resource="workflows", action="execute"),
            ],
        )

    def has_permission(self, role_name: RoleName, resource: str, action: str = "read") -> bool:
        """
        Checks if a role has permission for a specific resource and action.
        """
        cache_key = f"{role_name.value}:{resource}:{action}"
        with self._lock:
            if cache_key in self._cache:
                security_metrics_tracker.record_rbac_cache(hit=True)
                return self._cache[cache_key]

            security_metrics_tracker.record_rbac_cache(hit=False)
            role = self._roles.get(role_name)
            if not role:
                self._cache[cache_key] = False
                return False

            allowed = False
            for perm in role.permissions:
                if perm.is_wildcard or perm.resource == "*":
                    allowed = True
                    break
                if perm.resource == resource and (perm.action in ("*", action)):
                    allowed = True
                    break

            self._cache[cache_key] = allowed
            return allowed


# Global RBACEngine instance
rbac_engine = RBACEngine()
