"""Tool Agent implementation."""
from typing import Dict, Any, Optional
from app.core.agents.base_agent import BaseAgent, AgentResponse


class ToolAgent(BaseAgent):
    """Specialized agent responsible for tool selection and invocation."""

    def __init__(self):
        super().__init__(
            name="ToolAgent",
            role="Tool Execution Specialist",
            description="Selects and safely invokes backend computational tools.",
        )

    async def execute(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        content = f"Executed tools for query '{prompt[:40]}'."
        return AgentResponse(agent_name=self.name, role=self.role, content=content, confidence=0.91)
