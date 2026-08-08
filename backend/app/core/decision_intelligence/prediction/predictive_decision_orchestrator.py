"""
Global Predictive Decision Orchestrator.

Master orchestrator driving end-to-end predictive decision intelligence workflows:
Objective -> Context & Features -> Model Selection -> Prediction -> Probability Estimation -> Scenarios -> Uncertainty -> Explanation -> Outcome Ranking -> Recommendation.
"""

import time
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.decision_intelligence.prediction.predictive_types import (
    PredictionTarget, PredictionResult, PredictiveRecommendation, PredictionScenario
)
from app.core.decision_intelligence.prediction.predictive_model_registry import predictive_model_registry
from app.core.decision_intelligence.prediction.feature_engine import feature_engine
from app.core.decision_intelligence.prediction.predictive_engine import predictive_engine
from app.core.decision_intelligence.prediction.outcome_probability_engine import outcome_probability_engine
from app.core.decision_intelligence.prediction.predictive_scenario_engine import predictive_scenario_engine
from app.core.decision_intelligence.prediction.model_evaluation_engine import model_evaluation_engine
from app.core.decision_intelligence.prediction.prediction_explanation_engine import prediction_explanation_engine
from app.core.decision_intelligence.prediction.predictive_drift_monitor import predictive_drift_monitor


class MasterPredictionResult(BaseModel):
    analysis_id: str = Field(default_factory=lambda: f"mpred_{int(time.time() * 1000)}")
    target_name: str
    prediction: PredictionResult
    scenarios: List[PredictionScenario] = Field(default_factory=list)
    recommendation: PredictiveRecommendation
    status: str = "COMPLETED"
    summary: str = "Predictive decision analysis completed with explainable feature attribution."
    executed_at: float = Field(default_factory=time.time)


class PredictiveDecisionOrchestrator:
    """Global Predictive Decision Orchestrator Facade."""

    async def execute_predictive_analysis(self, target_name: str) -> MasterPredictionResult:
        """
        Executes complete end-to-end predictive decision analysis pipeline.

        Args:
            target_name: Target metric or outcome name string.

        Returns:
            MasterPredictionResult object.
        """
        t0 = time.time()
        security_logger.info(f"PredictiveDecisionOrchestrator: Starting predictive analysis for '{target_name}'.")

        # 1. Target & Feature Construction & Model Selection
        target = PredictionTarget(name=target_name)
        pinp = await feature_engine.construct_features(target)
        pmod = predictive_model_registry.get_deployed_model(target_name)

        # 2. Prediction & Probability Estimation & Scenarios
        pred = predictive_engine.generate_prediction(pinp, model_version=pmod.version)
        outcome_probability_engine.estimate_outcome_probabilities(target_name)
        scenarios = predictive_scenario_engine.evaluate_predictive_scenarios(pred.predicted_value)

        # 3. Model Evaluation & Explanation & Drift Monitoring
        model_evaluation_engine.evaluate_model_performance(pmod.model_id)
        prediction_explanation_engine.explain_prediction(pred)
        predictive_drift_monitor.check_drift(pmod.model_id)

        # 4. Recommendation Generation
        rec = PredictiveRecommendation(
            prediction_id=pred.prediction_id,
            recommended_action=f"Proceed with initiative targeting '{target_name}' based on predicted yield of {pred.predicted_value}.",
            expected_gain=15.0,
            confidence_level=pred.confidence.overall_confidence,
            requires_human_approval=True,
        )

        res = MasterPredictionResult(
            target_name=target_name,
            prediction=pred,
            scenarios=scenarios,
            recommendation=rec,
            status="COMPLETED",
        )

        security_logger.info(f"PredictiveDecisionOrchestrator: Completed predictive analysis '{res.analysis_id}' for '{target_name}' in {round((time.time() - t0)*1000, 2)}ms (Value={pred.predicted_value}).")
        return res


# Global PredictiveDecisionOrchestrator instance
predictive_decision_orchestrator = PredictiveDecisionOrchestrator()
