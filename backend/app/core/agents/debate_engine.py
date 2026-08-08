"""
Debate Engine for Enterprise Multi-Agent Framework.

Conducts multi-round structured debates between Reasoning and Critic agents.
"""

from typing import List, Dict, Any
from app.core.agents.base_agent import AgentResponse
from app.core.agents.communication_bus import communication_bus, AgentMessage
from app.core.agents.workspace import SharedWorkingMemory
from app.core.logging import logger


class DebateEngine:
    """Orchestrates structured debate rounds between reasoning and critic agents."""

    async def conduct_debate(
        self,
        prompt: str,
        reasoning_response: AgentResponse,
        critic_response: AgentResponse,
        workspace: SharedWorkingMemory,
        rounds: int = 1,
    ) -> Dict[str, Any]:
        """Conducts structured debate rounds."""
        logger.info(f"Initiating {rounds}-round debate between ReasoningAgent and CriticAgent.")

        debate_trace = []
        for r in range(1, rounds + 1):
            claim = reasoning_response.result
            critique = critic_response.result

            communication_bus.publish(
                AgentMessage(
                    sender="debate_engine",
                    recipient="all",
                    msg_type="critique_request",
                    content={"round": r, "claim": claim, "critique": critique},
                )
            )

            debate_trace.append(
                {
                    "round": r,
                    "reasoning_claim": claim,
                    "critic_review": critique,
                    "outcome": "consensus_reached" if critic_response.confidence > 0.85 else "revisions_applied",
                }
            )

        workspace.add_result("DebateEngine", debate_trace)
        return {"debate_trace": debate_trace, "rounds": rounds, "status": "completed"}


# Global DebateEngine instance
debate_engine = DebateEngine()
