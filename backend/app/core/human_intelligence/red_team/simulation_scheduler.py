"""
Defensive Simulation Scheduler.

Schedules recurring educational security awareness simulations, campaign runs,
department targeting, randomized educational scenario execution, and execution history versioning.
"""

import threading
import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class ScheduledSimulationJob(BaseModel):
    job_id: str
    scenario_id: str
    target_department: str = "All"
    cron_schedule: str = "0 9 1 * *"  # Monthly 1st day 9am
    status: str = "active"  # active, paused, completed
    created_at: float = Field(default_factory=time.time)


class SimulationScheduler:
    """Thread-safe Defensive Simulation Scheduler."""

    def __init__(self):
        self._lock = threading.Lock()
        self._jobs: Dict[str, ScheduledSimulationJob] = {}

    def schedule_simulation(self, scenario_id: str, target_department: str = "All", cron_schedule: str = "0 9 1 * *") -> ScheduledSimulationJob:
        """Schedules a recurring educational simulation campaign job."""
        job_id = f"simjob_{int(time.time() * 1000)}"
        job = ScheduledSimulationJob(
            job_id=job_id,
            scenario_id=scenario_id,
            target_department=target_department,
            cron_schedule=cron_schedule,
        )
        with self._lock:
            self._jobs[job_id] = job
            security_logger.info(f"SimulationScheduler: Scheduled simulation job '{job_id}' for '{target_department}'.")
        return job

    def list_jobs(self) -> List[ScheduledSimulationJob]:
        """Lists active scheduled simulation jobs."""
        with self._lock:
            return list(self._jobs.values())


# Global SimulationScheduler instance
simulation_scheduler = SimulationScheduler()
