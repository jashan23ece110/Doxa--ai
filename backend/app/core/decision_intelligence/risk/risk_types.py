"""
Enterprise Risk Intelligence Types & Data Schemas.

Comprehensive Pydantic models for Risk, RiskFactor, RiskCategory, RiskIndicator, RiskAssessment,
RiskScore, RiskProbability, RiskImpact, RiskScenario, RiskForecast, RiskCorrelation,
RiskPropagation, EarlyWarningSignal, RiskMitigation, RiskRecommendation, and RiskMetrics.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class RiskCategory(BaseModel):
    category_id: str = Field(default_factory=lambda: f"rcat_{uuid.uuid4().hex[:8]}")
    name: str  # OPERATIONAL, FINANCIAL, SECURITY, COMPLIANCE, STRATEGIC, TECHNICAL
    description: str = ""


class RiskFactor(BaseModel):
    factor_id: str = Field(default_factory=lambda: f"rfct_{uuid.uuid4().hex[:8]}")
    name: str
    weight: float = 1.0
    current_value: float = 0.50


class RiskIndicator(BaseModel):
    indicator_id: str = Field(default_factory=lambda: f"rind_{uuid.uuid4().hex[:8]}")
    name: str
    threshold_value: float = 0.80
    current_value: float = 0.45
    unit: str = "PCT"


class RiskProbability(BaseModel):
    value: float = 0.15  # 0.0 to 1.0
    confidence: float = 0.90
    basis_description: str = "Historical event frequency and trend extrapolation"


class RiskImpact(BaseModel):
    severity: str = "LOW"  # LOW, MEDIUM, HIGH, CRITICAL
    estimated_financial_loss: float = 10000.0
    operational_downtime_minutes: float = 0.0


class Risk(BaseModel):
    risk_id: str = Field(default_factory=lambda: f"risk_{uuid.uuid4().hex[:8]}")
    title: str
    category: str = "OPERATIONAL"
    probability: RiskProbability = Field(default_factory=RiskProbability)
    impact: RiskImpact = Field(default_factory=RiskImpact)
    indicators: List[RiskIndicator] = Field(default_factory=list)
    created_at: float = Field(default_factory=time.time)


class RiskScore(BaseModel):
    score_id: str = Field(default_factory=lambda: f"rscr_{uuid.uuid4().hex[:8]}")
    risk_id: str
    raw_score: float = 1.5  # 0.0 to 10.0
    normalized_score: float = 0.15
    scoring_methodology: str = "PROBABILITY_X_IMPACT"
    calculated_at: float = Field(default_factory=time.time)


class RiskAssessment(BaseModel):
    assessment_id: str = Field(default_factory=lambda: f"rass_{uuid.uuid4().hex[:8]}")
    target_entity: str
    risks_evaluated: List[Risk] = Field(default_factory=list)
    overall_risk_score: float = 1.5
    assessed_at: float = Field(default_factory=time.time)


class RiskCorrelation(BaseModel):
    correlation_id: str = Field(default_factory=lambda: f"rcorr_{uuid.uuid4().hex[:8]}")
    source_risk_id: str
    target_risk_id: str
    correlation_coefficient: float = 0.75  # -1.0 to 1.0
    relationship_type: str = "DEPENDENCY"


class RiskPropagation(BaseModel):
    propagation_id: str = Field(default_factory=lambda: f"rprop_{uuid.uuid4().hex[:8]}")
    primary_risk_id: str
    cascading_risk_ids: List[str] = Field(default_factory=list)
    amplification_factor: float = 1.2
    is_modeled_estimate: bool = True


class RiskForecast(BaseModel):
    forecast_id: str = Field(default_factory=lambda: f"rfcst_{uuid.uuid4().hex[:8]}")
    metric_name: str
    horizon_days: int = 30
    projected_risk_score: float = 1.8
    confidence_interval_low: float = 1.2
    confidence_interval_high: float = 2.4
    forecasted_at: float = Field(default_factory=time.time)


class EarlyWarningSignal(BaseModel):
    signal_id: str = Field(default_factory=lambda: f"ewsig_{uuid.uuid4().hex[:8]}")
    risk_id: str
    trigger_indicator_name: str
    severity: str = "MEDIUM"
    message: str
    detected_at: float = Field(default_factory=time.time)


class RiskScenario(BaseModel):
    scenario_id: str = Field(default_factory=lambda: f"rscen_{uuid.uuid4().hex[:8]}")
    name: str  # BASELINE, EMERGING, ADVERSE, SEVERE, STRESS
    triggers: List[str] = Field(default_factory=list)
    projected_impact_score: float = 2.5
    probability: float = 0.20


class RiskMitigation(BaseModel):
    mitigation_id: str = Field(default_factory=lambda: f"rmit_{uuid.uuid4().hex[:8]}")
    risk_id: str
    title: str
    description: str
    expected_risk_reduction_pct: float = 75.0
    implementation_cost: float = 5000.0
    residual_risk_score: float = 0.38
    requires_approval: bool = True


class RiskRecommendation(BaseModel):
    recommendation_id: str = Field(default_factory=lambda: f"rrec_{uuid.uuid4().hex[:8]}")
    assessment_id: str
    recommended_mitigation: RiskMitigation
    strategic_context: str
    requires_human_approval: bool = True
    created_at: float = Field(default_factory=time.time)


class RiskMetrics(BaseModel):
    risks_assessed_count: int = 0
    signals_detected_count: int = 0
    mitigations_recommended_count: int = 0
    average_forecast_confidence: float = 0.93
