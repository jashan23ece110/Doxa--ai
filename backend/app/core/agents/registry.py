"""
Dynamic Agent Registry & Factory.

Supports dynamic registration, self-discovery, and factory instantiation for multi-agent roles.
"""

from typing import Dict, Type, List
from app.core.agents.interfaces import IAgent
from app.core.agents.planner import PlannerAgent
from app.core.agents.researcher import ResearcherAgent
from app.core.agents.executor import ExecutorAgent
from app.core.agents.critic import CriticAgent
from app.core.agents.summarizer import SummarizerAgent
from app.core.agents.coordinator import CoordinatorAgent


class AgentRegistry:
    """Registry for discovering and instantiating multi-agent roles."""

    _registry: Dict[str, Type[IAgent]] = {
        "planner": PlannerAgent,
        "researcher": ResearcherAgent,
        "executor": ExecutorAgent,
        "critic": CriticAgent,
        "summarizer": SummarizerAgent,
        "coordinator": CoordinatorAgent,
    }

    @classmethod
    def register_agent(cls, role_name: str, agent_cls: Type[IAgent]) -> None:
        """Registers a new agent strategy class dynamically."""
        cls._registry[role_name.lower()] = agent_cls

    @classmethod
    def get_agent(cls, role_name: str) -> IAgent:
        """Instantiates and returns an agent strategy by role name."""
        key = role_name.lower()
        if key not in cls._registry:
            raise ValueError(f"Unknown agent role '{role_name}'. Registered roles: {list(cls._registry.keys())}")
        return cls._registry[key]()

    @classmethod
    def list_roles(cls) -> List[str]:
        """Returns list of all registered agent roles."""
        return list(cls._registry.keys())


# Global AgentRegistry instance
agent_registry = AgentRegistry()
