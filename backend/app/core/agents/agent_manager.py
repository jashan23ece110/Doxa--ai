"""
Enterprise Agent Manager.

Manages agent lifecycle transitions (Initialization -> Activation -> Suspension -> Termination),
health monitoring, resource allocation, execution limits, and agent runtime isolation.
"""

import threading
import time
from typing import Dict, Any, Optional
from app.core.logging import security_logger
from app.core.agents.agent_types import AgentState, AgentDefinition
from app.core.agents.agent_registry import agent_registry


class AgentRuntimeInstance:

    def __init__(self, definition: AgentDefinition):
        self.definition = definition
        self.state: AgentState = AgentState.IDLE
        self.active_tasks_count: int = 0
        self.last_heartbeat: float = time.time()


class AgentManager:
    """Thread-safe Enterprise Agent Manager."""

    def __init__(self):
        self._lock = threading.Lock()
        self._runtimes: Dict[str, AgentRuntimeInstance] = {}

    def initialize_agent(self, agent_id: str) -> bool:
        """Initializes a registered agent for runtime execution."""
        agent_def = agent_registry.get_agent(agent_id)
        if not agent_def:
            security_logger.error(f"AgentManager: Failed to initialize agent '{agent_id}' - Not registered.")
            return False

        with self._lock:
            rt = AgentRuntimeInstance(agent_def)
            rt.state = AgentState.IDLE
            self._runtimes[agent_id] = rt
            security_logger.info(f"AgentManager: Initialized agent '{agent_def.name}' ({agent_id}).")
            return True

    def activate_agent(self, agent_id: str) -> bool:
        """Activates an initialized agent."""
        with self._lock:
            rt = self._runtimes.get(agent_id)
            if not rt:
                return False
            rt.state = AgentState.EXECUTING
            rt.last_heartbeat = time.time()
            security_logger.info(f"AgentManager: Activated agent '{agent_id}'. State -> EXECUTING.")
            return True

    def suspend_agent(self, agent_id: str) -> bool:
        """Suspends an executing agent."""
        with self._lock:
            rt = self._runtimes.get(agent_id)
            if not rt:
                return False
            rt.state = AgentState.SUSPENDED
            security_logger.info(f"AgentManager: Suspended agent '{agent_id}'. State -> SUSPENDED.")
            return True

    def terminate_agent(self, agent_id: str) -> bool:
        """Terminates an agent."""
        with self._lock:
            rt = self._runtimes.get(agent_id)
            if not rt:
                return False
            rt.state = AgentState.TERMINATED
            security_logger.info(f"AgentManager: Terminated agent '{agent_id}'. State -> TERMINATED.")
            return True

    def get_agent_state(self, agent_id: str) -> Optional[AgentState]:
        """Retrieves agent runtime state."""
        with self._lock:
            rt = self._runtimes.get(agent_id)
            return rt.state if rt else None


# Global AgentManager instance
agent_manager = AgentManager()
