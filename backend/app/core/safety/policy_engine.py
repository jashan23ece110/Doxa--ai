"""
Enterprise AI Safety Policy Engine.

Dynamically evaluates ALLOW / DENY / CONDITIONAL rules across tool, memory,
RAG, execution, model, agent, workflow, plugin, and MCP scopes.

Supports role-based, tenant-based, time-based, and risk-threshold-based conditions.
"""

import asyncio
import time
import threading
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from app.core.logging import logger
from app.core.config import settings
from app.core.safety.safety_types import (
    SafetyPolicy,
    SafetyRule,
    PolicyScope,
    PolicyEffect,
    PolicyViolation,
    RiskLevel,
)


class SafetyPolicyEngine:
    """Enterprise-grade dynamic policy engine for AI Safety layer."""

    def __init__(self):
        self._lock = threading.Lock()
        self._policies: Dict[str, SafetyPolicy] = {}
        self._register_default_policies()

    def _register_default_policies(self) -> None:
        """Registers built-in enterprise-grade policies."""
        # ── Tool Execution Policies ──
        tool_policy = SafetyPolicy(
            name="Default Tool Execution Policy",
            scope=PolicyScope.TOOL,
            rules=[
                SafetyRule(
                    name="deny_dangerous_tools",
                    scope=PolicyScope.TOOL,
                    effect=PolicyEffect.DENY,
                    resource_pattern="shell_execute|system_command|os_exec|raw_sql",
                    conditions={"require_admin": True},
                    priority=1000,
                    description="Blocks direct shell/system/raw-SQL tool invocation for non-admin actors.",
                ),
                SafetyRule(
                    name="allow_standard_tools",
                    scope=PolicyScope.TOOL,
                    effect=PolicyEffect.ALLOW,
                    resource_pattern="*",
                    conditions={},
                    priority=10,
                    description="Default ALLOW for all non-restricted tools.",
                ),
            ],
        )
        # ── Memory Access Policies ──
        memory_policy = SafetyPolicy(
            name="Default Memory Access Policy",
            scope=PolicyScope.MEMORY,
            rules=[
                SafetyRule(
                    name="deny_cross_tenant_memory",
                    scope=PolicyScope.MEMORY,
                    effect=PolicyEffect.DENY,
                    resource_pattern="*",
                    conditions={"require_same_tenant": True},
                    priority=900,
                    description="Prevents cross-tenant memory access.",
                ),
                SafetyRule(
                    name="allow_own_memory",
                    scope=PolicyScope.MEMORY,
                    effect=PolicyEffect.ALLOW,
                    resource_pattern="*",
                    conditions={},
                    priority=10,
                    description="Default ALLOW for same-tenant memory access.",
                ),
            ],
        )
        # ── RAG Retrieval Policies ──
        rag_policy = SafetyPolicy(
            name="Default RAG Retrieval Policy",
            scope=PolicyScope.RAG,
            rules=[
                SafetyRule(
                    name="conditional_low_confidence_rag",
                    scope=PolicyScope.RAG,
                    effect=PolicyEffect.CONDITIONAL,
                    resource_pattern="*",
                    conditions={"min_retrieval_confidence": 0.3},
                    priority=500,
                    description="Requires minimum retrieval confidence threshold.",
                ),
                SafetyRule(
                    name="allow_rag",
                    scope=PolicyScope.RAG,
                    effect=PolicyEffect.ALLOW,
                    resource_pattern="*",
                    conditions={},
                    priority=10,
                    description="Default ALLOW for retrieval operations.",
                ),
            ],
        )
        # ── Execution Policies ──
        exec_policy = SafetyPolicy(
            name="Default Execution Policy",
            scope=PolicyScope.EXECUTION,
            rules=[
                SafetyRule(
                    name="deny_high_risk_execution",
                    scope=PolicyScope.EXECUTION,
                    effect=PolicyEffect.DENY,
                    resource_pattern="*",
                    conditions={"max_risk_score": settings.RISK_THRESHOLD},
                    priority=800,
                    description="Blocks executions exceeding the configured risk threshold.",
                ),
                SafetyRule(
                    name="time_restricted_execution",
                    scope=PolicyScope.EXECUTION,
                    effect=PolicyEffect.CONDITIONAL,
                    resource_pattern="*",
                    conditions={"allowed_hours": [0, 23]},  # all hours
                    priority=100,
                    description="Time-window restriction for execution policies.",
                ),
                SafetyRule(
                    name="allow_execution",
                    scope=PolicyScope.EXECUTION,
                    effect=PolicyEffect.ALLOW,
                    resource_pattern="*",
                    conditions={},
                    priority=10,
                    description="Default ALLOW for standard execution.",
                ),
            ],
        )
        # ── Model Policies ──
        model_policy = SafetyPolicy(
            name="Default Model Policy",
            scope=PolicyScope.MODEL,
            rules=[
                SafetyRule(
                    name="deny_blacklisted_models",
                    scope=PolicyScope.MODEL,
                    effect=PolicyEffect.DENY,
                    resource_pattern="gpt-4-unsafe|uncensored*",
                    conditions={},
                    priority=900,
                    description="Denies access to blacklisted or unsafe models.",
                ),
                SafetyRule(
                    name="allow_models",
                    scope=PolicyScope.MODEL,
                    effect=PolicyEffect.ALLOW,
                    resource_pattern="*",
                    conditions={},
                    priority=10,
                    description="Default ALLOW for approved models.",
                ),
            ],
        )
        # ── Agent Policies ──
        agent_policy = SafetyPolicy(
            name="Default Agent Policy",
            scope=PolicyScope.AGENT,
            rules=[
                SafetyRule(
                    name="deny_excessive_agent_spawning",
                    scope=PolicyScope.AGENT,
                    effect=PolicyEffect.DENY,
                    resource_pattern="*",
                    conditions={"max_concurrent_agents": settings.MAX_ACTIVE_AGENTS},
                    priority=700,
                    description="Prevents excessive concurrent agent creation.",
                ),
                SafetyRule(
                    name="allow_agents",
                    scope=PolicyScope.AGENT,
                    effect=PolicyEffect.ALLOW,
                    resource_pattern="*",
                    conditions={},
                    priority=10,
                    description="Default ALLOW for agent operations.",
                ),
            ],
        )
        # ── Workflow Policies ──
        workflow_policy = SafetyPolicy(
            name="Default Workflow Policy",
            scope=PolicyScope.WORKFLOW,
            rules=[
                SafetyRule(
                    name="allow_workflows",
                    scope=PolicyScope.WORKFLOW,
                    effect=PolicyEffect.ALLOW,
                    resource_pattern="*",
                    conditions={},
                    priority=10,
                    description="Default ALLOW for workflow execution.",
                ),
            ],
        )
        # ── Plugin / MCP Policies ──
        plugin_policy = SafetyPolicy(
            name="Default Plugin Policy",
            scope=PolicyScope.PLUGIN,
            rules=[
                SafetyRule(
                    name="conditional_plugin_execution",
                    scope=PolicyScope.PLUGIN,
                    effect=PolicyEffect.CONDITIONAL,
                    resource_pattern="*",
                    conditions={"require_signed": False},
                    priority=500,
                    description="Conditionally allows plugin execution based on signing status.",
                ),
                SafetyRule(
                    name="allow_plugins",
                    scope=PolicyScope.PLUGIN,
                    effect=PolicyEffect.ALLOW,
                    resource_pattern="*",
                    conditions={},
                    priority=10,
                    description="Default ALLOW for plugins.",
                ),
            ],
        )
        mcp_policy = SafetyPolicy(
            name="Default MCP Policy",
            scope=PolicyScope.MCP,
            rules=[
                SafetyRule(
                    name="allow_mcp",
                    scope=PolicyScope.MCP,
                    effect=PolicyEffect.ALLOW,
                    resource_pattern="*",
                    conditions={},
                    priority=10,
                    description="Default ALLOW for MCP execution.",
                ),
            ],
        )

        for policy in [
            tool_policy, memory_policy, rag_policy, exec_policy,
            model_policy, agent_policy, workflow_policy, plugin_policy, mcp_policy,
        ]:
            self._policies[policy.policy_id] = policy

    # ── Public API ──

    def add_policy(self, policy: SafetyPolicy) -> SafetyPolicy:
        """Registers a custom safety policy."""
        with self._lock:
            self._policies[policy.policy_id] = policy
        logger.info(f"SafetyPolicyEngine registered policy '{policy.name}' (scope={policy.scope.value}).")
        return policy

    def add_rule_to_scope(self, scope: PolicyScope, rule: SafetyRule) -> None:
        """Adds a rule to the first matching policy for the given scope."""
        with self._lock:
            for policy in self._policies.values():
                if policy.scope == scope:
                    policy.rules.append(rule)
                    policy.rules.sort(key=lambda r: r.priority, reverse=True)
                    return

    async def evaluate(
        self,
        scope: PolicyScope,
        resource: str,
        context: Dict[str, Any] = None,
    ) -> tuple:
        """
        Evaluates all rules for the given scope and resource.

        Args:
            scope: The policy scope to evaluate.
            resource: The resource identifier being accessed.
            context: Execution context dict with keys like role, tenant_id,
                     risk_score, current_agents, retrieval_confidence, etc.

        Returns:
            Tuple of (PolicyEffect, List[PolicyViolation]).
        """
        if not settings.POLICY_ENGINE_ENABLED:
            return PolicyEffect.ALLOW, []

        ctx = context or {}
        violations: List[PolicyViolation] = []

        with self._lock:
            matching_policies = [
                p for p in self._policies.values() if p.scope == scope
            ]

        for policy in matching_policies:
            sorted_rules = sorted(policy.rules, key=lambda r: r.priority, reverse=True)

            for rule in sorted_rules:
                if not rule.enabled:
                    continue

                if not self._resource_matches(rule.resource_pattern, resource):
                    continue

                condition_result = self._evaluate_conditions(rule, ctx)

                if rule.effect == PolicyEffect.DENY and condition_result:
                    violation = PolicyViolation(
                        rule_id=rule.rule_id,
                        rule_name=rule.name,
                        scope=scope,
                        effect=PolicyEffect.DENY,
                        actor_id=ctx.get("actor_id", "system"),
                        user_id=ctx.get("user_id", "anonymous"),
                        resource=resource,
                        reason=rule.description,
                        severity=RiskLevel.HIGH,
                    )
                    violations.append(violation)
                    logger.warning(
                        f"SafetyPolicyEngine DENY: rule='{rule.name}', "
                        f"resource='{resource}', scope={scope.value}"
                    )
                    return PolicyEffect.DENY, violations

                if rule.effect == PolicyEffect.CONDITIONAL and not condition_result:
                    violation = PolicyViolation(
                        rule_id=rule.rule_id,
                        rule_name=rule.name,
                        scope=scope,
                        effect=PolicyEffect.CONDITIONAL,
                        actor_id=ctx.get("actor_id", "system"),
                        user_id=ctx.get("user_id", "anonymous"),
                        resource=resource,
                        reason=f"Condition not met: {rule.description}",
                        severity=RiskLevel.MEDIUM,
                    )
                    violations.append(violation)

                if rule.effect == PolicyEffect.ALLOW and condition_result:
                    return PolicyEffect.ALLOW, violations

        # Default: allow if no explicit deny
        return PolicyEffect.ALLOW, violations

    # ── Internal Helpers ──

    @staticmethod
    def _resource_matches(pattern: str, resource: str) -> bool:
        """Checks if a resource matches a pattern (supports * and | separators)."""
        if pattern == "*":
            return True
        alternatives = [p.strip() for p in pattern.split("|")]
        for alt in alternatives:
            if alt.endswith("*"):
                if resource.startswith(alt[:-1]):
                    return True
            elif alt == resource:
                return True
        return False

    @staticmethod
    def _evaluate_conditions(rule: SafetyRule, ctx: Dict[str, Any]) -> bool:
        """Evaluates rule conditions against execution context."""
        conditions = rule.conditions
        if not conditions:
            return True

        # Role-based condition
        if "require_admin" in conditions and conditions["require_admin"]:
            return ctx.get("role", "").lower() != "admin"

        # Same-tenant condition
        if "require_same_tenant" in conditions and conditions["require_same_tenant"]:
            request_tenant = ctx.get("tenant_id", "default")
            resource_tenant = ctx.get("resource_tenant_id", "default")
            return request_tenant != resource_tenant

        # Risk threshold condition
        if "max_risk_score" in conditions:
            risk = ctx.get("risk_score", 0.0)
            return risk > conditions["max_risk_score"]

        # Time-window condition
        if "allowed_hours" in conditions:
            hours = conditions["allowed_hours"]
            current_hour = datetime.now(timezone.utc).hour
            return not (hours[0] <= current_hour <= hours[1])

        # Retrieval confidence threshold
        if "min_retrieval_confidence" in conditions:
            confidence = ctx.get("retrieval_confidence", 1.0)
            return confidence >= conditions["min_retrieval_confidence"]

        # Max concurrent agents
        if "max_concurrent_agents" in conditions:
            current_count = ctx.get("current_agent_count", 0)
            return current_count >= conditions["max_concurrent_agents"]

        return True

    def list_policies(self) -> List[SafetyPolicy]:
        """Returns all registered policies."""
        with self._lock:
            return list(self._policies.values())


# Global SafetyPolicyEngine instance
safety_policy_engine = SafetyPolicyEngine()
