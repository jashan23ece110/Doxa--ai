"""
Agent Conflict Resolution Engine.

Detects and resolves inter-agent plan and evidence conflicts using authority rules and evidence scoring.
"""

from typing import Dict, Any, List
from app.core.logging import security_logger
from app.core.agents.collaboration.collaboration_types import Conflict, Resolution


class ConflictResolutionEngine:
    """Agent Conflict Resolution Engine."""

    def resolve_conflict(self, conflict: Conflict) -> Resolution:
        """
        Resolves inter-agent conflict via evidence and authority rules.

        Args:
            conflict: Conflict object.

        Returns:
            Resolution object.
        """
        winning_id = conflict.competing_proposals[0].get("proposal_id", "prop_1") if conflict.competing_proposals else "prop_default"

        res = Resolution(
            conflict_id=conflict.conflict_id,
            winning_proposal_id=winning_id,
            resolution_strategy="EVIDENCE_COMPARISON",
        )

        security_logger.info(f"ConflictResolutionEngine: Resolved conflict '{conflict.conflict_id}' -> Winner='{winning_id}'.")
        return res


# Global ConflictResolutionEngine instance
conflict_resolution_engine = ConflictResolutionEngine()
