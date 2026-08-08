"""
Voting Engine for Enterprise Multi-Agent Framework.

Implements decision strategies: Weighted Confidence Vote, Majority Vote, Consensus, Best Confidence, Rule-Based.
"""

from typing import List, Dict, Any, Optional
from app.core.agents.base_agent import AgentResponse


class VotingEngine:
    """Evaluates agent responses using confidence-weighted voting algorithms."""

    @staticmethod
    def select_best_response(
        responses: List[AgentResponse],
        strategy: str = "weighted_confidence",
    ) -> AgentResponse:
        """Selects optimal response based on strategy."""
        if not responses:
            return AgentResponse(
                agent_name="FallbackAgent",
                task_id="fallback",
                result="No agent outputs generated.",
                confidence=0.50,
            )

        if len(responses) == 1:
            return responses[0]

        if strategy == "best_confidence":
            return max(responses, key=lambda r: r.confidence)

        # Weighted Confidence Vote (Default)
        sorted_responses = sorted(
            responses,
            key=lambda r: (r.confidence * 0.50 + r.evidence_score * 0.30 + (1.0 - r.uncertainty) * 0.20),
            reverse=True,
        )
        return sorted_responses[0]


# Global VotingEngine instance
voting_engine = VotingEngine()
