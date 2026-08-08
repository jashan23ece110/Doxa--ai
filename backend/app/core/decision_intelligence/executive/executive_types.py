"""
Executive Decision Support & Autonomous Recommendation Types & Data Schemas.

Comprehensive Pydantic models for ExecutiveDecisionRequest, ExecutiveObjective, ExecutiveDecisionBrief,
StrategicRecommendation, ActionRecommendation, PriorityRecommendation, RiskSummary, Opportunity,
ExecutiveScenario, ExecutiveForecast, DecisionAlternative, DecisionRationale, DecisionConfidence,
ExecutiveActionPlan, and ExecutiveMetrics.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ExecutiveObjective(BaseModel):
    objective_id: str = Field(default_factory=lambda: f"eobj_{uuid.uuid4().hex[:8]}")
    name: str
    target_kpi: str = "REVENUE_GROWTH"
    target_value: float = 15.0  # e.g., +15%
    time_horizon: str = "MEDIUM_TERM"  # SHORT_TERM, MEDIUM_TERM, LONG_TERM


class RiskSummary(BaseModel):
    summary_id: str = Field(default_factory=lambda: f"rsum_{uuid.uuid4().hex[:8]}")
    risk_level: str = "LOW"  # LOW, MEDIUM, HIGH, CRITICAL
    primary_risk_driver: str = "Market volatility"
    risk_score: float = 1.5


class Opportunity(BaseModel):
    opportunity_id: str = Field(default_factory=lambda: f"opp_{uuid.uuid4().hex[:8]}")
    title: str = "Automated Workload Scaling"
    estimated_upside_value: float = 250000.0
    probability: float = 0.85


class ExecutiveForecast(BaseModel):
    forecast_id: str = Field(default_factory=lambda: f"efore_{uuid.uuid4().hex[:8]}")
    metric_name: str = "NetProfit"
    projected_value: float = 1200000.0
    confidence_interval: str = "[1.1M, 1.3M]"


class DecisionAlternative(BaseModel):
    alternative_id: str = Field(default_factory=lambda: f"ealt_{uuid.uuid4().hex[:8]}")
    title: str
    description: str
    expected_roi: float = 22.5
    rank: int = 1


class DecisionRationale(BaseModel):
    rationale_id: str = Field(default_factory=lambda: f"erat_{uuid.uuid4().hex[:8]}")
    summary: str = "Top alternative maximizes ROI while respecting budget limits and low risk."


class DecisionConfidence(BaseModel):
    confidence_score: float = 0.94
    confidence_level: str = "HIGH"  # HIGH, MEDIUM, LOW
    notes: str = "Backed by 96% evidence reliability score."


class StrategicRecommendation(BaseModel):
    recommendation_id: str = Field(default_factory=lambda: f"srec_{uuid.uuid4().hex[:8]}")
    title: str
    recommended_option: str
    expected_benefit: float = 450000.0
    estimated_cost: float = 80000.0
    rationale: DecisionRationale = Field(default_factory=DecisionRationale)
    confidence: DecisionConfidence = Field(default_factory=DecisionConfidence)
    authorization_level: str = "LEVEL_3_APPROVAL_READY"  # LEVEL_0, LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4
    requires_approval: bool = True


class ActionRecommendation(BaseModel):
    action_id: str = Field(default_factory=lambda: f"arec_{uuid.uuid4().hex[:8]}")
    action_title: str
    target_system: str = "ProductionCluster"
    priority: str = "HIGH"


class PriorityRecommendation(BaseModel):
    priority_id: str = Field(default_factory=lambda: f"prec_{uuid.uuid4().hex[:8]}")
    decision_title: str
    urgency_score: float = 8.5
    impact_score: float = 9.0
    overall_priority_rank: int = 1


class ExecutiveScenario(BaseModel):
    scenario_id: str = Field(default_factory=lambda: f"escen_{uuid.uuid4().hex[:8]}")
    name: str  # BASELINE, OPTIMISTIC, ADVERSE, STRESS
    projected_roi: float = 22.5
    is_simulated: bool = True


class ExecutiveActionPlan(BaseModel):
    plan_id: str = Field(default_factory=lambda: f"eactp_{uuid.uuid4().hex[:8]}")
    title: str
    milestones: List[str] = Field(default_factory=list)
    responsible_role: str = "VP_Engineering"
    is_authorized: bool = False
    created_at: float = Field(default_factory=time.time)


class ExecutiveDecisionBrief(BaseModel):
    brief_id: str = Field(default_factory=lambda: f"ebrief_{uuid.uuid4().hex[:8]}")
    title: str
    current_situation: str
    key_facts: List[str] = Field(default_factory=list)
    risk_summary: RiskSummary = Field(default_factory=RiskSummary)
    opportunities: List[Opportunity] = Field(default_factory=list)
    forecasts: List[ExecutiveForecast] = Field(default_factory=list)
    alternatives: List[DecisionAlternative] = Field(default_factory=list)
    recommended_direction: StrategicRecommendation
    action_plan: ExecutiveActionPlan
    created_at: float = Field(default_factory=time.time)


class ExecutiveDecisionRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: f"exreq_{uuid.uuid4().hex[:8]}")
    title: str
    strategic_objective: ExecutiveObjective = Field(default_factory=ExecutiveObjective)
    budget_limit: float = 100000.0
    created_at: float = Field(default_factory=time.time)


class ExecutiveMetrics(BaseModel):
    briefs_generated_count: int = 0
    recommendations_delivered_count: int = 0
    approved_action_plans_count: int = 0
    average_recommendation_confidence: float = 0.94
