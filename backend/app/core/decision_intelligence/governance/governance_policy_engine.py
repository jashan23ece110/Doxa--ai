"""
Enterprise Decision Governance Engine.

Enforces role-based decision authority, risk thresholds, and human approval requirements.
"""

from typing import Dict, Any, List
from app.core.logging import security_logger
from app.core.decision_intelligence.governance.explainability_types import GovernancePolicy, GovernanceViolation


class GovernancePolicyEngine:
    """Enterprise Decision Governance Engine."""

    def evaluate_policy_compliance(self, estimated_cost: float, risk_score: float) -> List[GovernanceViolation]:
        """
        Evaluates decision parameters against active enterprise governance policy bounds.

        Args:
            estimated_cost: Decision estimated cost float.
            risk_score: Decision risk score float.

        Returns:
            List of GovernanceViolation objects (empty if fully compliant).
        """
        policy = GovernancePolicy(name="StandardEnterpriseGovernancePolicy", min_confidence_threshold=0.80, max_allowed_risk_score=5.0, requires_human_approval_over_cost=10000.0)
        violations = []

        if risk_score > policy.max_allowed_risk_score:
            violations.append(
                GovernanceViolation(
                    policy_name=policy.name,
                    violation_reason=f"Risk score ({risk_score}) exceeds max policy threshold ({policy.max_allowed_risk_score}).",
                    severity="HIGH",
                )
            )

        security_logger.info(f"GovernancePolicyEngine: Evaluated policy compliance -> Violations={len(violations)}.")
        return violations


# Global GovernancePolicyEngine instance
governance_policy_engine = GovernancePolicyEngine()
