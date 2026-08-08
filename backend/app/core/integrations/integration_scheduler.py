"""
Integration Scheduler for Universal Integration Platform.

Schedules sync jobs, polling, periodic refresh, incremental sync, and webhook retries.
"""

import asyncio
from typing import Dict, Any, Callable, Coroutine
from app.core.logging import logger


class IntegrationScheduler:
    """Schedules integration synchronization and polling tasks."""

    def __init__(self):
        self._scheduled_jobs: Dict[str, asyncio.Task] = {}

    def schedule_polling_job(
        self,
        job_id: str,
        interval_s: float,
        coro_func: Callable[[], Coroutine[Any, Any, Any]],
    ) -> str:
        """Schedules recurring polling or sync job."""
        async def _loop():
            while True:
                await asyncio.sleep(interval_s)
                logger.info(f"Executing scheduled polling job '{job_id}'.")
                try:
                    await coro_func()
                except Exception as e:
                    logger.error(f"Polling job '{job_id}' failed: {e}")

        task = asyncio.create_task(_loop())
        self._scheduled_jobs[job_id] = task
        logger.info(f"Scheduled polling job '{job_id}' every {interval_s}s.")
        return job_id


# Global IntegrationScheduler instance
integration_scheduler = IntegrationScheduler()
