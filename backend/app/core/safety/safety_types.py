"""
Enterprise AI Safety Types for the Safety, Governance, Compliance & Trust Layer.

Defines Pydantic data models for SafetyEvent, RiskAssessment, PolicyViolation,
GovernanceDecision, SafetyAuditRecord, ComplianceResult, TrustScore,
ExecutionRisk, AgentDecisionRecord, SafetyPolicy, SafetyRule, PIIDetection,
RedactionResult, ExplainabilityReport, and supporting enums.
"""

import time
import uuid
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class RiskLevel(str, Enum):
    """Risk severity levels."""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SafetyVerdict(str, Enum):
    """Outcome verdict from safety evaluation."""
    SAFE = "safe"
    CAUTION = "caution"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"


class GovernanceAction(str, Enum):
    """Governance action types."""
    APPROVE = "approve"
    DENY = "deny"
    ESCALATE = "escalate"
    CONDITIONALLY_APPROVE = "conditionally_approve"


class ComplianceStandard(str, Enum):
    """Supported compliance standards."""
    GDPR = "GDPR"
    SOC2 = "SOC2"
    ISO27001 = "ISO27001"
    HIPAA = "HIPAA"


class PIICategory(str, Enum):
    """PII / sensitive information categories."""
    EMAIL = "email"
    PHONE = "phone"
    SSN = "ssn"
    CREDIT_CARD = "credit_card"
    ADDRESS = "address"
    NAME = "name"
    DATE_OF_BIRTH = "date_of_birth"
    IP_ADDRESS = "ip_address"
    MEDICAL = "medical"
    FINANCIAL = "financial"
    CREDENTIALS = "credentials"


class PolicyEffect(str, Enum):
    """Policy rule effect."""
    ALLOW = "allow"
    DENY = "deny"
    CONDITIONAL = "conditional"


class PolicyScope(str, Enum):
    """Scope to which a policy applies."""
    TOOL = "tool"
    MEMORY = "memory"
    RAG = "rag"
    EXECUTION = "execution"
    MODEL = "model"
    AGENT = "agent"
    WORKFLOW = "workflow"
    PLUGIN = "plugin"
    MCP = "mcp"
    GLOBAL = "global"


# ---------------------------------------------------------------------------
# Core Safety Event & Risk Models
# ---------------------------------------------------------------------------

class SafetyEvent(BaseModel):
    """Represents a safety-relevant event in the platform."""
    event_id: str = Field(default_factory=lambda: f"sev_{uuid.uuid4().hex[:10]}")
    event_type: str  # tool_execution, memory_access, retrieval, agent_action, llm_call
    source_component: str  # which subsystem generated the event
    actor_id: str = "system"
    user_id: str = "anonymous"
    agent_id: Optional[str] = None
    request_id: Optional[str] = None
    tenant_id: str = "default"
    risk_level: RiskLevel = RiskLevel.NONE
    verdict: SafetyVerdict = SafetyVerdict.SAFE
    description: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=time.time)


class ExecutionRisk(BaseModel):
    """Quantified risk for a specific execution path."""
    risk_id: str = Field(default_factory=lambda: f"risk_{uuid.uuid4().hex[:8]}")
    category: str  # tool_chain, recursive_loop, privilege_escalation, data_leak, injection
    risk_score: float = 0.0  # 0.0–1.0
    risk_level: RiskLevel = RiskLevel.NONE
    description: str = ""
    affected_components: List[str] = Field(default_factory=list)
    mitigation: str = ""
    detected_at: float = Field(default_factory=time.time)


class RiskAssessment(BaseModel):
    """Complete risk assessment for an execution request."""
    assessment_id: str = Field(default_factory=lambda: f"ra_{uuid.uuid4().hex[:8]}")
    overall_risk_score: float = 0.0  # 0.0–1.0
    overall_risk_level: RiskLevel = RiskLevel.NONE
    individual_risks: List[ExecutionRisk] = Field(default_factory=list)
    is_acceptable: bool = True
    requires_human_review: bool = False
    assessed_at: float = Field(default_factory=time.time)
    assessment_duration_ms: float = 0.0


# ---------------------------------------------------------------------------
# Policy Models
# ---------------------------------------------------------------------------

class SafetyRule(BaseModel):
    """Individual safety policy rule."""
    rule_id: str = Field(default_factory=lambda: f"sr_{uuid.uuid4().hex[:8]}")
    name: str
    scope: PolicyScope
    effect: PolicyEffect = PolicyEffect.ALLOW
    resource_pattern: str = "*"  # glob pattern or exact match
    conditions: Dict[str, Any] = Field(default_factory=dict)
    # Conditions can include: roles, tenants, time_windows, risk_threshold, model_whitelist, etc.
    priority: int = 100  # higher = evaluated first
    enabled: bool = True
    description: str = ""


class SafetyPolicy(BaseModel):
    """Collection of safety rules for a scope."""
    policy_id: str = Field(default_factory=lambda: f"sp_{uuid.uuid4().hex[:8]}")
    name: str
    scope: PolicyScope
    rules: List[SafetyRule] = Field(default_factory=list)
    version: int = 1
    created_at: float = Field(default_factory=time.time)


class PolicyViolation(BaseModel):
    """Record of a policy violation."""
    violation_id: str = Field(default_factory=lambda: f"pv_{uuid.uuid4().hex[:8]}")
    rule_id: str
    rule_name: str
    scope: PolicyScope
    effect: PolicyEffect
    actor_id: str = "system"
    user_id: str = "anonymous"
    resource: str = ""
    reason: str = ""
    severity: RiskLevel = RiskLevel.MEDIUM
    timestamp: float = Field(default_factory=time.time)


# ---------------------------------------------------------------------------
# Governance Models
# ---------------------------------------------------------------------------

class GovernanceDecision(BaseModel):
    """Result of a governance evaluation."""
    decision_id: str = Field(default_factory=lambda: f"gd_{uuid.uuid4().hex[:8]}")
    action: GovernanceAction = GovernanceAction.APPROVE
    resource_type: str  # tool, memory, workflow, agent, plugin, mcp
    resource_id: str = ""
    reason: str = ""
    policy_violations: List[PolicyViolation] = Field(default_factory=list)
    conditions: List[str] = Field(default_factory=list)  # for CONDITIONALLY_APPROVE
    decided_at: float = Field(default_factory=time.time)
    latency_ms: float = 0.0


# ---------------------------------------------------------------------------
# Trust Models
# ---------------------------------------------------------------------------

class TrustScore(BaseModel):
    """Composite trust score for an execution or response."""
    trust_id: str = Field(default_factory=lambda: f"ts_{uuid.uuid4().hex[:8]}")
    overall_score: float = 0.0  # 0.0–1.0
    tool_trust: float = 0.0
    memory_trust: float = 0.0
    retrieval_trust: float = 0.0
    hallucination_risk: float = 0.0  # 0.0 = no risk, 1.0 = very likely
    citation_score: float = 0.0
    reasoning_consistency: float = 0.0
    execution_history_score: float = 0.0
    is_trustworthy: bool = True
    factors: Dict[str, float] = Field(default_factory=dict)
    computed_at: float = Field(default_factory=time.time)


# ---------------------------------------------------------------------------
# Compliance & PII Models
# ---------------------------------------------------------------------------

class PIIDetection(BaseModel):
    """A detected PII instance."""
    category: PIICategory
    matched_text: str = "[REDACTED]"  # redacted by default
    start_index: int = 0
    end_index: int = 0
    confidence: float = 0.0


class RedactionResult(BaseModel):
    """Result of PII redaction."""
    redaction_id: str = Field(default_factory=lambda: f"red_{uuid.uuid4().hex[:8]}")
    original_length: int = 0
    redacted_length: int = 0
    detections: List[PIIDetection] = Field(default_factory=list)
    pii_found: bool = False
    redacted_text: str = ""


class ComplianceResult(BaseModel):
    """Result of compliance evaluation."""
    result_id: str = Field(default_factory=lambda: f"cr_{uuid.uuid4().hex[:8]}")
    standard: ComplianceStandard
    is_compliant: bool = True
    violations: List[str] = Field(default_factory=list)
    pii_detections: List[PIIDetection] = Field(default_factory=list)
    redaction_applied: bool = False
    audit_metadata: Dict[str, Any] = Field(default_factory=dict)
    evaluated_at: float = Field(default_factory=time.time)


# ---------------------------------------------------------------------------
# Audit Models
# ---------------------------------------------------------------------------

class SafetyAuditRecord(BaseModel):
    """Immutable audit record for AI Safety layer."""
    audit_id: str = Field(default_factory=lambda: f"saud_{uuid.uuid4().hex[:10]}")
    timestamp: float = Field(default_factory=time.time)
    actor: str = "system"
    user_id: str = "anonymous"
    agent_id: Optional[str] = None
    tool_id: Optional[str] = None
    request_id: Optional[str] = None
    decision: str = "approved"  # approved, denied, escalated, blocked
    risk_score: float = 0.0
    trust_score: float = 1.0
    latency_ms: float = 0.0
    outcome: str = "success"  # success, failure, timeout, error
    event_type: str = "general"
    details: Dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Agent Decision Record
# ---------------------------------------------------------------------------

class AgentDecisionRecord(BaseModel):
    """Records an agent's decision for governance and explainability."""
    record_id: str = Field(default_factory=lambda: f"adr_{uuid.uuid4().hex[:8]}")
    agent_id: str
    decision_type: str  # tool_selection, memory_read, retrieval, workflow_step, model_selection
    chosen_option: str
    alternatives_considered: List[str] = Field(default_factory=list)
    reasoning_summary: str = ""
    confidence: float = 0.0
    risk_assessment: Optional[RiskAssessment] = None
    trust_score: Optional[TrustScore] = None
    governance_decision: Optional[GovernanceDecision] = None
    timestamp: float = Field(default_factory=time.time)


# ---------------------------------------------------------------------------
# Explainability Models
# ---------------------------------------------------------------------------

class ExplainabilityReport(BaseModel):
    """Structured explanation of AI decisions without exposing chain-of-thought."""
    report_id: str = Field(default_factory=lambda: f"expl_{uuid.uuid4().hex[:8]}")
    request_id: Optional[str] = None
    tool_selection_rationale: List[str] = Field(default_factory=list)
    memory_usage_rationale: List[str] = Field(default_factory=list)
    retrieval_rationale: List[str] = Field(default_factory=list)
    workflow_rationale: List[str] = Field(default_factory=list)
    model_selection_rationale: List[str] = Field(default_factory=list)
    confidence_explanation: str = ""
    risk_explanation: str = ""
    trust_explanation: str = ""
    generated_at: float = Field(default_factory=time.time)
