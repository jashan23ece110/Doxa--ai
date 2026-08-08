"""
Timer Service for In-App Reminders and Real-Time Notifications.

Manages background jobs via APScheduler and pushes SSE alerts to registered queues.
Validates parameter duration bounds and protects against memory leak queues.
"""

import asyncio
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
from apscheduler.schedulers.background import BackgroundScheduler
from app.core.logging import logger
from app.core.security import ToolValidator


class TimerService:
    """Service scheduling background timers and streaming real-time notifications."""

    def __init__(self):
        self._scheduler = BackgroundScheduler()
        self._scheduler.start()
        logger.info("BackgroundScheduler initialized and started.")
        self._queues: List[asyncio.Queue] = []
        self._loop: Optional[asyncio.AbstractEventLoop] = None

    def register_queue(self, queue: asyncio.Queue) -> None:
        """Registers a client SSE notification queue."""
        if queue not in self._queues:
            self._queues.append(queue)
            try:
                self._loop = asyncio.get_running_loop()
            except RuntimeError:
                pass

    def unregister_queue(self, queue: asyncio.Queue) -> None:
        """Unregisters a client SSE notification queue."""
        if queue in self._queues:
            self._queues.remove(queue)

    def _trigger_alert(self, title: str) -> None:
        """Triggered by APScheduler when a timer fires."""
        alert = {
            "title": title,
            "message": f"Timer finished: {title}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        logger.info(f"Timer fired: '{title}' — Pushing alert to {len(self._queues)} client queue(s)")

        for q in list(self._queues):
            try:
                if self._loop and self._loop.is_running():
                    self._loop.call_soon_threadsafe(q.put_nowait, alert)
                else:
                    q.put_nowait(alert)
            except Exception as e:
                logger.error(f"Failed to push alert to client queue: {e}")

    def schedule_timer(self, title: str, seconds: int) -> str:
        """Schedules a new timer with security bounds checking."""
        ToolValidator.validate_timer(title, seconds)

        run_date = datetime.now() + timedelta(seconds=seconds)
        job = self._scheduler.add_job(
            self._trigger_alert,
            "date",
            run_date=run_date,
            args=[title],
        )

        logger.info(f"Scheduled timer job '{title}' (ID: {job.id}) to fire in {seconds}s at {run_date}")
        return f"Timer set for '{title}' in {seconds} seconds."


timer_service = TimerService()
