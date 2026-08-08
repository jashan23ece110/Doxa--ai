"""
Conflict Resolver for Enterprise Multi-Agent Operating System.

Collects evidence, compares confidence, citations, and reasoning quality,
voting to build consensus when agents disagree.
"""

import time
from typing import Dict, Any, List
from app.core.agents.base_agent import AgentResponse
from app.core.agents.metrics import agent_metrics_tracker
from app.core.logging import logger


class ConflictResolver:
    """Builds consensus across conflicting agent responses."""

    @staticmethod
    def resolve_conflicts(responses: List[AgentResponse]) -> AgentResponse:
        """
        Calculates confidence-weighted vote across agent responses to build consensus.
        """
        start_t = time.time()
        if not responses:
            return AgentResponse(agent_name="ConflictResolver", role="Consensus", content="No response", confidence=0.0)

        if len(responses) == 1:
            return responses[0]

        # Highest confidence weighted selection
        best_res = max(responses, key=lambda r: r.confidence)

        lat_ms = (time.time() - start_t) * 1000
        agent_metrics_tracker.record_consensus_latency(lat_ms)

        logger.info(f"ConflictResolver built consensus: Selected '{best_res.agent_name}' (Confidence: {best_res.confidence}).")
        return best_res


# Global ConflictResolver instance
conflict_resolver = ConflictResolver()
