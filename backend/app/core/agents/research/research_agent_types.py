"""
Enterprise Autonomous Research Agent Types & Data Schemas.

Comprehensive Pydantic models for ResearchAgent, ResearchGoal, ResearchQuestion, ResearchPlan,
ResearchTask, InformationSource, SourceEvidence, EvidenceChain, SourceReliability, ResearchFinding,
KnowledgeGap, ResearchHypothesis, HypothesisTest, ResearchSynthesis, ResearchReport, and ResearchMetrics.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class InformationSource(BaseModel):
    source_id: str = Field(default_factory=lambda: f"src_{uuid.uuid4().hex[:8]}")
    name: str
    source_type: str  # ENTERPRISE_DOC, APPROVED_API, KNOWLEDGE_GRAPH, INTERNAL_DATASET
    access_uri: str
    is_authorized: bool = True
    authority_score: float = 0.95
    created_at: float = Field(default_factory=time.time)


class SourceEvidence(BaseModel):
    evidence_id: str = Field(default_factory=lambda: f"evid_{uuid.uuid4().hex[:8]}")
    source_id: str
    content_snippet: str
    citation_reference: str
    confidence_score: float = 0.92
    retrieved_at: float = Field(default_factory=time.time)


class EvidenceChain(BaseModel):
    chain_id: str = Field(default_factory=lambda: f"echain_{uuid.uuid4().hex[:8]}")
    evidences: List[SourceEvidence] = Field(default_factory=list)
    overall_confidence: float = 0.94


class SourceReliability(BaseModel):
    assessment_id: str = Field(default_factory=lambda: f"srel_{uuid.uuid4().hex[:8]}")
    source_id: str
    reliability_score: float = 0.96  # 0.0 (Untrusted) to 1.0 (Highly Trusted)
    explainability_notes: str = "Authorized enterprise database with verified provenance."
    evaluated_at: float = Field(default_factory=time.time)


class ResearchQuestion(BaseModel):
    question_id: str = Field(default_factory=lambda: f"rq_{uuid.uuid4().hex[:8]}")
    question_text: str
    priority: int = 1
    status: str = "ANSWERED"  # OPEN, IN_PROGRESS, ANSWERED


class ResearchTask(BaseModel):
    task_id: str = Field(default_factory=lambda: f"rtask_{uuid.uuid4().hex[:8]}")
    question_id: str
    target_source_id: Optional[str] = None
    query_string: str
    status: str = "COMPLETED"


class ResearchPlan(BaseModel):
    plan_id: str = Field(default_factory=lambda: f"rplan_{uuid.uuid4().hex[:8]}")
    goal_id: str
    questions: List[ResearchQuestion] = Field(default_factory=list)
    tasks: List[ResearchTask] = Field(default_factory=list)
    created_at: float = Field(default_factory=time.time)


class ResearchFinding(BaseModel):
    finding_id: str = Field(default_factory=lambda: f"rfind_{uuid.uuid4().hex[:8]}")
    title: str
    summary: str
    verification_status: str = "VERIFIED"  # VERIFIED, STRONGLY_SUPPORTED, PARTIALLY_SUPPORTED, CONFLICTING
    supporting_evidence: List[SourceEvidence] = Field(default_factory=list)
    citations: List[str] = Field(default_factory=list)


class KnowledgeGap(BaseModel):
    gap_id: str = Field(default_factory=lambda: f"kgap_{uuid.uuid4().hex[:8]}")
    description: str
    impact_level: str = "MEDIUM"  # LOW, MEDIUM, HIGH
    recommended_action: str = "Search external authorized APIs"


class ResearchHypothesis(BaseModel):
    hypothesis_id: str = Field(default_factory=lambda: f"rhyp_{uuid.uuid4().hex[:8]}")
    statement: str
    confidence_score: float = 0.88
    supporting_evidence_ids: List[str] = Field(default_factory=list)


class HypothesisTest(BaseModel):
    test_id: str = Field(default_factory=lambda: f"htest_{uuid.uuid4().hex[:8]}")
    hypothesis_id: str
    is_confirmed: bool = True
    test_notes: str = "Validated against historical knowledge graph records."


class ResearchSynthesis(BaseModel):
    synthesis_id: str = Field(default_factory=lambda: f"synth_{uuid.uuid4().hex[:8]}")
    findings: List[ResearchFinding] = Field(default_factory=list)
    hypotheses: List[ResearchHypothesis] = Field(default_factory=list)
    knowledge_gaps: List[KnowledgeGap] = Field(default_factory=list)
    synthesized_at: float = Field(default_factory=time.time)


class ResearchGoal(BaseModel):
    goal_id: str = Field(default_factory=lambda: f"rgoal_{uuid.uuid4().hex[:8]}")
    topic: str
    objective: str
    status: str = "IN_PROGRESS"
    created_at: float = Field(default_factory=time.time)


class ResearchReport(BaseModel):
    report_id: str = Field(default_factory=lambda: f"rep_{uuid.uuid4().hex[:8]}")
    goal_id: str
    title: str
    executive_summary: str
    methodology: str
    findings: List[ResearchFinding] = Field(default_factory=list)
    knowledge_gaps: List[KnowledgeGap] = Field(default_factory=list)
    conclusions: str
    citations: List[str] = Field(default_factory=list)
    overall_confidence: float = 0.95
    generated_at: float = Field(default_factory=time.time)


class ResearchMetrics(BaseModel):
    goals_processed_count: int = 0
    sources_discovered_count: int = 0
    evidences_retrieved_count: int = 0
    reports_generated_count: int = 0
    average_research_latency_ms: float = 0.0


class ResearchAgent(BaseModel):
    agent_id: str = Field(default_factory=lambda: f"ragent_{uuid.uuid4().hex[:8]}")
    name: str = "AutonomousResearchScientist"
    role: str = "RESEARCHER"
    capabilities: List[str] = Field(default_factory=lambda: ["source_discovery", "evidence_retrieval", "synthesis", "report_generation"])
    is_active: bool = True
