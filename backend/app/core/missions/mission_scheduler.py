"""
Mission Scheduler for Autonomous Mission Control System.

Manages future, periodic, cron, event-driven, and time-based checkpoint scheduling.
"""

import asyncio
from typing import Dict, Any, Callable, Coroutine
from app.core.logging import logger


class MissionScheduler:
    """Schedules long-horizon mission execution checks and periodic tasks."""

    def __init__(self):
        self._scheduled_tasks: Dict[str, asyncio.Task] = {}

    def schedule_mission_check(
        self,
        mission_id: str,
        interval_s: float,
        coro_func: Callable[[], Coroutine[Any, Any, Any]],
    ) -> str:
        """Schedules a recurring or delayed mission health check."""
        async def _loop():
            while True:
                await asyncio.sleep(interval_s)
                logger.info(f"Executing scheduled mission check for '{mission_id}'.")
                try:
                    await coro_func()
                except Exception as e:
                    logger.error(f"Scheduled mission check failed for '{mission_id}': {e}")

        task = asyncio.create_task(_loop())
        self._scheduled_tasks[mission_id] = task
        logger.info(f"Scheduled recurring check for mission '{mission_id}' every {interval_s}s.")
        return mission_id


# Global MissionScheduler instance
mission_scheduler = MissionScheduler()
