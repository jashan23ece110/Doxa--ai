import datetime
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler

# Initialize the global background scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Track active asyncio Queues for SSE notifications
notification_queues = []

def schedule_timer(title: str, seconds: int) -> str:
    """
    Schedules a background job to run after `seconds`.
    When triggered, it thread-safely pushes a notification to all active SSE client streams.
    """
    if seconds <= 0:
        return "Error: Timer duration must be greater than zero."

    run_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
    
    def trigger_alert():
        payload = {
            "type": "timer_completed",
            "title": title,
            "seconds": seconds,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        # Pushing to asyncio queues from APScheduler worker threads requires call_soon_threadsafe
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            # If no event loop in this thread, try to fetch the main loop or handle gracefully
            loop = None
            
        for q in notification_queues:
            if loop:
                loop.call_soon_threadsafe(q.put_nowait, payload)
            else:
                q.put_nowait(payload)

    # Schedule date-based single run job
    scheduler.add_job(trigger_alert, 'date', run_date=run_time)
    
    readable_time = str(datetime.timedelta(seconds=seconds))
    return f"Timer '{title}' set successfully for {readable_time} ({seconds} seconds)."
