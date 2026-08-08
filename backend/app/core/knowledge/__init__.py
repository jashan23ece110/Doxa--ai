"""Knowledge package initialization."""
from app.core.knowledge.knowledge_models import (
    ResearchPlan,
    KnowledgeGraphNode,
    KnowledgeGraphEdge,
    KnowledgeGraph,
    SourceReliabilityScore,
    FusedEvidence,
    FactVerificationReport,
    ConflictReport,
    KnowledgeRevision,
    CitationReference,
    KnowledgeAnalyticsSummary,
)
from app.core.knowledge.research_engine import research_engine, AutonomousResearchEngine
from app.core.knowledge.knowledge_graph import knowledge_graph_engine, KnowledgeGraphEngine
from app.core.knowledge.fact_verifier import fact_verification_engine, FactVerificationEngine
from app.core.knowledge.source_reliability import source_reliability_engine, SourceReliabilityEngine
from app.core.knowledge.evidence_fusion import evidence_fusion_engine, EvidenceFusionEngine
from app.core.knowledge.conflict_detector import conflict_detection_engine, ConflictDetectionEngine
from app.core.knowledge.knowledge_evolution import knowledge_evolution_engine, KnowledgeEvolutionEngine
from app.core.knowledge.citation_manager import citation_manager, CitationManager
from app.core.knowledge.knowledge_cache import knowledge_cache, KnowledgeCache
from app.core.knowledge.knowledge_analytics import knowledge_analytics_tracker, KnowledgeAnalyticsTracker
from app.core.knowledge.knowledge_orchestrator import knowledge_orchestrator, KnowledgeOrchestrator

__all__ = [
    "ResearchPlan",
    "KnowledgeGraphNode",
    "KnowledgeGraphEdge",
    "KnowledgeGraph",
    "SourceReliabilityScore",
    "FusedEvidence",
    "FactVerificationReport",
    "ConflictReport",
    "KnowledgeRevision",
    "CitationReference",
    "KnowledgeAnalyticsSummary",
    "research_engine",
    "AutonomousResearchEngine",
    "knowledge_graph_engine",
    "KnowledgeGraphEngine",
    "fact_verification_engine",
    "FactVerificationEngine",
    "source_reliability_engine",
    "SourceReliabilityEngine",
    "evidence_fusion_engine",
    "EvidenceFusionEngine",
    "conflict_detection_engine",
    "ConflictDetectionEngine",
    "knowledge_evolution_engine",
    "KnowledgeEvolutionEngine",
    "citation_manager",
    "CitationManager",
    "knowledge_cache",
    "KnowledgeCache",
    "knowledge_analytics_tracker",
    "KnowledgeAnalyticsTracker",
    "knowledge_orchestrator",
    "KnowledgeOrchestrator",
]
