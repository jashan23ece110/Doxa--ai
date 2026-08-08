"""
Agent Coordinator for Enterprise Multi-Agent Operating System.

Spawns agents, assigns work, splits tasks, merges outputs, resolves conflicts,
and monitors agent health.
"""

from typing import Dict, Any, List, Optional
from app.core.agents.agent_registry import agent_registry
from app.core.agents.base_agent import BaseAgent, AgentResponse
from app.core.agents.conflict_resolver import conflict_resolver
from app.core.agents.coordinator_agent import CoordinatorAgent
from app.core.agents.critic_agent import CriticAgent
from app.core.agents.execution_agent import ExecutionAgent
from app.core.agents.memory_agent import MemoryAgent
from app.core.agents.planner_agent import PlannerAgent
from app.core.agents.reasoning_agent import ReasoningAgent
from app.core.agents.research_agent import ResearchAgent
from app.core.agents.retrieval_agent import RetrievalAgent
from app.core.agents.scheduler import scheduler
from app.core.agents.shared_workspace import shared_workspace
from app.core.agents.supervisor import supervisor
from app.core.agents.tool_agent import ToolAgent
from app.core.agents.verification_agent import VerificationAgent
from app.core.logging import logger


class AgentCoordinator:
    """Central coordinator orchestrating multi-agent OS executions."""

    def __init__(self):
        self._register_default_agents()

    def _register_default_agents(self) -> None:
        """Registers the 10 specialized agent roles in agent_registry."""
        agent_registry.register_agent(PlannerAgent(), priority=1, capabilities=["planning"])
        agent_registry.register_agent(ResearchAgent(), priority=2, capabilities=["research"])
        agent_registry.register_agent(RetrievalAgent(), priority=2, capabilities=["retrieval"])
        agent_registry.register_agent(MemoryAgent(), priority=2, capabilities=["memory"])
        agent_registry.register_agent(ToolAgent(), priority=2, capabilities=["tool_execution"])
        agent_registry.register_agent(ReasoningAgent(), priority=2, capabilities=["reasoning"])
        agent_registry.register_agent(CriticAgent(), priority=3, capabilities=["critic"])
        agent_registry.register_agent(VerificationAgent(), priority=3, capabilities=["verification"])
        agent_registry.register_agent(ExecutionAgent(), priority=2, capabilities=["execution"])
        agent_registry.register_agent(CoordinatorAgent(), priority=1, capabilities=["coordination"])

    async def execute_multi_agent_goal(self, prompt: str, user_id: str = "default_user") -> Dict[str, Any]:
        """
        Executes goal via multi-agent pipeline:
        Planner -> Research/Retrieval/Reasoning (Parallel) -> Conflict Resolution -> Verification -> Synthesized Output.
        """
        # Run health recovery check before execution
        await supervisor.inspect_and_recover_agents()

        planner = agent_registry.get_agent("PlannerAgent")
        retriever = agent_registry.get_agent("RetrievalAgent")
        reasoner = agent_registry.get_agent("ReasoningAgent")
        verifier = agent_registry.get_agent("VerificationAgent")

        # 1. Planner Agent
        plan_res = await planner.execute(prompt) if planner else AgentResponse(agent_name="Planner", role="Plan", content="Plan")
        shared_workspace.write("plan", plan_res.content, author_agent="PlannerAgent", category="plans")

        # 2. Parallel Specialist Execution
        coros = []
        if retriever:
            coros.append(retriever.execute(prompt))
        if reasoner:
            coros.append(reasoner.execute(prompt))

        responses = await scheduler.schedule_parallel_execution(coros)

        # 3. Conflict Resolution
        consensus_res = conflict_resolver.resolve_conflicts(responses)
        shared_workspace.write("consensus", consensus_res.content, author_agent="ConflictResolver", category="reasoning")

        # 4. Verification Agent
        if verifier:
            verify_res = await verifier.execute(consensus_res.content)
            shared_workspace.write("verification", verify_res.content, author_agent="VerificationAgent", category="artifacts")

        return {
            "prompt": prompt,
            "user_id": user_id,
            "status": "completed",
            "active_agents_count": len(agent_registry.list_agents()),
            "final_response": consensus_res.content,
        }


# Global AgentCoordinator instance
coordinator = AgentCoordinator()
