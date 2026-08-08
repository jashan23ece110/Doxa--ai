"""
Decision Scoring Engine for Enterprise Decision Platform.

Scores candidate decisions by expected value, confidence, risk, cost, time,
and success probability.
"""

from app.core.decision.decision_models import DecisionScoreCard


class DecisionScoringEngine:
    """Calculates multi-factor decision scorecards."""

    @staticmethod
    def score_decision(
        expected_value: float = 0.95,
        confidence: float = 0.94,
        risk: float = 0.05,
    ) -> DecisionScoreCard:
        """
        Calculates composite decision score.
        """
        composite = round(
            (expected_value * 0.35)
            + (confidence * 0.35)
            - (risk * 0.3)
            + 0.15,
            2,
        )
        composite = max(0.0, min(1.0, composite))

        return DecisionScoreCard(
            expected_value_score=expected_value,
            confidence_score=confidence,
            risk_score=risk,
            composite_score=composite,
        )


# Global DecisionScoringEngine instance
decision_scoring_engine = DecisionScoringEngine()
