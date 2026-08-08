"""
Security Models for Enterprise Zero-Trust AI Security Platform.

Defines Pydantic data models for Role, Permission, PolicyRule, APIKey, SecretRecord,
AuditRecord, SecurityEvent, ComplianceReport, and TenantContext.
"""

import time
import uuid
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class RoleName(str, Enum):
    """Enterprise RBAC Roles."""

    ADMIN = "admin"
    OWNER = "owner"
    DEVELOPER = "developer"
    OPERATOR = "operator"
    RESEARCHER = "researcher"
    VIEWER = "viewer"
    API_CLIENT = "api_client"


class ActionType(str, Enum):
    """Permission Action Types."""

    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"
    ALL = "*"


class Permission(BaseModel):
    """Resource permission specification."""

    resource: str
    action: str = "*"
    is_wildcard: bool = False


class Role(BaseModel):
    """RBAC Role definition."""

    name: RoleName
    description: str
    permissions: List[Permission] = Field(default_factory=list)
    inherited_roles: List[RoleName] = Field(default_factory=list)


class PolicyRule(BaseModel):
    """Authorization Policy Engine Rule."""

    rule_id: str = Field(default_factory=lambda: f"rule_{uuid.uuid4().hex[:8]}")
    name: str
    effect: str = "allow"  # allow, deny
    resource_pattern: str = "*"
    allowed_roles: List[RoleName] = Field(default_factory=list)
    allowed_tenants: List[str] = Field(default_factory=list)
    priority: int = 100
    enabled: bool = True


class APIKey(BaseModel):
    """Hashed Enterprise API Key record."""

    key_id: str = Field(default_factory=lambda: f"key_{uuid.uuid4().hex[:8]}")
    key_hash: str
    owner_id: str
    tenant_id: str = "default_tenant"
    scopes: List[str] = Field(default_factory=list)
    rate_plan: str = "enterprise_standard"
    expires_at: Optional[float] = None
    created_at: float = Field(default_factory=time.time)
    is_revoked: bool = False


class SecretRecord(BaseModel):
    """Encrypted secret manager record."""

    secret_id: str
    encrypted_value: str
    version: int = 1
    updated_at: float = Field(default_factory=time.time)


class AuditRecord(BaseModel):
    """Immutable security audit log entry."""

    audit_id: str = Field(default_factory=lambda: f"aud_{uuid.uuid4().hex[:12]}")
    timestamp: float = Field(default_factory=time.time)
    user_id: str
    tenant_id: str
    resource: str
    action: str
    result: str = "success"  # success, denied, error
    ip_address: Optional[str] = "127.0.0.1"
    request_id: Optional[str] = None
    trace_id: Optional[str] = None
    details: Dict[str, Any] = Field(default_factory=dict)


class SecurityEvent(BaseModel):
    """Security event record."""

    event_id: str = Field(default_factory=lambda: f"sevent_{uuid.uuid4().hex[:8]}")
    event_type: str  # LOGIN, LOGOUT, ACCESS_DENIED, SECRET_ROTATED, etc.
    user_id: str = "system"
    tenant_id: str = "default_tenant"
    timestamp: float = Field(default_factory=time.time)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ComplianceReport(BaseModel):
    """Compliance audit readiness report."""

    report_id: str = Field(default_factory=lambda: f"comp_{uuid.uuid4().hex[:8]}")
    standard: str  # GDPR, SOC2, ISO27001, HIPAA
    status: str = "COMPLIANT"
    total_audit_records: int
    access_violations_count: int
    generated_at: float = Field(default_factory=time.time)


class TenantContext(BaseModel):
    """Tenant isolation context."""

    tenant_id: str = "default_tenant"
    user_id: str = "default_user"
    role: RoleName = RoleName.DEVELOPER
