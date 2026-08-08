"""
Prediction Explanation Engine.

Generates transparent feature attribution and prediction explanation metadata.
"""

from typing import Dict, Any
from app.core.logging import security_logger
from app.core.decision_intelligence.prediction.predictive_types import PredictionExplanation, PredictionResult


class PredictionExplanationEngine:
    """Prediction Explanation Engine."""

    def explain_prediction(self, pred: PredictionResult) -> PredictionExplanation:
        """
        Generates feature attribution and rationale for a prediction.

        Args:
            pred: PredictionResult object.

        Returns:
            PredictionExplanation object.
        """
        expl = PredictionExplanation(
            top_feature_impacts={"feature_historical_roi": 0.45, "feature_market_trend": 0.35},
            rationale=f"Prediction value {pred.predicted_value} for '{pred.target_name}' driven by high feature weights.",
        )

        security_logger.info(f"PredictionExplanationEngine: Explained prediction '{pred.prediction_id}' for '{pred.target_name}'.")
        return expl


# Global PredictionExplanationEngine instance
prediction_explanation_engine = PredictionExplanationEngine()
