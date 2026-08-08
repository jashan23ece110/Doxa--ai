"""
Executor Agent Implementation.

Executes computation sandboxes, calculator evaluations, and external tool integrations.
"""

from typing import Dict, Any
from app.core.agents.base import BaseAgent
from app.core.agents.workspace import SharedWorkingMemory
from app.tools.registry import tool_registry


class ExecutorAgent(BaseAgent):
    """Executes auxiliary tools and sandbox computations."""

    def __init__(self):
        super().__init__(
            role_name="executor",
            description="Executes tools including Python sandbox, math calculator, and calendar integrations.",
        )

    async def _run_agent_logic(
        self,
        task: Dict[str, Any],
        workspace: SharedWorkingMemory,
    ) -> Dict[str, Any]:
        tool_name = task.get("tool_name")
        tool_args = task.get("tool_args", {})

        if not tool_name:
            return {
                "role": self.role_name,
                "status": "completed",
                "output": "No tool execution requested for this step.",
                "confidence": 1.0,
            }

        # Execute registered tool via ToolRegistry
        tool_output = await tool_registry.execute_tool(tool_name, tool_args)
        workspace.add_evidence(source=f"tool:{tool_name}", data=tool_output)

        return {
            "role": self.role_name,
            "status": "completed",
            "tool_name": tool_name,
            "tool_output": tool_output,
            "output": f"Tool '{tool_name}' executed successfully.",
            "confidence": 0.95,
        }
