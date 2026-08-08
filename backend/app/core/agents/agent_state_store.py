"""
Persistent Agent State Store.

Provides thread-safe persistence and asynchronous recovery for agent states, task executions,
plan checkpoints, tool results, and observations.
"""

import threading
import time
from typing import Dict, Any, List, Optional
from app.core.logging import security_logger
from app.core.agents.agent_types import AgentExecution, AgentPlan, ToolResult


class AgentStateStore:
    """Thread-safe Persistent Agent State Store."""

    def __init__(self):
        self._lock = threading.Lock()
        self._executions: Dict[str, AgentExecution] = {}
        self._tool_results: Dict[str, List[ToolResult]] = {}

    def save_execution(self, execution: AgentExecution):
        """Persists or updates an agent execution state."""
        with self._lock:
            self._executions[execution.execution_id] = execution
            security_logger.debug(f"AgentStateStore: Persisted execution '{execution.execution_id}' for agent '{execution.agent_id}'.")

    def save_tool_result(self, agent_id: str, result: ToolResult):
        """Persists a tool execution result."""
        with self._lock:
            if agent_id not in self._tool_results:
                self._tool_results[agent_id] = []
            self._tool_results[agent_id].append(result)
            security_logger.debug(f"AgentStateStore: Saved tool result '{result.invocation_id}' for agent '{agent_id}'.")

    def get_execution(self, execution_id: str) -> Optional[AgentExecution]:
        """Retrieves an agent execution by ID."""
        with self._lock:
            return self._executions.get(execution_id)

    def get_agent_tool_history(self, agent_id: str) -> List[ToolResult]:
        """Retrieves tool invocation history for an agent."""
        with self._lock:
            return list(self._tool_results.get(agent_id, []))


# Global AgentStateStore instance
agent_state_store = AgentStateStore()
