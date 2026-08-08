"""
Abstract Base Class for Multi-Agent Implementation.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from app.core.agents.interfaces import IAgent
from app.core.agents.workspace import SharedWorkingMemory
from app.core.logging import logger


class BaseAgent(IAgent, ABC):
    """Base implementation providing common execution, logging, and error handling for agents."""

    def __init__(self, role_name: str, description: str):
        self._role_name = role_name
        self._description = description

    @property
    def role_name(self) -> str:
        return self._role_name

    @property
    def description(self) -> str:
        return self._description

    async def execute_task(
        self,
        task: Dict[str, Any],
        workspace: SharedWorkingMemory,
    ) -> Dict[str, Any]:
        """Wraps concrete task execution in diagnostics and logging."""
        logger.info(f"Agent '{self.role_name}' starting task: {task.get('goal', 'General Task')[:40]}...")
        try:
            result = await self._run_agent_logic(task, workspace)
            workspace.set_agent_output(self.role_name, result)
            return result
        except Exception as e:
            logger.error(f"Agent '{self.role_name}' execution failed: {e}")
            error_result = {
                "role": self.role_name,
                "status": "failed",
                "output": f"Execution error in agent '{self.role_name}': {str(e)}",
                "confidence": 0.0,
            }
            workspace.set_agent_output(self.role_name, error_result)
            return error_result

    @abstractmethod
    async def _run_agent_logic(
        self,
        task: Dict[str, Any],
        workspace: SharedWorkingMemory,
    ) -> Dict[str, Any]:
        """Concrete agent execution logic implementation."""
        pass
