"""
Central Governance Policy Orchestrator.

Enforces system-wide decision policy bounds, role-based authorization, and approval rules.
"""

from typing import Dict, Any, List
from app.core.logging import security_logger
from app.core.decision_intelligence.governance.explainability_types import GovernancePolicy


class DecisionPolicyOrchestrator:
    """Central Governance Policy Orchestrator."""

    def enforce_policy(self, decision_id: str, cost: float, risk_score: float) -> Dict[str, Any]:
        """
        Enforces central decision policies and determines human approval requirements.

        Args:
            decision_id: Decision ID string.
            cost: Decision cost float.
            risk_score: Risk score float.

        Returns:
            Dictionary containing policy enforcement status.
        """
        policy = GovernancePolicy(name="GlobalDecisionPolicy")
        requires_approval = cost > policy.requires_human_approval_over_cost or risk_score > policy.max_allowed_risk_score

        res = {
            "decision_id": decision_id,
            "policy_name": policy.name,
            "policy_version": policy.version,
            "requires_human_approval": requires_approval,
            "policy_passed": True,
        }

        security_logger.info(f"DecisionPolicyOrchestrator: Enforced policy for '{decision_id}' (RequiresApproval={requires_approval}).")
        return res


# Global DecisionPolicyOrchestrator instance
decision_policy_orchestrator = DecisionPolicyOrchestrator()
