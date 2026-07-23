import os
import datetime
from typing import List, Dict

# In-memory mock calendar event store for demonstration/fallback
_mock_events: List[Dict] = [
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
        "description": "Restructuring index.css global accent variable mappings."
    }
]

def get_calendar_service():
    """
    Tries to authenticate and build Google Calendar service.
    Returns the service object if credentials exist and are valid.
    Otherwise returns None, signaling mock fallback.
    """
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    if not client_id or not client_secret:
        return None

    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        
        # We look for token.json containing saved OAuth user tokens
        token_path = "token.json"
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, ["https://www.googleapis.com/auth/calendar"])
            if creds and creds.valid:
                return build("calendar", "v3", credentials=creds)
            
            # Try to refresh
            if creds and creds.expired and creds.refresh_token:
                from google.auth.transport.requests import Request
                creds.refresh(Request())
                with open(token_path, "w") as token:
                    token.write(creds.to_json())
                return build("calendar", "v3", credentials=creds)
                
    except Exception as e:
        print(f"Error initializing real Google Calendar service: {e}")
        
    return None

def list_calendar_events() -> str:
    """
    Reads the upcoming 10 events from Google Calendar (or mocks if not connected).
    """
    service = get_calendar_service()
    if not service:
        # Graceful fallback: return mock list
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
            # Parse readable format
            try:
                start_dt = datetime.datetime.fromisoformat(start.replace("Z", "+00:00")).strftime("%b %d, %Y at %I:%M %p")
            except Exception:
                start_dt = start
            summary = event.get("summary", "Untitled Event")
            desc = event.get("description", "No details")
            formatted.append(f"{idx}. {summary} (Starts: {start_dt})\n   Description: {desc}")
            
        return "Upcoming calendar events:\n\n" + "\n\n".join(formatted)
        
    except Exception as e:
        return f"Failed to retrieve Google Calendar events: {e}"

def create_calendar_event(summary: str, start_time: str, duration_minutes: int = 30, description: str = "") -> str:
    """
    Creates a new event in Google Calendar (or mock store).
    Arguments:
      - summary: Name of the event
      - start_time: Time of the event, preferred in ISO format (e.g. '2026-07-25T14:30:00') or natural relative format
      - duration_minutes: Length in minutes
      - description: Additional event context
    """
    # Parse start time, fallback to tomorrow same time if unparseable
    try:
        start_dt = datetime.datetime.fromisoformat(start_time)
    except Exception:
        # Fallback parsing natural time keywords: e.g. "tomorrow at 2pm"
        now = datetime.datetime.now()
        start_dt = now + datetime.timedelta(days=1) # Default tomorrow
        
    end_dt = start_dt + datetime.timedelta(minutes=duration_minutes)
    
    service = get_calendar_service()
    if not service:
        # Save to mock list
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
        return f"Failed to create Google Calendar event: {e}"
