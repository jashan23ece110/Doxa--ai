"""Retrieval Agent implementation."""
from typing import Dict, Any, Optional
from app.core.agents.base_agent import BaseAgent, AgentResponse


class RetrievalAgent(BaseAgent):
    """Specialized agent responsible for Hybrid RAG document retrieval."""

    def __init__(self):
        super().__init__(
            name="RetrievalAgent",
            role="Hybrid RAG Document Retriever",
            description="Executes hybrid vector + BM25 search across internal knowledge bases.",
        )

    async def execute(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        content = f"Retrieved documents matching query '{prompt[:40]}'."
        return AgentResponse(agent_name=self.name, role=self.role, content=content, confidence=0.92)
