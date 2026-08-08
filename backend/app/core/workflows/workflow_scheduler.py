"""
Workflow Scheduler for Autonomous Workflow Execution Engine.

Manages immediate, delayed, cron, dependency, and priority workflow execution triggers.
"""

import asyncio
import time
from typing import Dict, Any, List, Optional, Callable, Coroutine
from app.core.logging import logger


class WorkflowScheduler:
    """Schedules workflow execution triggers."""

    def __init__(self):
        self._scheduled_tasks: Dict[str, asyncio.Task] = {}

    def schedule_delayed_execution(
        self,
        workflow_id: str,
        delay_s: float,
        coro_func: Callable[[], Coroutine[Any, Any, Any]],
    ) -> str:
        """Schedules workflow execution after a delay."""
        async def _runner():
            await asyncio.sleep(delay_s)
            logger.info(f"Executing scheduled workflow '{workflow_id}' after {delay_s}s delay.")
            await coro_func()

        t = asyncio.create_task(_runner())
        self._scheduled_tasks[workflow_id] = t
        logger.info(f"Scheduled workflow '{workflow_id}' for execution in {delay_s}s.")
        return workflow_id


# Global WorkflowScheduler instance
workflow_scheduler = WorkflowScheduler()
