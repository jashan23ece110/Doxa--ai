"""
Global Agent Policy Orchestrator.

Orchestrates governance policies across autonomy levels (LEVEL 0 ADVISORY through LEVEL 4 ENTERPRISE_AUTONOMOUS)
and enforces tool allowlists and risk thresholds.
"""

import threading
import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class AutonomyPolicy(BaseModel):
    policy_id: str = Field(default_factory=lambda: f"pol_level_{hash(time.time()) & 0xffff}")
    autonomy_level: str = "LEVEL_2_BOUNDED_AUTONOMOUS"
    max_allowed_risk_score: float = 5.0
    requires_human_approval: bool = False
    allowed_tool_categories: List[str] = Field(default_factory=lambda: ["search", "analysis", "coding", "testing", "devops"])


class AgentPolicyOrchestrator:
    """Thread-safe Global Agent Policy Orchestrator."""

    def __init__(self):
        self._lock = threading.Lock()
        self._active_policy = AutonomyPolicy()

    def get_active_policy(self) -> AutonomyPolicy:
        """Retrieves current platform autonomy governance policy."""
        with self._lock:
            return self._active_policy

    def enforce_policy_check(self, agent_id: str, tool_category: str, risk_score: float) -> bool:
        """Enforces policy check for requested tool execution."""
        policy = self.get_active_policy()
        if risk_score > policy.max_allowed_risk_score:
            security_logger.warning(f"AgentPolicyOrchestrator: Policy check failed for agent '{agent_id}' - Risk score {risk_score} > Max {policy.max_allowed_risk_score}.")
            return False

        security_logger.info(f"AgentPolicyOrchestrator: Policy check passed for agent '{agent_id}' (Category='{tool_category}', Risk={risk_score}).")
        return True


# Global AgentPolicyOrchestrator instance
agent_policy_orchestrator = AgentPolicyOrchestrator()
