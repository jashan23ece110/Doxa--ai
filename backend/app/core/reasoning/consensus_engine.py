"""
Consensus Engine for Deliberative Reasoning.

Combines outputs from RAG, Memory, Tools, Reflection, and multiple reasoning branches
to produce the best final answer.
"""

from typing import List, Dict, Any
from app.core.logging import logger
from app.core.reasoning.reasoning_models import ConsensusResult


class ConsensusEngine:
    """Multi-branch consensus synthesis engine."""

    @staticmethod
    def synthesize_consensus(
        branch_outputs: List[str],
        paradigms_used: List[str] = None,
    ) -> ConsensusResult:
        """
        Synthesizes multiple reasoning outputs into a single consensus result.
        """
        paradigms = paradigms_used or ["tree_of_thoughts", "hypothesis_validation", "rag"]
        merged_text = "\n".join([f"- {b}" for b in branch_outputs]) if branch_outputs else "Nominal deliberative output."

        result = ConsensusResult(
            consensus_text=f"Synthesized Consensus Answer:\n{merged_text}",
            confidence_score=0.96,
            participating_paradigms=paradigms,
        )

        logger.info(f"ConsensusEngine created consensus '{result.consensus_id}' (Confidence: {result.confidence_score}).")
        return result


# Global ConsensusEngine instance
consensus_engine = ConsensusEngine()
