"""
Researcher Agent Implementation.

Executes evidence gathering across Hybrid RAG, BM25, and Tavily web search.
"""

from typing import Dict, Any
from app.core.agents.base import BaseAgent
from app.core.agents.workspace import SharedWorkingMemory
from app.services.document_service import document_service


class ResearcherAgent(BaseAgent):
    """Gathers evidence across document knowledge base and search tools."""

    def __init__(self):
        super().__init__(
            role_name="researcher",
            description="Executes hybrid document retrieval and web search to gather evidence.",
        )

    async def _run_agent_logic(
        self,
        task: Dict[str, Any],
        workspace: SharedWorkingMemory,
    ) -> Dict[str, Any]:
        query = task.get("query", workspace.goal)

        # Execute Hybrid Retrieval (Dense ChromaDB + BM25 + RRF + Reranker)
        contexts = await document_service.retrieve_context(query, n_results=3)

        workspace.add_evidence(source="hybrid_rag", data=contexts)

        output_summary = f"Retrieved {len(contexts)} relevant document evidence chunks."
        if contexts:
            output_summary += f" Top source: {contexts[0].get('filename')}"

        return {
            "role": self.role_name,
            "status": "completed",
            "evidence": contexts,
            "output": output_summary,
            "confidence": 0.90 if contexts else 0.50,
        }
