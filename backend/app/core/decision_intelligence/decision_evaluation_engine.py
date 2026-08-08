"""
Decision Evaluation Engine.

Ranks alternatives against objectives, constraints, risk, cost, benefit, and uncertainty.
"""

from typing import Dict, Any, List, Tuple
from app.core.logging import security_logger
from app.core.decision_intelligence.decision_types import DecisionAlternative, DecisionEvaluation


class DecisionEvaluationEngine:
    """Decision Evaluation Engine."""

    def select_best_alternative(
        self,
        evaluations: List[Tuple[DecisionAlternative, DecisionEvaluation]]
    ) -> Tuple[DecisionAlternative, DecisionEvaluation]:
        """
        Ranks and selects the highest scoring decision alternative.

        Args:
            evaluations: List of (DecisionAlternative, DecisionEvaluation) tuples.

        Returns:
            Tuple of (Best DecisionAlternative, Best DecisionEvaluation).
        """
        sorted_evals = sorted(evaluations, key=lambda x: x[1].composite_score, reverse=True)
        best_alt, best_eval = sorted_evals[0]

        security_logger.info(f"DecisionEvaluationEngine: Selected best alternative '{best_alt.title}' (Composite Score={best_eval.composite_score}).")
        return best_alt, best_eval


# Global DecisionEvaluationEngine instance
decision_evaluation_engine = DecisionEvaluationEngine()
