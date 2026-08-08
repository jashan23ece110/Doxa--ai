"""
Enterprise Agent Registry.

Manages agent definitions, versioning, capability matching, and dynamic discovery.
Agents are discoverable by capability rather than hard-coded names.
"""

import threading
from typing import Dict, Any, List, Optional
from app.core.logging import security_logger
from app.core.agents.agent_types import AgentDefinition, AgentCapability, AgentRole


class AgentRegistry:
    """Thread-safe Enterprise Agent Registry."""

    def __init__(self):
        self._lock = threading.Lock()
        self._agents: Dict[str, AgentDefinition] = {}

    def register_agent(self, agent_def: AgentDefinition) -> AgentDefinition:
        """Registers a new agent definition in the registry."""
        with self._lock:
            self._agents[agent_def.agent_id] = agent_def
            security_logger.info(f"AgentRegistry: Registered agent '{agent_def.name}' ({agent_def.agent_id}, Role={agent_def.role.value}).")
        return agent_def

    def get_agent(self, agent_id: str) -> Optional[AgentDefinition]:
        """Retrieves registered agent by ID."""
        with self._lock:
            return self._agents.get(agent_id)

    def find_agents_by_capability(self, capability_name: str) -> List[AgentDefinition]:
        """
        Discovers active agents matching a specific capability name.

        Args:
            capability_name: Required capability string.

        Returns:
            List of matching AgentDefinition objects.
        """
        with self._lock:
            matching = []
            for agent in self._agents.values():
                if not agent.is_active:
                    continue
                for cap in agent.capabilities:
                    if cap.name.lower() == capability_name.lower():
                        matching.append(agent)
                        break
            security_logger.debug(f"AgentRegistry: Discovered {len(matching)} agents matching capability '{capability_name}'.")
            return matching

    def list_all_agents(self) -> List[AgentDefinition]:
        """Lists all registered agents."""
        with self._lock:
            return list(self._agents.values())


# Global AgentRegistry instance
agent_registry = AgentRegistry()
