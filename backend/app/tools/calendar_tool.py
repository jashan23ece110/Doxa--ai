"""
Google Calendar Tool Integration and Mock Store Fallback.
"""

import os
import datetime
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.logging import logger

_mock_events: List[Dict[str, Any]] = [
    {
        "id": "mock_1",
        "summary": "Doxa System Sync",
        "start": (datetime.datetime.now() + datetime.timedelta(hours=2)).isoformat(),
        "end": (datetime.datetime.now() + datetime.timedelta(hours=2, minutes=30)).isoformat(),
        "description": "Daily status review for dynamic dashboard components."
    },
    {
        "id": "mock_2",
        "summary": "AI Agent Evaluation Review",
        "start": (datetime.datetime.now() + datetime.timedelta(days=1, hours=4)).isoformat(),
        "end": (datetime.datetime.now() + datetime.timedelta(days=1, hours=5)).isoformat(),
        "description": "Evaluate Llama-3.3-70b-versatile tool use reliability."
    },
    {
        "id": "mock_3",
        "summary": "Codebase Refactoring Standup",
        "start": (datetime.datetime.now() + datetime.timedelta(days=2, hours=1)).isoformat(),
        "end": (datetime.datetime.now() + datetime.timedelta(days=2, hours=1, minutes=45)).isoformat(),
        "description": "Restructuring backend clean architecture modules."
    }
]


def get_calendar_service():
    """Tries to build Google Calendar API service instance if OAuth credentials exist."""
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        return None

    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build

        token_path = settings.TOKEN_FILE_PATH
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, ["https://www.googleapis.com/auth/calendar"])
            if creds and creds.valid:
                return build("calendar", "v3", credentials=creds)

            if creds and creds.expired and creds.refresh_token:
                from google.auth.transport.requests import Request
                creds.refresh(Request())
                with open(token_path, "w") as token_file:
                    token_file.write(creds.to_json())
                return build("calendar", "v3", credentials=creds)
    except Exception as e:
        logger.warning(f"Failed initializing real Google Calendar service: {e}")

    return None


def list_calendar_events() -> str:
    """Lists upcoming 10 events from Google Calendar or mock store."""
    service = get_calendar_service()
    if not service:
        formatted = []
        for idx, event in enumerate(_mock_events, 1):
            start_dt = datetime.datetime.fromisoformat(event["start"]).strftime("%b %d, %Y at %I:%M %p")
            formatted.append(f"{idx}. {event['summary']} (Starts: {start_dt})\n   Description: {event.get('description', 'No details')}")

        return "*(Mock Mode Active - Google OAuth credentials missing)*\nHere are your upcoming events:\n\n" + "\n\n".join(formatted)

    try:
        now = datetime.datetime.utcnow().isoformat() + "Z"
        events_result = service.events().list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        events = events_result.get("items", [])
        if not events:
            return "No upcoming events found in your Google Calendar."

        formatted = []
        for idx, event in enumerate(events, 1):
            start = event["start"].get("dateTime", event["start"].get("date"))
            try:
                start_dt = datetime.datetime.fromisoformat(start.replace("Z", "+00:00")).strftime("%b %d, %Y at %I:%M %p")
            except Exception:
                start_dt = start
            summary = event.get("summary", "Untitled Event")
            desc = event.get("description", "No details")
            formatted.append(f"{idx}. {summary} (Starts: {start_dt})\n   Description: {desc}")

        return "Upcoming calendar events:\n\n" + "\n\n".join(formatted)
    except Exception as e:
        logger.error(f"Failed retrieving Google Calendar events: {e}")
        return f"Failed to retrieve Google Calendar events: {e}"


def create_calendar_event(summary: str, start_time: str, duration_minutes: int = 30, description: str = "") -> str:
    """Creates a new event in Google Calendar or mock store."""
    try:
        start_dt = datetime.datetime.fromisoformat(start_time)
    except Exception:
        now = datetime.datetime.now()
        start_dt = now + datetime.timedelta(days=1)

    end_dt = start_dt + datetime.timedelta(minutes=duration_minutes)

    service = get_calendar_service()
    if not service:
        new_event = {
            "id": f"mock_{len(_mock_events) + 1}",
            "summary": summary,
            "start": start_dt.isoformat(),
            "end": end_dt.isoformat(),
            "description": description or "Created via Doxa Voice Command"
        }
        _mock_events.append(new_event)
        _mock_events.sort(key=lambda x: x["start"])

        readable_start = start_dt.strftime("%b %d, %Y at %I:%M %p")
        return f"*(Mock Mode Active)*\nSuccessfully created calendar event: '{summary}' scheduled for {readable_start} ({duration_minutes} mins)."

    try:
        event_body = {
            "summary": summary,
            "description": description or "Created by Doxa Agent Command",
            "start": {
                "dateTime": start_dt.isoformat(),
                "timeZone": "UTC"
            },
            "end": {
                "dateTime": end_dt.isoformat(),
                "timeZone": "UTC"
            }
        }

        created_event = service.events().insert(calendarId="primary", body=event_body).execute()
        html_link = created_event.get("htmlLink", "#")
        readable_start = start_dt.strftime("%b %d, %Y at %I:%M %p")
        return f"Event '{summary}' successfully created on Google Calendar for {readable_start} ({duration_minutes} mins).\nLink: {html_link}"
    except Exception as e:
        logger.error(f"Failed creating Google Calendar event: {e}")
        return f"Failed to create Google Calendar event: {e}"
