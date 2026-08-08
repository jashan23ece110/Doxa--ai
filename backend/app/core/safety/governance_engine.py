"""
Enterprise AI Governance Engine.

Approves or denies tool execution, memory updates, workflow execution,
agent collaboration, plugin execution, and external MCP execution
based on policy engine evaluations, risk assessments, and trust scores.
"""

import asyncio
import time
from typing import Dict, Any, List
from app.core.logging import logger
from app.core.config import settings
from app.core.safety.safety_types import (
    GovernanceDecision,
    GovernanceAction,
    PolicyViolation,
    PolicyScope,
    PolicyEffect,
    RiskLevel,
)
from app.core.safety.policy_engine import safety_policy_engine


class GovernanceEngine:
    """Enterprise governance engine for approving/denying AI actions."""

    # Maps resource types to policy scopes
    _SCOPE_MAP: Dict[str, PolicyScope] = {
        "tool": PolicyScope.TOOL,
        "memory": PolicyScope.MEMORY,
        "rag": PolicyScope.RAG,
        "workflow": PolicyScope.WORKFLOW,
        "agent": PolicyScope.AGENT,
        "plugin": PolicyScope.PLUGIN,
        "mcp": PolicyScope.MCP,
        "model": PolicyScope.MODEL,
        "execution": PolicyScope.EXECUTION,
    }

    async def evaluate(
        self,
        resource_type: str,
        resource_id: str = "",
        context: Dict[str, Any] = None,
    ) -> GovernanceDecision:
        """
        Evaluates whether an action should be approved, denied, or escalated.

        Args:
            resource_type: Type of resource (tool, memory, workflow, agent, plugin, mcp).
            resource_id: Specific resource identifier.
            context: Execution context dict with keys like:
                - user_id, tenant_id, role, risk_score, trust_score, etc.

        Returns:
            GovernanceDecision with action, reason, violations, and conditions.
        """
        if not settings.GOVERNANCE_ENABLED:
            return GovernanceDecision(
                action=GovernanceAction.APPROVE,
                resource_type=resource_type,
                resource_id=resource_id,
                reason="Governance disabled.",
            )

        start = time.time()
        ctx = context or {}
        scope = self._SCOPE_MAP.get(resource_type, PolicyScope.GLOBAL)

        # ── Step 1: Policy Engine Evaluation ──
        effect, violations = await safety_policy_engine.evaluate(
            scope=scope,
            resource=resource_id,
            context=ctx,
        )

        # ── Step 2: Risk-Based Governance ──
        risk_score = ctx.get("risk_score", 0.0)
        trust_score = ctx.get("trust_score", 1.0)

        action = GovernanceAction.APPROVE
        reason_parts: List[str] = []
        conditions: List[str] = []

        if effect == PolicyEffect.DENY:
            action = GovernanceAction.DENY
            reason_parts.append(f"Policy DENY for {resource_type}/{resource_id}.")

        elif effect == PolicyEffect.CONDITIONAL:
            # Check additional conditions
            if risk_score > settings.RISK_THRESHOLD:
                action = GovernanceAction.DENY
                reason_parts.append(
                    f"Risk score ({risk_score:.4f}) exceeds threshold ({settings.RISK_THRESHOLD})."
                )
            elif trust_score < settings.TRUST_THRESHOLD:
                action = GovernanceAction.DENY
                reason_parts.append(
                    f"Trust score ({trust_score:.4f}) below threshold ({settings.TRUST_THRESHOLD})."
                )
            else:
                action = GovernanceAction.CONDITIONALLY_APPROVE
                conditions.extend(self._generate_conditions(resource_type, ctx))
                reason_parts.append("Conditionally approved with safeguards.")

        else:
            # ALLOW — but check critical risk overrides
            if risk_score > 0.9:
                action = GovernanceAction.ESCALATE
                reason_parts.append(
                    f"Critical risk score ({risk_score:.4f}) requires human review."
                )
            elif trust_score < 0.2:
                action = GovernanceAction.ESCALATE
                reason_parts.append(
                    f"Very low trust score ({trust_score:.4f}) requires human review."
                )
            else:
                reason_parts.append(f"Approved: {resource_type}/{resource_id}.")

        elapsed = (time.time() - start) * 1000

        decision = GovernanceDecision(
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            reason=" ".join(reason_parts),
            policy_violations=violations,
            conditions=conditions,
            latency_ms=round(elapsed, 2),
        )

        log_fn = logger.info if action == GovernanceAction.APPROVE else logger.warning
        log_fn(
            f"GovernanceEngine '{decision.decision_id}': "
            f"Action={action.value}, Resource={resource_type}/{resource_id}, "
            f"Risk={risk_score:.4f}, Trust={trust_score:.4f}, "
            f"Violations={len(violations)}, Duration={elapsed:.2f}ms"
        )
        return decision

    @staticmethod
    def _generate_conditions(resource_type: str, ctx: Dict[str, Any]) -> List[str]:
        """Generates conditions for CONDITIONALLY_APPROVE decisions."""
        conditions: List[str] = []

        if resource_type == "tool":
            conditions.append("Tool output must be validated before further processing.")
            conditions.append("Tool execution timeout enforced.")
        elif resource_type == "memory":
            conditions.append("Memory update must be logged in audit trail.")
            conditions.append("Cross-tenant isolation verified.")
        elif resource_type == "workflow":
            conditions.append("Workflow steps must respect execution quotas.")
        elif resource_type == "agent":
            conditions.append("Agent count must not exceed configured maximum.")
            conditions.append("Agent output must pass safety check before delivery.")
        elif resource_type == "plugin":
            conditions.append("Plugin execution sandboxed.")
            conditions.append("Plugin output sanitized.")
        elif resource_type == "mcp":
            conditions.append("MCP external call logged and monitored.")
            conditions.append("MCP response validated before integration.")

        return conditions

    async def batch_evaluate(
        self,
        requests: List[Dict[str, Any]],
    ) -> List[GovernanceDecision]:
        """
        Evaluates multiple governance requests concurrently.

        Args:
            requests: List of dicts, each with resource_type, resource_id, context.

        Returns:
            List of GovernanceDecision.
        """
        tasks = [
            self.evaluate(
                resource_type=req.get("resource_type", "execution"),
                resource_id=req.get("resource_id", ""),
                context=req.get("context", {}),
            )
            for req in requests
        ]
        return list(await asyncio.gather(*tasks))


# Global GovernanceEngine instance
governance_engine = GovernanceEngine()
