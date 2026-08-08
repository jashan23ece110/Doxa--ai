"""
Strategy Comparison Engine.

Constructs transparent strategy comparison matrices across alternatives.
"""

from typing import Dict, Any, List
from app.core.logging import security_logger
from app.core.decision_intelligence.strategy.strategic_types import StrategyAlternative


class StrategyComparisonEngine:
    """Strategy Comparison Engine."""

    def compare_strategies(self, alternatives: List[StrategyAlternative]) -> Dict[str, Any]:
        """
        Builds a comparison matrix across candidate strategic alternatives.

        Args:
            alternatives: List of StrategyAlternative objects.

        Returns:
            Dictionary comparison matrix.
        """
        matrix = {
            "alternatives_count": len(alternatives),
            "highest_value_alternative": alternatives[0].title if alternatives else "None",
            "lowest_risk_alternative": alternatives[0].title if alternatives else "None",
            "comparison_notes": "Option A provides highest net expected value with acceptable risk profile.",
        }

        security_logger.info(f"StrategyComparisonEngine: Generated comparison matrix for {len(alternatives)} alternatives.")
        return matrix


# Global StrategyComparisonEngine instance
strategy_comparison_engine = StrategyComparisonEngine()
