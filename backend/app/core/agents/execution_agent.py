"""Execution Agent implementation."""
from typing import Dict, Any, Optional
from app.core.agents.base_agent import BaseAgent, AgentResponse


class ExecutionAgent(BaseAgent):
    """Specialized agent responsible for task execution and workflow handling."""

    def __init__(self):
        super().__init__(
            name="ExecutionAgent",
            role="Subtask Executor",
            description="Executes concrete subtask actions and records output artifacts.",
        )

    async def execute(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        content = f"Executed subtask for '{prompt[:40]}'."
        return AgentResponse(agent_name=self.name, role=self.role, content=content, confidence=0.92)
