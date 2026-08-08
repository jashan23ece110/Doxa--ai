"""Researcher Agent Implementation."""
import time
from app.core.agents.base_agent import BaseAgent, AgentResponse
from app.core.agents.workspace import SharedWorkingMemory


class ResearcherAgent(BaseAgent):
    """Gathers external search and web context."""

    def __init__(self, agent_id: str = "agent_researcher"):
        super().__init__(agent_id=agent_id, name="ResearcherAgent", role="External Knowledge Researcher")

    async def execute(self, prompt: str, workspace: SharedWorkingMemory) -> AgentResponse:
        start = time.time()
        try:
            # Lazy import tool_registry to avoid circular dependency
            from app.tools.registry import tool_registry
            search_res = await tool_registry.execute_tool("brave_search", {"query": prompt})
        except Exception:
            search_res = f"Web search results for '{prompt}'."

        duration_ms = (time.time() - start) * 1000

        res = AgentResponse(
            agent_name=self.name,
            task_id="research_task",
            result=search_res,
            confidence=0.88,
            evidence_score=0.85,
            latency_ms=duration_ms,
        )
        workspace.add_result(self.name, search_res)
        return res
