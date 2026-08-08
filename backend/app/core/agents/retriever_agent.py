"""Retriever Agent Implementation."""
import time
from app.core.agents.base_agent import BaseAgent, AgentResponse
from app.core.agents.workspace import SharedWorkingMemory


class RetrieverAgent(BaseAgent):
    """Executes Hybrid RAG retrieval (Dense + BM25 + Rerank)."""

    def __init__(self, agent_id: str = "agent_retriever"):
        super().__init__(agent_id=agent_id, name="RetrieverAgent", role="Hybrid RAG Document Retriever")

    async def execute(self, prompt: str, workspace: SharedWorkingMemory) -> AgentResponse:
        start = time.time()
        # Lazy import to avoid circular dependency
        from app.services.document_service import document_service
        contexts = await document_service.retrieve_context(prompt, n_results=3)
        duration_ms = (time.time() - start) * 1000

        top_similarity = contexts[0].get("similarity", 0.80) if contexts else 0.50

        res = AgentResponse(
            agent_name=self.name,
            task_id="retrieval_task",
            result=contexts,
            confidence=top_similarity,
            evidence_score=top_similarity,
            latency_ms=duration_ms,
        )
        workspace.add_result(self.name, contexts)
        return res
