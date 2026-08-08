"""
Timer and SSE Real-Time Notification Stream API Router with Connection Hardening.
"""

import json
import asyncio
import time
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.schemas.timer import TimerRequest, TimerResponse
from app.services.timer_service import TimerService
from app.api.deps import get_timer_service
from app.core.config import settings

router = APIRouter(tags=["Timers & Notifications"])


@router.post("/timers", response_model=TimerResponse)
def create_timer(
    req: TimerRequest,
    tm_service: TimerService = Depends(get_timer_service),
):
    """Schedules an in-app alarm or reminder timer with bounds validation."""
    msg = tm_service.schedule_timer(req.title, req.seconds)
    return {"status": "ok", "message": msg}


@router.get("/notifications/stream")
async def notifications_stream(
    tm_service: TimerService = Depends(get_timer_service),
):
    """SSE endpoint pushing real-time timer completion alerts with clean unregistration."""

    async def event_generator():
        queue: asyncio.Queue = asyncio.Queue()
        tm_service.register_queue(queue)
        start_time = time.time()
        max_lifetime = settings.MAX_SSE_STREAM_LIFETIME_SECONDS

        try:
            while True:
                if time.time() - start_time > max_lifetime:
                    yield f"data: {json.dumps({'title': 'System Notification', 'message': 'Notification stream lifetime expired. Reconnecting...'})}\n\n"
                    break

                try:
                    alert = await asyncio.wait_for(queue.get(), timeout=15.0)
                    yield f"data: {json.dumps(alert)}\n\n"
                except asyncio.TimeoutError:
                    # Keep-alive heartbeat ping to detect client disconnects
                    yield f": keepalive\n\n"
        except asyncio.CancelledError:
            pass
        finally:
            tm_service.unregister_queue(queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
