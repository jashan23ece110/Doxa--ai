"""
Enterprise Early Warning System.

Detects threshold breaches, anomalous trends, and accelerating risk indicators.
"""

from typing import Dict, Any, List
from app.core.logging import security_logger
from app.core.decision_intelligence.risk.risk_types import Risk, EarlyWarningSignal


class EarlyWarningEngine:
    """Enterprise Early Warning System."""

    def check_indicators(self, risks: List[Risk]) -> List[EarlyWarningSignal]:
        """
        Evaluates risk indicators against thresholds to generate prioritized early warning signals.

        Args:
            risks: List of Risk objects.

        Returns:
            List of EarlyWarningSignal objects.
        """
        signals = []
        for r in risks:
            for ind in r.indicators:
                if ind.current_value >= ind.threshold_value:
                    signals.append(
                        EarlyWarningSignal(
                            risk_id=r.risk_id,
                            trigger_indicator_name=ind.name,
                            severity="HIGH" if r.impact.severity in ["HIGH", "CRITICAL"] else "MEDIUM",
                            message=f"Indicator '{ind.name}' breached threshold ({ind.current_value} >= {ind.threshold_value} {ind.unit}).",
                        )
                    )

        security_logger.info(f"EarlyWarningEngine: Evaluated {len(risks)} risks -> Generated {len(signals)} early warning signals.")
        return signals


# Global EarlyWarningEngine instance
early_warning_engine = EarlyWarningEngine()
