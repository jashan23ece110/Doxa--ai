"""
Global Autonomous Agent Orchestrator.

Master orchestrator coordinating agent selection, goal routing, task delegation,
context loading, tool authorization, inter-agent communication, and unified integration with Stages 1–8.
"""

import time
from typing import Dict, Any, Optional
from app.core.logging import security_logger
from app.core.agents.agent_types import AgentDefinition, AgentRole, AgentCapability, AgentExecution
from app.core.agents.agent_registry import agent_registry
from app.core.agents.agent_manager import agent_manager
from app.core.agents.agent_execution_engine import agent_execution_engine
from app.core.agents.tool_registry import tool_registry, ToolDefinition


class AgentOrchestrationResult(BaseModel_Orchestration := type("AgentOrchestrationResult", (), {})):
    """Pydantic model fallback for orchestrator response."""
    pass


from pydantic import BaseModel, Field


class AgentOrchestrationResult(BaseModel):
    orchestration_id: str
    selected_agent_id: str
    goal_title: str
    execution_status: str = "COMPLETED"
    result_summary: Dict[str, Any] = Field(default_factory=dict)
    orchestrated_at: float = Field(default_factory=time.time)


class AgentOrchestrator:
    """Global Autonomous Agent Orchestrator Facade."""

    def __init__(self):
        self._register_default_agents_and_tools()

    def _register_default_agents_and_tools(self):
        """Initializes baseline default agents and tools."""
        # 1. Register system analyzer tool
        tool_def = ToolDefinition(
            tool_name="system_analyzer",
            description="Analyzes system performance and security state.",
            input_schema={"target": "string"},
            output_schema={"status": "string"},
        )
        tool_registry.register_tool(tool_def)

        # 2. Register security analyst agent
        cap = AgentCapability(name="system_analysis", description="Capability to analyze systems")
        agent_def = AgentDefinition(
            name="SecurityAnalystAgent",
            role=AgentRole.SECURITY_AUDITOR,
            description="Specialized agent for security audits and threat modeling.",
            capabilities=[cap],
        )
        agent_registry.register_agent(agent_def)
        agent_manager.initialize_agent(agent_def.agent_id)

    async def execute_autonomous_goal(self, goal_title: str, goal_description: str, required_capability: str = "system_analysis") -> AgentOrchestrationResult:
        """
        Orchestrates autonomous goal execution by selecting a matching agent and running the execution pipeline.

        Args:
            goal_title: Title of user goal.
            goal_description: Detailed goal description.
            required_capability: Required capability string for agent discovery.

        Returns:
            AgentOrchestrationResult object.
        """
        t0 = time.time()
        security_logger.info(f"AgentOrchestrator: Orchestrating goal '{goal_title}' (Required Capability='{required_capability}').")

        # 1. Discover matching agent by capability
        matching_agents = agent_registry.find_agents_by_capability(required_capability)
        if not matching_agents:
            all_agents = agent_registry.list_all_agents()
            selected_agent = all_agents[0] if all_agents else AgentDefinition(name="DefaultAgent", description="Fallback agent")
        else:
            selected_agent = matching_agents[0]

        # 2. Activate agent
        agent_manager.activate_agent(selected_agent.agent_id)

        # 3. Execute goal
        execution = await agent_execution_engine.execute_goal(selected_agent.agent_id, goal_title, goal_description)

        res = AgentOrchestrationResult(
            orchestration_id=f"aorch_{int(t0 * 1000)}",
            selected_agent_id=selected_agent.agent_id,
            goal_title=goal_title,
            execution_status=execution.state.value,
            result_summary={"execution_id": execution.execution_id, "goal_id": execution.goal_id},
        )

        security_logger.info(f"AgentOrchestrator: Completed orchestration '{res.orchestration_id}' via agent '{selected_agent.name}' ({selected_agent.agent_id}).")
        return res


# Global AgentOrchestrator instance
agent_orchestrator = AgentOrchestrator()
