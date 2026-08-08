"""
Mission Metrics Tracker for Autonomous Mission Control System.

Tracks active, completed, and failed missions, goal completion rates,
milestones completed, mission recovery events, priority recalculations, and strategy changes.
"""

import threading
from typing import Dict, Any, List


class MissionMetricsTracker:
    """Thread-safe metrics tracker for long-horizon mission control."""

    def __init__(self):
        self._lock = threading.Lock()
        self.active_missions_count: int = 0
        self.completed_missions_count: int = 0
        self.failed_missions_count: int = 0
        self.milestones_completed_count: int = 0
        self.mission_recoveries_count: int = 0
        self.priority_recalculations_count: int = 0
        self.durations_s: List[float] = []

    def record_mission_completion(self, duration_s: float = 0.0) -> None:
        """Records a completed mission."""
        with self._lock:
            self.completed_missions_count += 1
            self.durations_s.append(duration_s)
            if len(self.durations_s) > 1000:
                self.durations_s = self.durations_s[-1000:]

    def record_milestone_completion(self) -> None:
        """Records a completed milestone."""
        with self._lock:
            self.milestones_completed_count += 1

    def record_recovery(self) -> None:
        """Records a mission failure recovery event."""
        with self._lock:
            self.mission_recoveries_count += 1

    def record_priority_recalculation(self) -> None:
        """Records a goal priority recalculation."""
        with self._lock:
            self.priority_recalculations_count += 1

    def get_summary(self) -> Dict[str, Any]:
        """Returns summary statistics across long-horizon mission executions."""
        with self._lock:
            tot = self.completed_missions_count + self.failed_missions_count
            rate = round(self.completed_missions_count / tot, 2) if tot > 0 else 1.0
            avg_dur = (
                round(sum(self.durations_s) / len(self.durations_s), 2)
                if self.durations_s
                else 0.0
            )

            return {
                "active_missions": self.active_missions_count,
                "completed_missions": self.completed_missions_count,
                "failed_missions": self.failed_missions_count,
                "goal_completion_rate": rate,
                "milestones_completed": self.milestones_completed_count,
                "mission_recoveries": self.mission_recoveries_count,
                "priority_recalculations": self.priority_recalculations_count,
                "average_mission_duration_s": avg_dur,
            }


# Global MissionMetricsTracker instance
mission_metrics_tracker = MissionMetricsTracker()
