"""
Enterprise Strategic Intelligence Types & Data Schemas.

Comprehensive Pydantic models for StrategicObjective, StrategicPlan, StrategicInitiative,
StrategicMilestone, StrategicAssumption, StrategicConstraint, Scenario, ScenarioVariable,
ScenarioOutcome, ScenarioComparison, WhatIfAnalysis, StrategyAlternative, StrategicTradeoff,
StrategicRecommendation, StrategicEvaluation, and StrategicMetrics.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class StrategicObjective(BaseModel):
    objective_id: str = Field(default_factory=lambda: f"sobj_{uuid.uuid4().hex[:8]}")
    title: str
    target_metric: str
    target_value: float = 100.0
    horizon_months: int = 12
    created_at: float = Field(default_factory=time.time)


class StrategicAssumption(BaseModel):
    assumption_id: str = Field(default_factory=lambda: f"sasm_{uuid.uuid4().hex[:8]}")
    description: str
    confidence_level: float = 0.85
    impact_if_false: str = "HIGH"  # LOW, MEDIUM, HIGH, CRITICAL


class StrategicConstraint(BaseModel):
    constraint_id: str = Field(default_factory=lambda: f"scnst_{uuid.uuid4().hex[:8]}")
    name: str
    constraint_type: str  # FINANCIAL, RESOURCE, TIMELINE, REGULATORY
    limit_value: float = 500000.0


class StrategicMilestone(BaseModel):
    milestone_id: str = Field(default_factory=lambda: f"smil_{uuid.uuid4().hex[:8]}")
    title: str
    target_month: int = 3
    is_critical_path: bool = True


class StrategicInitiative(BaseModel):
    initiative_id: str = Field(default_factory=lambda: f"sinit_{uuid.uuid4().hex[:8]}")
    title: str
    description: str
    estimated_cost: float = 50000.0
    expected_benefit: float = 200000.0
    milestones: List[StrategicMilestone] = Field(default_factory=list)


class ScenarioVariable(BaseModel):
    variable_id: str = Field(default_factory=lambda: f"scvar_{uuid.uuid4().hex[:8]}")
    name: str
    baseline_value: float = 1.0
    scenario_value: float = 1.25


class ScenarioOutcome(BaseModel):
    outcome_id: str = Field(default_factory=lambda: f"sout_{uuid.uuid4().hex[:8]}")
    scenario_id: str
    projected_roi_pct: float = 25.0
    projected_cost: float = 50000.0
    projected_risk_score: float = 0.15


class Scenario(BaseModel):
    scenario_id: str = Field(default_factory=lambda: f"scen_{uuid.uuid4().hex[:8]}")
    name: str  # BASELINE, OPTIMISTIC, CONSERVATIVE, ADVERSE, STRESS
    description: str
    variables: List[ScenarioVariable] = Field(default_factory=list)
    assumptions: List[StrategicAssumption] = Field(default_factory=list)
    outcomes: List[ScenarioOutcome] = Field(default_factory=list)
    probability: float = 0.50
    created_at: float = Field(default_factory=time.time)


class ScenarioComparison(BaseModel):
    comparison_id: str = Field(default_factory=lambda: f"scomp_{uuid.uuid4().hex[:8]}")
    base_scenario_id: str
    target_scenario_id: str
    delta_roi_pct: float = 10.0
    delta_cost: float = -5000.0
    evaluated_at: float = Field(default_factory=time.time)


class WhatIfAnalysis(BaseModel):
    analysis_id: str = Field(default_factory=lambda: f"whatif_{uuid.uuid4().hex[:8]}")
    param_name: str
    original_value: Any
    modified_value: Any
    resulting_impact_summary: str
    analyzed_at: float = Field(default_factory=time.time)


class StrategyAlternative(BaseModel):
    alternative_id: str = Field(default_factory=lambda: f"salt_{uuid.uuid4().hex[:8]}")
    title: str
    initiatives: List[StrategicInitiative] = Field(default_factory=list)
    expected_value: float = 150000.0
    risk_score: float = 0.20


class StrategicTradeoff(BaseModel):
    tradeoff_id: str = Field(default_factory=lambda: f"trade_{uuid.uuid4().hex[:8]}")
    dimension_a: str  # e.g., SPEED
    dimension_b: str  # e.g., RELIABILITY
    tradeoff_description: str
    recommended_balance: str = "70% Speed / 30% Extra Audit Verification"


class StrategicPlan(BaseModel):
    plan_id: str = Field(default_factory=lambda: f"splan_{uuid.uuid4().hex[:8]}")
    title: str
    objectives: List[StrategicObjective] = Field(default_factory=list)
    chosen_alternative: StrategyAlternative
    scenarios: List[Scenario] = Field(default_factory=list)
    version: str = "1.0.0"
    created_at: float = Field(default_factory=time.time)


class StrategicRecommendation(BaseModel):
    recommendation_id: str = Field(default_factory=lambda: f"srec_{uuid.uuid4().hex[:8]}")
    plan_id: str
    recommended_path_title: str
    strategic_rationale: str
    confidence_level: float = 0.94
    requires_human_approval: bool = True
    created_at: float = Field(default_factory=time.time)


class StrategicEvaluation(BaseModel):
    evaluation_id: str = Field(default_factory=lambda: f"seval_{uuid.uuid4().hex[:8]}")
    plan_id: str
    overall_strategic_fit: float = 95.0
    feasibility_score: float = 92.0
    risk_adjusted_return: float = 88.5
    evaluated_at: float = Field(default_factory=time.time)


class StrategicMetrics(BaseModel):
    plans_generated_count: int = 0
    scenarios_simulated_count: int = 0
    what_if_analyses_count: int = 0
    average_forecasting_accuracy: float = 0.94
