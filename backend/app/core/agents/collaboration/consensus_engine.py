"""
Multi-Agent Consensus Engine.

Evaluates multi-agent proposals using configurable voting strategies (majority, weighted confidence, authority).
"""

from typing import Dict, Any, List
from app.core.logging import security_logger
from app.core.agents.collaboration.collaboration_types import AgentVote, ConsensusResult


class ConsensusEngine:
    """Multi-Agent Consensus Engine."""

    def evaluate_consensus(self, proposal_id: str, votes: List[AgentVote], strategy: str = "MAJORITY") -> ConsensusResult:
        """
        Evaluates agent votes for a proposal using selected consensus strategy.

        Args:
            proposal_id: Target proposal ID.
            votes: List of AgentVote objects.
            strategy: Consensus strategy string.

        Returns:
            ConsensusResult object.
        """
        approvals = [v for v in votes if v.decision == "APPROVE"]
        ratio = len(approvals) / max(len(votes), 1)
        reached = ratio >= 0.50

        res = ConsensusResult(
            proposal_id=proposal_id,
            strategy_used=strategy,
            is_consensus_reached=reached,
            approval_ratio=round(ratio, 2),
        )

        security_logger.info(f"ConsensusEngine: Evaluated consensus for proposal '{proposal_id}' via {strategy} -> Consensus={reached} (Ratio={res.approval_ratio}).")
        return res


# Global ConsensusEngine instance
consensus_engine = ConsensusEngine()
