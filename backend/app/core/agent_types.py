"""
Multi-Agent Role Architecture and Plugin Extension Interfaces.

Paves the way for future specialized agent roles (Planner, Researcher, Critic, Executor, Memory Manager)
and plugin extensions without breaking core execution loops.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class IAgentRole(ABC):
    """Abstract interface for specialized multi-agent roles."""

    @property
    @abstractmethod
    def role_name(self) -> str:
        """Name identifier of the agent role (e.g. 'planner', 'researcher', 'critic', 'executor')."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Description of the sub-agent's responsibility."""
        pass

    @abstractmethod
    async def process(self, goal: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Processes a task goal within the context of multi-agent execution."""
        pass


class IPlugin(ABC):
    """Abstract interface for future plugin packages extending Doxa capabilities."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Plugin version."""
        pass

    @abstractmethod
    def initialize(self, app_context: Dict[str, Any]) -> None:
        """Initializes plugin components and registers custom tools/providers."""
        pass
