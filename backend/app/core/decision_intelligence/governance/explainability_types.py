"""
Explainable AI, Decision Governance & Trust Types & Data Schemas.

Comprehensive Pydantic models for ExplanationRequest, Explanation, EvidenceContribution,
FeatureContribution, DecisionFactor, ModelReasoning, UncertaintyExplanation, CounterfactualScenario,
DecisionTrace, DecisionLineage, GovernancePolicy, GovernanceViolation, HumanReview,
ApprovalRequest, ApprovalDecision, AuditRecord, TrustScore, and GovernanceMetrics.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class EvidenceContribution(BaseModel):
    contribution_id: str = Field(default_factory=lambda: f"econtrib_{uuid.uuid4().hex[:8]}")
    source_name: str
    weight: float = 0.40
    summary: str = "Knowledge Graph node corroborates historical success"


class FeatureContribution(BaseModel):
    feature_name: str
    contribution_score: float = 0.35
    impact_direction: str = "POSITIVE"  # POSITIVE, NEGATIVE, NEUTRAL


class DecisionFactor(BaseModel):
    factor_name: str
    importance: float = 0.85
    description: str = ""


class ModelReasoning(BaseModel):
    model_type: str = "GRADIENT_BOOSTING_ENSEMBLE"
    top_features: List[FeatureContribution] = Field(default_factory=list)
    rationale: str = "High positive contribution from historical ROI feature."


class UncertaintyExplanation(BaseModel):
    overall_uncertainty_score: float = 0.08
    key_uncertainty_drivers: List[str] = Field(default_factory=list)
    confidence_interval_note: str = "95% confidence interval [85.0, 115.0]"


class CounterfactualScenario(BaseModel):
    counterfactual_id: str = Field(default_factory=lambda: f"cfact_{uuid.uuid4().hex[:8]}")
    modified_parameter: str
    original_val: Any
    hypothetical_val: Any
    resulting_outcome_delta: str
    is_hypothetical: bool = True


class Explanation(BaseModel):
    explanation_id: str = Field(default_factory=lambda: f"expl_{uuid.uuid4().hex[:8]}")
    decision_id: str
    summary_rationale: str
    evidence_contributions: List[EvidenceContribution] = Field(default_factory=list)
    reasoning: ModelReasoning = Field(default_factory=ModelReasoning)
    uncertainty: UncertaintyExplanation = Field(default_factory=UncertaintyExplanation)
    counterfactuals: List[CounterfactualScenario] = Field(default_factory=list)
    created_at: float = Field(default_factory=time.time)


class ExplanationRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: f"ereq_{uuid.uuid4().hex[:8]}")
    decision_id: str
    depth: str = "DETAILED"  # SUMMARY, DETAILED, AUDIT
    created_at: float = Field(default_factory=time.time)


class DecisionTrace(BaseModel):
    trace_id: str = Field(default_factory=lambda: f"dtrc_{uuid.uuid4().hex[:8]}")
    step_name: str
    input_summary: str
    output_summary: str
    execution_time_ms: float = 0.10


class DecisionLineage(BaseModel):
    lineage_id: str = Field(default_factory=lambda: f"dlin_{uuid.uuid4().hex[:8]}")
    decision_id: str
    traces: List[DecisionTrace] = Field(default_factory=list)
    is_reproducible: bool = True
    recorded_at: float = Field(default_factory=time.time)


class GovernancePolicy(BaseModel):
    policy_id: str = Field(default_factory=lambda: f"gpol_{uuid.uuid4().hex[:8]}")
    name: str
    min_confidence_threshold: float = 0.80
    max_allowed_risk_score: float = 5.0
    requires_human_approval_over_cost: float = 10000.0
    version: str = "1.0.0"


class GovernanceViolation(BaseModel):
    violation_id: str = Field(default_factory=lambda: f"gviol_{uuid.uuid4().hex[:8]}")
    policy_name: str
    violation_reason: str
    severity: str = "MEDIUM"


class ApprovalRequest(BaseModel):
    approval_request_id: str = Field(default_factory=lambda: f"areq_{uuid.uuid4().hex[:8]}")
    decision_id: str
    action_title: str
    estimated_cost: float = 15000.0
    requester: str = "DecisionIntelligenceSystem"
    status: str = "PENDING_APPROVAL"  # PENDING_APPROVAL, APPROVED, REJECTED
    created_at: float = Field(default_factory=time.time)


class ApprovalDecision(BaseModel):
    decision_id: str = Field(default_factory=lambda: f"adec_{uuid.uuid4().hex[:8]}")
    approval_request_id: str
    approver_id: str = "EnterpriseAdmin"
    decision: str = "APPROVED"  # APPROVED, REJECTED
    reviewer_comments: str = "Approved after reviewing evidence and risk assessments."
    decided_at: float = Field(default_factory=time.time)


class HumanReview(BaseModel):
    review_id: str = Field(default_factory=lambda: f"hrev_{uuid.uuid4().hex[:8]}")
    approval_request: ApprovalRequest
    decision: Optional[ApprovalDecision] = None


class AuditRecord(BaseModel):
    record_id: str = Field(default_factory=lambda: f"audrec_{uuid.uuid4().hex[:8]}")
    event_type: str
    entity_id: str
    actor: str = "System"
    details: Dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=time.time)


class TrustScore(BaseModel):
    score_id: str = Field(default_factory=lambda: f"tscore_{uuid.uuid4().hex[:8]}")
    composite_trust: float = 0.94  # 0.0 to 1.0
    evidence_reliability: float = 0.96
    model_certainty: float = 0.95
    policy_compliance: float = 1.00
    provenance_integrity: float = 1.00
    calculated_at: float = Field(default_factory=time.time)


class GovernanceMetrics(BaseModel):
    approvals_requested_count: int = 0
    approvals_granted_count: int = 0
    policy_violations_detected_count: int = 0
    average_trust_score: float = 0.94
