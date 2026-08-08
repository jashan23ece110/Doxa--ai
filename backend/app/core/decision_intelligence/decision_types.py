"""
Enterprise Decision Intelligence Types & Data Schemas.

Comprehensive Pydantic models for DecisionRequest, DecisionObjective, DecisionContext,
DecisionConstraint, DecisionCriterion, DecisionAlternative, DecisionEvidence, DecisionFactor,
DecisionOutcome, DecisionRecommendation, DecisionConfidence, DecisionRisk, DecisionScenario,
DecisionEvaluation, DecisionAudit, and DecisionMetrics.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class DecisionObjective(BaseModel):
    objective_id: str = Field(default_factory=lambda: f"dobj_{uuid.uuid4().hex[:8]}")
    title: str
    target_metric: str
    target_value: float = 100.0
    weight: float = 1.0
    created_at: float = Field(default_factory=time.time)


class DecisionConstraint(BaseModel):
    constraint_id: str = Field(default_factory=lambda: f"dcnst_{uuid.uuid4().hex[:8]}")
    name: str
    constraint_type: str  # BUDGET, TIME, SECURITY, LEGAL, CAPACITY
    max_limit: float = 1000.0
    is_hard_constraint: bool = True


class DecisionCriterion(BaseModel):
    criterion_id: str = Field(default_factory=lambda: f"dcrit_{uuid.uuid4().hex[:8]}")
    name: str
    weight: float = 0.25
    evaluation_method: str = "WEIGHTED_SCORE"


class DecisionAlternative(BaseModel):
    alternative_id: str = Field(default_factory=lambda: f"alt_{uuid.uuid4().hex[:8]}")
    title: str
    description: str
    expected_benefit: float = 85.0
    expected_cost: float = 15.0
    risk_level: str = "LOW"  # LOW, MEDIUM, HIGH
    assumptions: List[str] = Field(default_factory=list)
    created_at: float = Field(default_factory=time.time)


class DecisionEvidence(BaseModel):
    evidence_id: str = Field(default_factory=lambda: f"devid_{uuid.uuid4().hex[:8]}")
    source_type: str  # KNOWLEDGE_GRAPH, RAG, DATA_INTELLIGENCE, AGENT_OBSERVATION
    fact_type: str = "FACT"  # FACT, INFERENCE, PREDICTION, ASSUMPTION
    content: str
    confidence_score: float = 0.95
    freshness_timestamp: float = Field(default_factory=time.time)


class DecisionFactor(BaseModel):
    factor_id: str = Field(default_factory=lambda: f"fact_{uuid.uuid4().hex[:8]}")
    name: str
    impact_score: float = 0.85
    description: str = ""


class DecisionConfidence(BaseModel):
    overall_confidence: float = 0.92  # 0.0 to 1.0
    evidence_quality_score: float = 0.95
    model_certainty_score: float = 0.90
    uncertainty_notes: str = "High data corroboration across multiple independent sources."


class DecisionRisk(BaseModel):
    risk_id: str = Field(default_factory=lambda: f"drisk_{uuid.uuid4().hex[:8]}")
    risk_type: str  # OPERATIONAL, FINANCIAL, SECURITY, COMPLIANCE
    impact: str = "LOW"  # LOW, MEDIUM, HIGH, CRITICAL
    probability: float = 0.10
    mitigation_strategy: str = "Standard rollback and monitoring controls"


class DecisionScenario(BaseModel):
    scenario_id: str = Field(default_factory=lambda: f"scen_{uuid.uuid4().hex[:8]}")
    name: str
    probability: float = 0.70
    outcome_multiplier: float = 1.0


class DecisionEvaluation(BaseModel):
    evaluation_id: str = Field(default_factory=lambda: f"deval_{uuid.uuid4().hex[:8]}")
    alternative_id: str
    composite_score: float = 92.5  # 0 to 100
    benefit_cost_ratio: float = 5.67
    risk_adjusted_score: float = 88.0
    evaluated_at: float = Field(default_factory=time.time)


class DecisionRecommendation(BaseModel):
    recommendation_id: str = Field(default_factory=lambda: f"rec_{uuid.uuid4().hex[:8]}")
    recommended_alternative_id: str
    recommended_alternative_title: str
    rationale: str
    expected_outcome_summary: str
    confidence: DecisionConfidence = Field(default_factory=DecisionConfidence)
    requires_human_approval: bool = True
    created_at: float = Field(default_factory=time.time)


class DecisionContext(BaseModel):
    context_id: str = Field(default_factory=lambda: f"dctx_{uuid.uuid4().hex[:8]}")
    request_id: str
    relevant_evidences: List[DecisionEvidence] = Field(default_factory=list)
    collected_at: float = Field(default_factory=time.time)


class DecisionRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: f"dreq_{uuid.uuid4().hex[:8]}")
    title: str
    description: str
    objectives: List[DecisionObjective] = Field(default_factory=list)
    constraints: List[DecisionConstraint] = Field(default_factory=list)
    requester_id: str = "EnterpriseUser"
    created_at: float = Field(default_factory=time.time)


class DecisionOutcome(BaseModel):
    outcome_id: str = Field(default_factory=lambda: f"dout_{uuid.uuid4().hex[:8]}")
    decision_id: str
    realized_benefit: float = 88.0
    realized_cost: float = 14.5
    was_successful: bool = True
    recorded_at: float = Field(default_factory=time.time)


class DecisionAudit(BaseModel):
    audit_id: str = Field(default_factory=lambda: f"daud_{uuid.uuid4().hex[:8]}")
    request_id: str
    lineage_steps: List[str] = Field(default_factory=list)
    model_version: str = "1.0.0"
    is_reproducible: bool = True
    audited_at: float = Field(default_factory=time.time)


class DecisionMetrics(BaseModel):
    decisions_processed_count: int = 0
    recommendations_generated_count: int = 0
    average_decision_latency_ms: float = 0.0
    average_confidence_score: float = 0.92
