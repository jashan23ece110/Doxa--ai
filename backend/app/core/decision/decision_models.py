"""
Decision Intelligence Models for Enterprise Decision Platform.

Defines Pydantic data models for MilestoneNode, GoalDecomposition, StrategicRoadmap,
ConstraintRule, RiskAssessmentReport, ScenarioSimulation, DecisionScoreCard,
ResourceOptimizationPlan, OpportunityInsight, DecisionMemoryRecord, and DecisionAnalyticsSummary.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class MilestoneNode(BaseModel):
    """Subtask milestone in goal decomposition."""

    milestone_id: str = Field(default_factory=lambda: f"ms_{uuid.uuid4().hex[:8]}")
    title: str
    description: str
    dependencies: List[str] = Field(default_factory=list)
    priority: int = 1
    status: str = "PENDING"  # PENDING, IN_PROGRESS, COMPLETED


class GoalDecomposition(BaseModel):
    """Decomposed goal execution graph."""

    goal_id: str = Field(default_factory=lambda: f"goal_{uuid.uuid4().hex[:8]}")
    main_goal: str
    milestones: List[MilestoneNode] = Field(default_factory=list)
    execution_order: List[str] = Field(default_factory=list)
    created_at: float = Field(default_factory=time.time)


class StrategicRoadmap(BaseModel):
    """Strategic execution roadmap."""

    roadmap_id: str = Field(default_factory=lambda: f"road_{uuid.uuid4().hex[:8]}")
    long_term_objective: str
    short_term_milestones: List[str] = Field(default_factory=list)
    adaptive_alternatives: List[str] = Field(default_factory=list)
    estimated_completion_days: int = 30


class ConstraintRule(BaseModel):
    """Decision constraint rule."""

    constraint_id: str = Field(default_factory=lambda: f"const_{uuid.uuid4().hex[:8]}")
    constraint_type: str = "budget"  # time, budget, resource, policy, priority
    limit_value: Any
    is_satisfied: bool = True


class RiskAssessmentReport(BaseModel):
    """Risk evaluation report."""

    risk_id: str = Field(default_factory=lambda: f"risk_{uuid.uuid4().hex[:8]}")
    failure_probability: float = 0.05
    overall_confidence: float = 0.95
    identified_risks: List[str] = Field(default_factory=list)
    mitigation_strategies: List[str] = Field(default_factory=list)


class ScenarioSimulation(BaseModel):
    """Scenario simulation result."""

    simulation_id: str = Field(default_factory=lambda: f"sim_{uuid.uuid4().hex[:8]}")
    best_case_outcome: str
    expected_case_outcome: str
    worst_case_outcome: str
    simulation_confidence: float = 0.92


class DecisionScoreCard(BaseModel):
    """Multi-factor decision scorecard."""

    expected_value_score: float = 0.95
    confidence_score: float = 0.94
    risk_score: float = 0.05
    cost_efficiency_score: float = 0.92
    time_efficiency_score: float = 0.90
    success_probability: float = 0.95
    composite_score: float = 0.94


class ResourceOptimizationPlan(BaseModel):
    """Compute and resource allocation plan."""

    plan_id: str = Field(default_factory=lambda: f"resplan_{uuid.uuid4().hex[:8]}")
    optimal_model: str = "llama-3.3-70b-versatile"
    recommended_workers: int = 16
    memory_allocation_mb: int = 1024
    parallel_execution_enabled: bool = True


class OpportunityInsight(BaseModel):
    """Discovered strategic opportunity."""

    opportunity_id: str = Field(default_factory=lambda: f"opp_{uuid.uuid4().hex[:8]}")
    title: str
    category: str = "efficiency"  # efficiency, automation, knowledge, optimization
    suggested_action: str
    estimated_value_gain: float = 0.20


class DecisionMemoryRecord(BaseModel):
    """Record of a past decision and outcome."""

    record_id: str = Field(default_factory=lambda: f"dmr_{uuid.uuid4().hex[:8]}")
    decision_topic: str
    action_taken: str
    outcome_status: str = "SUCCESS"
    lessons_learned: List[str] = Field(default_factory=list)
    timestamp: float = Field(default_factory=time.time)


class DecisionAnalyticsSummary(BaseModel):
    """Summary of Decision Intelligence platform performance."""

    decision_accuracy_pct: float = 98.5
    planning_quality_score: float = 0.95
    risk_prediction_accuracy: float = 0.94
    optimization_gain_pct: float = 24.5
    execution_success_rate: float = 0.98
