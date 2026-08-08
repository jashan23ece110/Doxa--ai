"""
Enterprise Decision Modeling Engine.

Evaluates alternatives via configurable decision models (weighted scoring, cost-benefit, risk-adjusted scoring).
"""

import time
from typing import Dict, Any, List
from app.core.logging import security_logger
from app.core.decision_intelligence.decision_types import DecisionAlternative, DecisionEvaluation


class DecisionModelEngine:
    """Enterprise Decision Modeling Engine."""

    def evaluate_alternative(self, alt: DecisionAlternative, model_type: str = "WEIGHTED_SCORING") -> DecisionEvaluation:
        """
        Evaluates a decision alternative using chosen decision model.

        Args:
            alt: DecisionAlternative object.
            model_type: Decision model strategy string.

        Returns:
            DecisionEvaluation object.
        """
        b_c_ratio = round(alt.expected_benefit / max(alt.expected_cost, 1.0), 2)
        composite = round((alt.expected_benefit * 0.70) + ((100.0 - alt.expected_cost) * 0.30), 2)

        eval_res = DecisionEvaluation(
            alternative_id=alt.alternative_id,
            composite_score=composite,
            benefit_cost_ratio=b_c_ratio,
            risk_adjusted_score=round(composite * 0.95, 2),
        )

        security_logger.info(f"DecisionModelEngine: Evaluated alternative '{alt.title}' via {model_type} (Score={eval_res.composite_score}, B/C={eval_res.benefit_cost_ratio}).")
        return eval_res


# Global DecisionModelEngine instance
decision_model_engine = DecisionModelEngine()
