"""Memory Agent implementation."""
from typing import Dict, Any, Optional
from app.core.agents.base_agent import BaseAgent, AgentResponse


class MemoryAgent(BaseAgent):
    """Specialized agent responsible for user memory retrieval and profile context."""

    def __init__(self):
        super().__init__(
            name="MemoryAgent",
            role="Long-Term Memory Specialist",
            description="Retrieves long-term facts, preferences, and entity relationship graphs.",
        )

    async def execute(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        content = f"Retrieved memory profiles for user interaction '{prompt[:40]}'."
        return AgentResponse(agent_name=self.name, role=self.role, content=content, confidence=0.94)
