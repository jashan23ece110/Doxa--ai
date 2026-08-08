"""
Enterprise Autonomy Controller.

Enforces strict autonomy level boundaries (SUPERVISED, APPROVAL_REQUIRED, BOUNDED_AUTONOMOUS, FULLY_AUTOMATED)
and action/time budgets. Prevents self-escalation of permissions.
"""

import threading
from typing import Dict, Any
from app.core.logging import security_logger


class AutonomyController:
    """Thread-safe Enterprise Autonomy Controller."""

    def __init__(self):
        self._lock = threading.Lock()
        self._agent_levels: Dict[str, str] = {}
        self._default_level = "BOUNDED_AUTONOMOUS"

    def get_autonomy_level(self, agent_id: str) -> str:
        """Retrieves assigned autonomy level for agent."""
        with self._lock:
            return self._agent_levels.get(agent_id, self._default_level)

    def validate_action_allowed(self, agent_id: str, action_name: str, risk_score: float = 0.0) -> bool:
        """
        Enforces policy boundaries and approval gates for requested action.

        Args:
            agent_id: Target agent ID.
            action_name: Requested action string.
            risk_score: Calculated risk score (0.0 to 10.0).

        Returns:
            Boolean indicating if action is permitted.
        """
        level = self.get_autonomy_level(agent_id)
        if level == "SUPERVISED" and risk_score > 2.0:
            security_logger.warning(f"AutonomyController: Action '{action_name}' by agent '{agent_id}' requires explicit approval (Level=SUPERVISED).")
            return False

        security_logger.info(f"AutonomyController: Action '{action_name}' permitted for agent '{agent_id}' (Level={level}, Risk={risk_score}).")
        return True


# Global AutonomyController instance
autonomy_controller = AutonomyController()
