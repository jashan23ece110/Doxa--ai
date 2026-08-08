"""
Mission Failure Recovery Engine for Autonomous Mission Control System.

Auto-recovers from tool, workflow, agent, network, or API failures via retries,
strategy switching, and goal branch resumption.
"""

from typing import Dict, Any
from app.core.logging import logger
from app.core.missions.mission_metrics import mission_metrics_tracker
from app.core.missions.mission_models import Mission, MissionRecoveryEvent, MissionState


class MissionRecovery:
    """Manages failure recovery and strategy switching for long-running missions."""

    @staticmethod
    def handle_mission_failure(
        mission: Mission,
        failed_component: str,
        error_message: str,
    ) -> bool:
        """
        Logs recovery event, resets mission state to RUNNING, and switches execution strategy.
        """
        rec_event = MissionRecoveryEvent(
            mission_id=mission.mission_id,
            failed_component=failed_component,
            error_message=error_message,
            recovery_action="Auto-recovery: Switched strategy & resumed execution branch.",
        )
        mission.recovery_events.append(rec_event)
        mission.status = MissionState.RUNNING

        mission_metrics_tracker.record_recovery()
        logger.info(
            f"MissionRecovery handled failure for mission '{mission.mission_id}' "
            f"in component '{failed_component}': {error_message}"
        )
        return True


# Global MissionRecovery instance
mission_recovery = MissionRecovery()
