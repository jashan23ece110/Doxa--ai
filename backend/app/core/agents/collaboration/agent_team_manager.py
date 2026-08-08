"""
Enterprise Agent Team Manager.

Manages dynamic agent team formation, role assignment, capability matching, and team health.
"""

import threading
import time
from typing import Dict, Any, List, Optional
from app.core.logging import security_logger
from app.core.agents.collaboration.collaboration_types import AgentTeam


class AgentTeamManager:
    """Thread-safe Enterprise Agent Team Manager."""

    def __init__(self):
        self._lock = threading.Lock()
        self._teams: Dict[str, AgentTeam] = {}

    def form_team(self, team_name: str, member_agent_ids: List[str], roles_map: Dict[str, str]) -> AgentTeam:
        """
        Forms a dynamic agent team for collaborative workflows.

        Args:
            team_name: Descriptive team name.
            member_agent_ids: List of participating agent IDs.
            roles_map: Mapping of agent_id -> role_name.

        Returns:
            AgentTeam object.
        """
        team = AgentTeam(
            team_name=team_name,
            member_agent_ids=member_agent_ids,
            roles_map=roles_map,
        )

        with self._lock:
            self._teams[team.team_id] = team
            security_logger.info(f"AgentTeamManager: Formed team '{team_name}' ({team.team_id}) with {len(member_agent_ids)} member agents.")
        return team

    def get_team(self, team_id: str) -> Optional[AgentTeam]:
        """Retrieves team by ID."""
        with self._lock:
            return self._teams.get(team_id)


# Global AgentTeamManager instance
agent_team_manager = AgentTeamManager()
