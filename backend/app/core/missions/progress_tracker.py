"""
Progress Tracker for Autonomous Mission Control System.

Continuously monitors goal, workflow, agent, and tool completion percentages,
updating overall mission percentage and saving progress snapshots.
"""

from typing import Dict, Any
from app.core.missions.mission_models import Mission, ProgressSnapshot


class ProgressTracker:
    """Monitors mission execution progress and records snapshots."""

    @staticmethod
    def update_mission_progress(mission: Mission) -> float:
        """
        Calculates and updates mission progress percentage based on completed goals.
        """
        total = len(mission.goals)
        if total == 0:
            mission.overall_progress_percentage = 100.0
            return 100.0

        completed = sum(1 for g in mission.goals.values() if g.completed)
        pct = round((completed / total) * 100.0, 2)
        mission.overall_progress_percentage = pct

        # Save progress snapshot
        snap = ProgressSnapshot(
            mission_id=mission.mission_id,
            progress_percentage=pct,
            completed_goals_count=completed,
            total_goals_count=total,
        )
        mission.snapshots.append(snap)
        if len(mission.snapshots) > 100:
            mission.snapshots = mission.snapshots[-100:]

        return pct


# Global ProgressTracker instance
progress_tracker = ProgressTracker()
