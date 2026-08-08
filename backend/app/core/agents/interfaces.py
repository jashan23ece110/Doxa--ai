"""
Abstract Multi-Agent Interfaces.

Defines IAgent, IAgentTask, IAgentResult, and IAgentContext contracts for SOLID compliance.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class IAgentContext(ABC):
    """Abstract interface for agent execution context."""

    @property
    @abstractmethod
    def run_id(str) -> str:
        pass


class IAgentTask(ABC):
    """Abstract interface for agent task specifications."""

    @property
    @abstractmethod
    def task_id(str) -> str:
        pass

    @property
    @abstractmethod
    def goal(str) -> str:
        pass


class IAgentResult(ABC):
    """Abstract interface for agent execution outputs."""

    @property
    @abstractmethod
    def task_id(str) -> str:
        pass

    @property
    @abstractmethod
    def status(str) -> str:
        pass

    @property
    @abstractmethod
    def output(str) -> str:
        pass


class IAgent(ABC):
    """Abstract interface for multi-agent system agents."""

    @property
    @abstractmethod
    def role_name(str) -> str:
        pass

    @property
    @abstractmethod
    def description(str) -> str:
        pass

    @abstractmethod
    async def execute_task(
        self,
        task: Dict[str, Any],
        workspace: Any,
    ) -> Dict[str, Any]:
        """Executes assigned task using shared workspace state."""
        pass
