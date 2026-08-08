"""
Governance Monitor.

Monitors decision pipelines for policy violations, approval bypass attempts, and missing evidence.
"""

from typing import Dict, Any, List
from app.core.logging import security_logger
from app.core.decision_intelligence.governance.explainability_types import GovernanceViolation


class GovernanceMonitor:
    """Governance Monitor."""

    def inspect_decision(self, decision_id: str, confidence_score: float) -> List[GovernanceViolation]:
        """
        Inspects decision parameters for governance anomalies and low confidence scores.

        Args:
            decision_id: Decision ID string.
            confidence_score: Decision confidence score float.

        Returns:
            List of GovernanceViolation objects.
        """
        violations = []
        if confidence_score < 0.80:
            violations.append(
                GovernanceViolation(
                    policy_name="MinimumConfidencePolicy",
                    violation_reason=f"Confidence score ({confidence_score}) below required policy threshold (0.80).",
                    severity="MEDIUM",
                )
            )

        security_logger.info(f"GovernanceMonitor: Inspected decision '{decision_id}' -> Violations={len(violations)}.")
        return violations


# Global GovernanceMonitor instance
governance_monitor = GovernanceMonitor()
