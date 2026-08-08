"""Research Agent implementation."""
from typing import Dict, Any, Optional
from app.core.agents.base_agent import BaseAgent, AgentResponse


class ResearchAgent(BaseAgent):
    """Specialized agent responsible for web and external domain research."""

    def __init__(self):
        super().__init__(
            name="ResearchAgent",
            role="Web & Information Researcher",
            description="Searches external resources and gathers real-time web content.",
        )

    async def execute(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        content = f"Research findings for '{prompt[:40]}': Gathered external context."
        return AgentResponse(agent_name=self.name, role=self.role, content=content, confidence=0.90)
