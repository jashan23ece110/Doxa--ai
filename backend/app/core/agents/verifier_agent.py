"""Verifier Agent Implementation."""
import time
from app.core.agents.base_agent import BaseAgent, AgentResponse
from app.core.agents.workspace import SharedWorkingMemory
from app.core.reasoning.verifier import verification_engine


class VerifierAgent(BaseAgent):
    """Validates factual claims against retrieved context and memory."""

    def __init__(self, agent_id: str = "agent_verifier"):
        super().__init__(agent_id=agent_id, name="VerifierAgent", role="Factual Grounding Verifier")

    async def execute(self, prompt: str, workspace: SharedWorkingMemory) -> AgentResponse:
        start = time.time()
        contexts = workspace.results.get("RetrieverAgent", [])
        draft = workspace.results.get("WriterAgent", prompt)

        if isinstance(draft, dict):
            draft = str(draft)

        verification = verification_engine.verify_response_evidence(draft, contexts)
        duration_ms = (time.time() - start) * 1000

        res = AgentResponse(
            agent_name=self.name,
            task_id="verification_task",
            result=verification,
            confidence=0.95 if verification.get("verified") else 0.60,
            evidence_score=verification.get("grounded_ratio", 0.90),
            latency_ms=duration_ms,
        )
        workspace.add_result(self.name, verification)
        return res
