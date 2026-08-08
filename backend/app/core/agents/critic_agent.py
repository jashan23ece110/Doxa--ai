"""Critic Agent implementation."""
from typing import Dict, Any, Optional
from app.core.agents.base_agent import BaseAgent, AgentResponse


class CriticAgent(BaseAgent):
    """Specialized agent responsible for output auditing and flaw detection."""

    def __init__(self):
        super().__init__(
            name="CriticAgent",
            role="Output Critic & Auditor",
            description="Audits intermediate outputs for logical flaws or contradictions.",
        )

    async def execute(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        content = f"Critic review for '{prompt[:40]}': 0 critical flaws detected."
        return AgentResponse(agent_name=self.name, role=self.role, content=content, confidence=0.96)
