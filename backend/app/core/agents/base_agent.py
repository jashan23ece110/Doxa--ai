"""
Base Agent Abstract Interface for Enterprise Multi-Agent Operating System.

Every agent implementation supports:
plan(), reason(), execute(), review(), communicate(), handoff(), cancel(), recover(), report_metrics().
All operations remain async.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class AgentResponse(BaseModel):
    """Standardized response schema returned by all agents."""

    agent_name: str
    role: str
    content: str
    confidence: float = Field(default=0.90, ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list)


class BaseAgent(ABC):
    """Abstract base class for all enterprise AI agents."""

    def __init__(self, name: str, role: str, description: str):
        self.name = name
        self.role = role
        self.description = description
        self.status = "idle"  # idle, active, failed

    @abstractmethod
    async def execute(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """Executes the agent's core task asynchronously."""
        pass

    async def plan(self, prompt: str) -> Dict[str, Any]:
        """Formulates an execution plan for a goal."""
        return {"agent": self.name, "plan": f"Plan execution for '{prompt[:40]}'"}

    async def reason(self, prompt: str) -> Dict[str, Any]:
        """Performs structured reasoning prior to execution."""
        return {"agent": self.name, "reasoning": f"Reasoning for '{prompt[:40]}'"}

    async def review(self, output: str) -> Dict[str, Any]:
        """Reviews and audits execution output."""
        return {"agent": self.name, "review_passed": True}

    async def communicate(self, message: str, recipient: str) -> Dict[str, Any]:
        """Sends an inter-agent message."""
        return {"sender": self.name, "recipient": recipient, "message": message}

    async def handoff(self, target_agent: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handoffs a task to another specialized agent."""
        return {"from": self.name, "to": target_agent, "task_data": task_data}

    async def cancel(self) -> bool:
        """Cancels active agent execution."""
        self.status = "idle"
        return True

    async def recover(self) -> bool:
        """Recovers agent from a failure state."""
        self.status = "idle"
        return True

    def report_metrics(self) -> Dict[str, Any]:
        """Reports agent operational metrics."""
        return {"name": self.name, "role": self.role, "status": self.status}
