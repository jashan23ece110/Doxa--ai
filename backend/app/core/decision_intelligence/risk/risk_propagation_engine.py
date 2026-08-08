"""
Enterprise Risk Propagation Engine.

Models cascading risk propagation chains and amplification factors across dependencies.
"""

from typing import Dict, Any, List
from app.core.logging import security_logger
from app.core.decision_intelligence.risk.risk_types import Risk, RiskPropagation


class RiskPropagationEngine:
    """Enterprise Risk Propagation Engine."""

    def analyze_propagation(self, primary_risk: Risk, secondary_risks: List[Risk]) -> RiskPropagation:
        """
        Models cascading propagation from primary risk to secondary risks.

        Args:
            primary_risk: Root Risk object.
            secondary_risks: List of downstream Risk objects.

        Returns:
            RiskPropagation object.
        """
        cascade_ids = [r.risk_id for r in secondary_risks]
        prop = RiskPropagation(
            primary_risk_id=primary_risk.risk_id,
            cascading_risk_ids=cascade_ids,
            amplification_factor=1.25,
            is_modeled_estimate=True,
        )

        security_logger.info(f"RiskPropagationEngine: Modeled risk propagation from '{primary_risk.title}' to {len(cascade_ids)} downstream risks (Amplification={prop.amplification_factor}x).")
        return prop


# Global RiskPropagationEngine instance
risk_propagation_engine = RiskPropagationEngine()
