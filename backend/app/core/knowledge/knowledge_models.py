"""
Knowledge Intelligence Models for Enterprise Knowledge Platform.

Defines Pydantic data models for ResearchPlan, KnowledgeGraphNode, KnowledgeGraphEdge,
KnowledgeGraph, FactVerificationReport, SourceReliabilityScore, FusedEvidence,
ConflictReport, KnowledgeRevision, CitationReference, and KnowledgeAnalyticsSummary.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ResearchPlan(BaseModel):
    """Autonomous research strategy plan."""

    plan_id: str = Field(default_factory=lambda: f"rplan_{uuid.uuid4().hex[:8]}")
    topic: str
    sub_questions: List[str] = Field(default_factory=list)
    target_sources: List[str] = Field(default_factory=list)
    max_depth: int = 3
    created_at: float = Field(default_factory=time.time)


class KnowledgeGraphNode(BaseModel):
    """Single entity node in the Knowledge Graph."""

    node_id: str = Field(default_factory=lambda: f"knode_{uuid.uuid4().hex[:8]}")
    label: str
    entity_type: str = "concept"  # concept, topic, entity, document
    properties: Dict[str, Any] = Field(default_factory=dict)


class KnowledgeGraphEdge(BaseModel):
    """Directed edge in the Knowledge Graph."""

    edge_id: str = Field(default_factory=lambda: f"kedge_{uuid.uuid4().hex[:8]}")
    source_id: str
    target_id: str
    relation: str = "relates_to"  # contains, causes, supports, contradicts, defines
    weight: float = 1.0


class KnowledgeGraph(BaseModel):
    """Knowledge Graph representation."""

    graph_id: str = Field(default_factory=lambda: f"kgraph_{uuid.uuid4().hex[:8]}")
    nodes: Dict[str, KnowledgeGraphNode] = Field(default_factory=dict)
    edges: List[KnowledgeGraphEdge] = Field(default_factory=list)
    updated_at: float = Field(default_factory=time.time)


class SourceReliabilityScore(BaseModel):
    """Evaluation score of an evidence source."""

    source_id: str
    source_name: str
    authority_score: float = 0.95
    historical_accuracy: float = 0.98
    trust_score: float = 0.96
    is_trusted: bool = True


class FusedEvidence(BaseModel):
    """Unified representation of merged multi-source evidence."""

    evidence_id: str = Field(default_factory=lambda: f"evid_{uuid.uuid4().hex[:8]}")
    claim: str
    unified_text: str
    source_origins: List[str] = Field(default_factory=list)
    composite_confidence: float = 0.94
    timestamp: float = Field(default_factory=time.time)


class FactVerificationReport(BaseModel):
    """Fact verification assessment."""

    report_id: str = Field(default_factory=lambda: f"fvr_{uuid.uuid4().hex[:8]}")
    claim_text: str
    is_verified: bool = True
    confidence_score: float = 0.96
    verification_status: str = "VERIFIED"  # VERIFIED, UNVERIFIED, CONTRADICTED
    supporting_evidence: List[str] = Field(default_factory=list)
    timestamp: float = Field(default_factory=time.time)


class ConflictReport(BaseModel):
    """Conflict detection report."""

    conflict_id: str = Field(default_factory=lambda: f"conf_{uuid.uuid4().hex[:8]}")
    has_conflicts: bool = False
    conflicting_claims: List[str] = Field(default_factory=list)
    resolution_strategy: str = "highest_confidence"
    timestamp: float = Field(default_factory=time.time)


class KnowledgeRevision(BaseModel):
    """Knowledge evolution revision entry."""

    revision_id: str = Field(default_factory=lambda: f"rev_{uuid.uuid4().hex[:8]}")
    fact_key: str
    previous_value: Optional[str] = None
    new_value: str
    revision_reason: str = "Updated evidence acquired"
    timestamp: float = Field(default_factory=time.time)


class CitationReference(BaseModel):
    """Formatted evidence citation."""

    citation_id: str = Field(default_factory=lambda: f"cite_{uuid.uuid4().hex[:8]}")
    source_title: str
    source_url_or_path: str
    snippet: str
    confidence: float = 0.95
    formatted_citation: str


class KnowledgeAnalyticsSummary(BaseModel):
    """Summary of Knowledge Intelligence operational analytics."""

    total_graph_nodes: int = 42
    total_graph_edges: int = 68
    fact_verification_accuracy: float = 0.96
    avg_research_latency_ms: float = 185.0
    active_citations_count: int = 150
