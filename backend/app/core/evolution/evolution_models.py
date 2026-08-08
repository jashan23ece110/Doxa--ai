"""
Evolution Intelligence Models for Enterprise Self-Optimization Platform.

Defines Pydantic data models for CapabilityProfile, CapabilityDimension,
SelfEvaluationScore, EvaluationMetric, OptimizationRecommendation,
OptimizationPlan, TuningParameter, TuningSnapshot, PerformanceLearningRecord,
LearningInsight, SystemRecommendation, RecommendationCategory,
ABExperiment, ExperimentVariant, EvolutionSnapshot, and EvolutionAnalyticsSummary.
"""

import time
import uuid
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class CapabilityDimension(str, Enum):
    """Measurable capability dimensions."""
    REASONING = "reasoning"
    MEMORY = "memory"
    RETRIEVAL = "retrieval"
    WORKFLOW = "workflow"
    TOOL_USE = "tool_use"
    KNOWLEDGE = "knowledge"
    DECISION = "decision"
    PLANNING = "planning"
    METACOGNITION = "metacognition"
    INTEGRATION = "integration"


class CapabilityScore(BaseModel):
    """Score for a single capability dimension."""
    dimension: CapabilityDimension
    score: float = 0.0  # 0.0 - 1.0
    confidence: float = 0.95
    sample_count: int = 0
    trend: str = "STABLE"  # IMPROVING, STABLE, DECLINING
    last_assessed: float = Field(default_factory=time.time)


class CapabilityProfile(BaseModel):
    """Complete capability profile across all dimensions."""
    profile_id: str = Field(default_factory=lambda: f"cap_{uuid.uuid4().hex[:8]}")
    scores: List[CapabilityScore] = Field(default_factory=list)
    overall_score: float = 0.0
    intelligence_quotient: float = 0.0  # Composite IQ-like metric
    maturity_level: str = "DEVELOPING"  # NASCENT, DEVELOPING, PROFICIENT, ADVANCED, EXPERT
    assessed_at: float = Field(default_factory=time.time)
    assessment_duration_ms: float = 0.0


class EvaluationMetric(BaseModel):
    """Single evaluation metric measurement."""
    metric_name: str
    value: float = 0.0
    target: float = 1.0
    weight: float = 1.0
    passed: bool = True
    details: str = ""


class SelfEvaluationScore(BaseModel):
    """Comprehensive self-evaluation result."""
    evaluation_id: str = Field(default_factory=lambda: f"eval_{uuid.uuid4().hex[:8]}")
    accuracy_score: float = 0.0
    latency_score: float = 0.0
    reliability_score: float = 0.0
    consistency_score: float = 0.0
    resource_efficiency_score: float = 0.0
    goal_completion_score: float = 0.0
    composite_score: float = 0.0
    metrics: List[EvaluationMetric] = Field(default_factory=list)
    evaluated_at: float = Field(default_factory=time.time)
    recommendations: List[str] = Field(default_factory=list)


class OptimizationRecommendation(BaseModel):
    """Single optimization recommendation."""
    recommendation_id: str = Field(default_factory=lambda: f"opt_{uuid.uuid4().hex[:8]}")
    target_component: str
    optimization_type: str  # prompt_routing, tool_selection, reasoning_depth, memory_retrieval, cache_usage
    current_value: Any = None
    recommended_value: Any = None
    expected_improvement_pct: float = 0.0
    confidence: float = 0.0
    priority: str = "MEDIUM"  # LOW, MEDIUM, HIGH, CRITICAL


class OptimizationPlan(BaseModel):
    """Complete optimization plan with multiple recommendations."""
    plan_id: str = Field(default_factory=lambda: f"plan_{uuid.uuid4().hex[:8]}")
    recommendations: List[OptimizationRecommendation] = Field(default_factory=list)
    estimated_total_improvement_pct: float = 0.0
    risk_level: str = "LOW"  # LOW, MEDIUM, HIGH
    created_at: float = Field(default_factory=time.time)
    approved: bool = False
    applied: bool = False


class TuningParameter(BaseModel):
    """A dynamically tunable system parameter."""
    parameter_name: str
    current_value: float = 0.0
    min_value: float = 0.0
    max_value: float = 1.0
    step_size: float = 0.01
    last_tuned: float = Field(default_factory=time.time)


class TuningSnapshot(BaseModel):
    """Snapshot of all tuned parameters at a point in time."""
    snapshot_id: str = Field(default_factory=lambda: f"tune_{uuid.uuid4().hex[:8]}")
    parameters: List[TuningParameter] = Field(default_factory=list)
    performance_before: float = 0.0
    performance_after: float = 0.0
    tuning_strategy: str = "GRADIENT_FREE"  # GRADIENT_FREE, BAYESIAN, RANDOM, GRID
    tuned_at: float = Field(default_factory=time.time)


class LearningInsight(BaseModel):
    """A learned insight from historical performance data."""
    insight_id: str = Field(default_factory=lambda: f"ins_{uuid.uuid4().hex[:8]}")
    category: str  # throughput, accuracy, latency, reliability, cost
    pattern_description: str
    actionable_recommendation: str
    confidence: float = 0.0
    evidence_count: int = 0
    discovered_at: float = Field(default_factory=time.time)


class PerformanceLearningRecord(BaseModel):
    """Record of performance learning extraction."""
    record_id: str = Field(default_factory=lambda: f"plr_{uuid.uuid4().hex[:8]}")
    insights: List[LearningInsight] = Field(default_factory=list)
    execution_logs_analyzed: int = 0
    benchmarks_compared: int = 0
    period_start: float = Field(default_factory=time.time)
    period_end: float = Field(default_factory=time.time)


class RecommendationCategory(str, Enum):
    """Categories for system recommendations."""
    ARCHITECTURE = "architecture"
    PERFORMANCE = "performance"
    SECURITY = "security"
    RELIABILITY = "reliability"
    COST = "cost"
    DEVELOPER_PRODUCTIVITY = "developer_productivity"


class SystemRecommendation(BaseModel):
    """Actionable system-wide recommendation."""
    recommendation_id: str = Field(default_factory=lambda: f"sysrec_{uuid.uuid4().hex[:8]}")
    category: RecommendationCategory = RecommendationCategory.PERFORMANCE
    title: str
    description: str
    impact_score: float = 0.0  # 0.0 - 1.0
    effort_score: float = 0.0  # 0.0 - 1.0 (lower = easier)
    priority_rank: int = 1
    status: str = "PROPOSED"  # PROPOSED, ACCEPTED, IMPLEMENTED, REJECTED
    created_at: float = Field(default_factory=time.time)


class ExperimentVariant(BaseModel):
    """A variant in an A/B experiment."""
    variant_id: str = Field(default_factory=lambda: f"var_{uuid.uuid4().hex[:8]}")
    name: str = "control"
    config_overrides: Dict[str, Any] = Field(default_factory=dict)
    sample_size: int = 0
    success_rate: float = 0.0
    avg_latency_ms: float = 0.0


class ABExperiment(BaseModel):
    """A/B experiment definition and results."""
    experiment_id: str = Field(default_factory=lambda: f"exp_{uuid.uuid4().hex[:8]}")
    name: str
    hypothesis: str
    variants: List[ExperimentVariant] = Field(default_factory=list)
    status: str = "DRAFT"  # DRAFT, RUNNING, COMPLETED, ROLLED_BACK
    winner_variant_id: Optional[str] = None
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    created_at: float = Field(default_factory=time.time)
    auto_rollback_enabled: bool = True
    rollback_threshold: float = 0.1  # Minimum degradation to trigger rollback


class EvolutionSnapshot(BaseModel):
    """Point-in-time snapshot of the platform's evolution state."""
    snapshot_id: str = Field(default_factory=lambda: f"snap_{uuid.uuid4().hex[:8]}")
    capability_profile: Optional[CapabilityProfile] = None
    evaluation_score: Optional[SelfEvaluationScore] = None
    active_experiments: List[str] = Field(default_factory=list)
    optimization_plans_applied: int = 0
    tuning_snapshots_count: int = 0
    learning_insights_count: int = 0
    recommendations_count: int = 0
    snapshot_at: float = Field(default_factory=time.time)


class EvolutionAnalyticsSummary(BaseModel):
    """Summary analytics for the evolution platform."""
    improvement_rate_pct: float = 0.0
    optimization_success_rate: float = 0.0
    capability_growth_rate: float = 0.0
    regression_avoidance_rate: float = 0.0
    experiments_completed: int = 0
    experiments_successful: int = 0
    total_recommendations: int = 0
    recommendations_implemented: int = 0
    total_tuning_cycles: int = 0
    insights_discovered: int = 0
