"""
Policy Engine for Enterprise Zero-Trust Security Platform.

Evaluates fine-grained ALLOW/DENY authorization rules with priority ordering and conflict resolution.
"""

from typing import Dict, Any, List
from app.core.logging import security_logger
from app.core.security.rbac import rbac_engine
from app.core.security.security_metrics import security_metrics_tracker
from app.core.security.security_models import PolicyRule, RoleName, TenantContext


class PolicyEngine:
    """Enterprise policy engine for request authorization."""

    def __init__(self):
        self._rules: List[PolicyRule] = []

    def add_rule(self, rule: PolicyRule) -> None:
        """Adds a policy rule and sorts by priority."""
        self._rules.append(rule)
        self._rules.sort(key=lambda r: r.priority, reverse=True)

    def evaluate_request(
        self,
        context: TenantContext,
        resource: str,
        action: str = "read",
    ) -> bool:
        """
        Evaluates policy rules and RBAC permissions. Explicit DENY overrides ALLOW.
        """
        # 1. Check explicit policy rules
        for rule in self._rules:
            if not rule.enabled:
                continue

            if rule.resource_pattern in ("*", resource):
                if rule.allowed_roles and context.role not in rule.allowed_roles:
                    continue
                if rule.allowed_tenants and context.tenant_id not in rule.allowed_tenants:
                    continue

                if rule.effect == "deny":
                    security_logger.warning(f"PolicyEngine DENIED access for user '{context.user_id}' to '{resource}'.")
                    security_metrics_tracker.record_denied_request()
                    return False
                elif rule.effect == "allow":
                    return True

        # 2. Fallback to RBAC engine
        allowed = rbac_engine.has_permission(context.role, resource, action)
        if not allowed:
            security_logger.warning(f"RBAC DENIED access for user '{context.user_id}' (Role: {context.role.value}) to '{resource}'.")
            security_metrics_tracker.record_denied_request()

        return allowed


# Global PolicyEngine instance
policy_engine = PolicyEngine()
