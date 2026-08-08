"""
Enterprise Multi-Source Intelligence Fusion & Knowledge Graph Package Initialization.
"""

from app.core.data_intelligence.fusion.entity_resolution import (
    entity_resolution_engine,
    EntityResolutionEngine,
    ResolvedEntity,
)
from app.core.data_intelligence.fusion.data_normalizer import (
    data_normalizer,
    DataNormalizer,
    NormalizedRecord,
)
from app.core.data_intelligence.fusion.semantic_enrichment import (
    semantic_enrichment_engine,
    SemanticEnrichmentEngine,
    EnrichedDataset,
)
from app.core.data_intelligence.fusion.intelligence_fusion import (
    multi_source_fusion_engine,
    MultiSourceIntelligenceFusionEngine,
)
from app.core.data_intelligence.fusion.cross_source_correlation import (
    cross_source_correlation_engine,
    CrossSourceCorrelationEngine,
    CorrelationFinding,
)
from app.core.data_intelligence.fusion.knowledge_graph_builder import (
    knowledge_graph_builder,
    KnowledgeGraphBuilder,
    KnowledgeGraphNode,
    KnowledgeGraphEdge,
)
from app.core.data_intelligence.fusion.graph_query_engine import (
    graph_query_engine,
    GraphQueryEngine,
    GraphQueryResult,
)
from app.core.data_intelligence.fusion.provenance_manager import (
    provenance_manager,
    ProvenanceManager,
    ProvenanceRecord,
)
from app.core.data_intelligence.fusion.conflict_resolution import (
    conflict_resolution_engine,
    ConflictResolutionEngine,
    ConflictResolutionDecision,
)
from app.core.data_intelligence.fusion.fusion_analytics import (
    fusion_analytics,
    FusionAnalytics,
    FusionAnalyticsSnapshot,
)

__all__ = [
    "entity_resolution_engine",
    "EntityResolutionEngine",
    "ResolvedEntity",
    "data_normalizer",
    "DataNormalizer",
    "NormalizedRecord",
    "semantic_enrichment_engine",
    "SemanticEnrichmentEngine",
    "EnrichedDataset",
    "multi_source_fusion_engine",
    "MultiSourceIntelligenceFusionEngine",
    "cross_source_correlation_engine",
    "CrossSourceCorrelationEngine",
    "CorrelationFinding",
    "knowledge_graph_builder",
    "KnowledgeGraphBuilder",
    "KnowledgeGraphNode",
    "KnowledgeGraphEdge",
    "graph_query_engine",
    "GraphQueryEngine",
    "GraphQueryResult",
    "provenance_manager",
    "ProvenanceManager",
    "ProvenanceRecord",
    "conflict_resolution_engine",
    "ConflictResolutionEngine",
    "ConflictResolutionDecision",
    "fusion_analytics",
    "FusionAnalytics",
    "FusionAnalyticsSnapshot",
]
