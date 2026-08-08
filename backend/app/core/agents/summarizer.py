"""
Summarizer Agent Implementation.

Synthesizes outputs from all specialist agents into cohesive final answers.
"""

from typing import Dict, Any
from app.core.agents.base import BaseAgent
from app.core.agents.workspace import SharedWorkingMemory


class SummarizerAgent(BaseAgent):
    """Synthesizes agent outputs and evidence into a unified response."""

    def __init__(self):
        super().__init__(
            role_name="summarizer",
            description="Merges outputs, removes redundancies, and generates the final response.",
        )

    async def _run_agent_logic(
        self,
        task: Dict[str, Any],
        workspace: SharedWorkingMemory,
    ) -> Dict[str, Any]:
        all_outputs = workspace.get_all_outputs()

        research_info = all_outputs.get("researcher", {}).get("output", "")
        executor_info = all_outputs.get("executor", {}).get("output", "")
        critic_info = all_outputs.get("critic", {}).get("output", "")

        summarized = (
            f"Multi-Agent Synthesis for Goal: '{workspace.goal}'\n"
            f"- Research Phase: {research_info}\n"
            f"- Execution Phase: {executor_info}\n"
            f"- Factual Audit: {critic_info}"
        )

        return {
            "role": self.role_name,
            "status": "completed",
            "final_response": summarized,
            "output": summarized,
            "confidence": 0.95,
        }
