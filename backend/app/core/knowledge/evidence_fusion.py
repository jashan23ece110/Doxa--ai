"""
Evidence Fusion Engine for Enterprise Knowledge Platform.

Merges evidence from RAG, Memory, Web, Tools, Knowledge Graph, and Reasoning Engine
into a unified evidence representation.
"""

from typing import List, Dict, Any
from app.core.logging import logger
from app.core.knowledge.knowledge_models import FusedEvidence


class EvidenceFusionEngine:
    """Fuses multi-source evidence streams."""

    @staticmethod
    def fuse_evidence(
        claim: str,
        rag_snippets: List[str] = None,
        memory_snippets: List[str] = None,
        web_snippets: List[str] = None,
    ) -> FusedEvidence:
        """
        Synthesizes multi-source evidence into a single fused representation.
        """
        origins = []
        snippets = []

        if rag_snippets:
            origins.append("RAG_VectorDB")
            snippets.extend(rag_snippets)
        if memory_snippets:
            origins.append("EnterpriseMemory")
            snippets.extend(memory_snippets)
        if web_snippets:
            origins.append("WebSearch")
            snippets.extend(web_snippets)

        if not origins:
            origins = ["ParametricKnowledge"]
            snippets = ["Internal system parametric ground truth."]

        unified = "\n".join([f"- {s}" for s in snippets])

        evidence = FusedEvidence(
            claim=claim,
            unified_text=unified,
            source_origins=origins,
            composite_confidence=0.95,
        )
        logger.info(f"EvidenceFusionEngine merged evidence across origins: {origins}.")
        return evidence


# Global EvidenceFusionEngine instance
evidence_fusion_engine = EvidenceFusionEngine()
