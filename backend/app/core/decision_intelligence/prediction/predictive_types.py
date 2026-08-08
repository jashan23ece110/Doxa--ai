"""
Enterprise Predictive Intelligence Types & Data Schemas.

Comprehensive Pydantic models for PredictionRequest, PredictionTarget, PredictionInput,
PredictionFeature, PredictionModel, PredictionResult, OutcomeDistribution, PredictionInterval,
PredictionScenario, PredictionConfidence, PredictionUncertainty, PredictionExplanation,
ModelEvaluation, PredictionComparison, PredictiveRecommendation, and PredictionMetrics.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class PredictionTarget(BaseModel):
    target_id: str = Field(default_factory=lambda: f"ptarg_{uuid.uuid4().hex[:8]}")
    name: str
    target_type: str = "NUMERIC"  # NUMERIC, CATEGORICAL, PROBABILITY
    horizon_days: int = 30


class PredictionFeature(BaseModel):
    feature_id: str = Field(default_factory=lambda: f"pfeat_{uuid.uuid4().hex[:8]}")
    name: str
    feature_value: float = 1.0
    importance_weight: float = 0.25
    feature_version: str = "1.0.0"


class PredictionInput(BaseModel):
    input_id: str = Field(default_factory=lambda: f"pinp_{uuid.uuid4().hex[:8]}")
    target: PredictionTarget
    features: List[PredictionFeature] = Field(default_factory=list)


class PredictionModel(BaseModel):
    model_id: str = Field(default_factory=lambda: f"pmod_{uuid.uuid4().hex[:8]}")
    name: str
    version: str = "1.0.0"
    model_type: str = "GRADIENT_BOOSTING_ENSEMBLE"
    status: str = "DEPLOYED"  # REGISTERED, VALIDATED, DEPLOYED, RETIRED
    accuracy_score: float = 0.94
    created_at: float = Field(default_factory=time.time)


class PredictionInterval(BaseModel):
    confidence_level: float = 0.95
    lower_bound: float = 85.0
    upper_bound: float = 115.0


class OutcomeDistribution(BaseModel):
    outcome_label: str
    probability: float = 0.85
    expected_value: float = 100.0


class PredictionConfidence(BaseModel):
    overall_confidence: float = 0.93
    model_certainty: float = 0.95
    data_quality_score: float = 0.91


class PredictionUncertainty(BaseModel):
    uncertainty_score: float = 0.07  # 0.0 to 1.0
    epistemic_uncertainty: float = 0.04
    aleatoric_uncertainty: float = 0.03
    uncertainty_description: str = "Low uncertainty driven by abundant historical data"


class PredictionExplanation(BaseModel):
    explanation_id: str = Field(default_factory=lambda: f"pexpl_{uuid.uuid4().hex[:8]}")
    top_feature_impacts: Dict[str, float] = Field(default_factory=lambda: {"feature_historical_roi": 0.45, "feature_market_trend": 0.35})
    rationale: str = "Prediction strongly influenced by positive historical ROI and baseline market stability."


class PredictionResult(BaseModel):
    prediction_id: str = Field(default_factory=lambda: f"pres_{uuid.uuid4().hex[:8]}")
    target_name: str
    predicted_value: float = 100.0
    outcome_distributions: List[OutcomeDistribution] = Field(default_factory=list)
    confidence: PredictionConfidence = Field(default_factory=PredictionConfidence)
    uncertainty: PredictionUncertainty = Field(default_factory=PredictionUncertainty)
    interval: PredictionInterval = Field(default_factory=PredictionInterval)
    explanation: PredictionExplanation = Field(default_factory=PredictionExplanation)
    model_version: str = "1.0.0"
    created_at: float = Field(default_factory=time.time)


class PredictionScenario(BaseModel):
    scenario_id: str = Field(default_factory=lambda: f"pscen_{uuid.uuid4().hex[:8]}")
    name: str  # BASELINE, OPTIMISTIC, ADVERSE, STRESS
    projected_prediction_value: float = 100.0
    probability: float = 0.50


class PredictionComparison(BaseModel):
    comparison_id: str = Field(default_factory=lambda: f"pcomp_{uuid.uuid4().hex[:8]}")
    model_a_id: str
    model_b_id: str
    delta_accuracy: float = 0.02
    compared_at: float = Field(default_factory=time.time)


class PredictionRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: f"preq_{uuid.uuid4().hex[:8]}")
    target_name: str
    inputs: PredictionInput
    created_at: float = Field(default_factory=time.time)


class ModelEvaluation(BaseModel):
    evaluation_id: str = Field(default_factory=lambda: f"meval_{uuid.uuid4().hex[:8]}")
    model_id: str
    accuracy: float = 0.94
    precision: float = 0.92
    recall: float = 0.93
    f1_score: float = 0.925
    rmse: float = 0.05
    brier_score: float = 0.02
    evaluated_at: float = Field(default_factory=time.time)


class PredictiveRecommendation(BaseModel):
    recommendation_id: str = Field(default_factory=lambda: f"prec_{uuid.uuid4().hex[:8]}")
    prediction_id: str
    recommended_action: str
    expected_gain: float = 15.0
    confidence_level: float = 0.93
    requires_human_approval: bool = True
    created_at: float = Field(default_factory=time.time)


class PredictionMetrics(BaseModel):
    predictions_generated_count: int = 0
    models_registered_count: int = 0
    drift_alerts_count: int = 0
    average_prediction_latency_ms: float = 0.0
