"""Calendar tools — saves to JSON, optionally syncs to Google Calendar."""

import json
from pathlib import Path
from datetime import datetime, timedelta

from langchain_core.tools import tool

from services.calendar_service import get_calendar_service


# --------------- Storage ---------------

CALENDAR_FILE = Path("data/calendar.json")


def load_events():
    if not CALENDAR_FILE.exists():
        return []
    with open(CALENDAR_FILE, "r") as f:
        return json.load(f)


def save_events(events):
    CALENDAR_FILE.parent.mkdir(exist_ok=True)
    with open(CALENDAR_FILE, "w") as f:
        json.dump(events, f, indent=4)


# --------------- Tools ---------------

@tool
def create_event(title: str, date: str, time: str):
    """
    Create a calendar event.

    Required:
    - title
    - date
    - time

    Use only when all required information is available.
    """

    # Always save to local JSON
    events = load_events()

    event = {
        "id": len(events) + 1,
        "title": title,
        "date": date,
        "time": time,
    }

    # Optionally sync to Google Calendar
    service = get_calendar_service()

    if service is not None:
        try:
            start = datetime.now() + timedelta(hours=1)
            end = start + timedelta(hours=1)

            google_event = {
                "summary": title,
                "description": f"Date: {date}\nTime: {time}",
                "start": {
                    "dateTime": start.isoformat(),
                    "timeZone": "Asia/Kolkata",
                },
                "end": {
                    "dateTime": end.isoformat(),
                    "timeZone": "Asia/Kolkata",
                },
            }

            created = (
                service.events()
                .insert(calendarId="primary", body=google_event)
                .execute()
            )

            event["google_link"] = created["htmlLink"]

        except Exception:
            pass  # Google sync failed, but local save still works

    events.append(event)
    save_events(events)

    google_note = ""
    if "google_link" in event:
        google_note = "\nAlso synced to Google Calendar! 🔗"

    return (
        f"Event created successfully.\n\n"
        f"Title: {title}\n"
        f"Date: {date}\n"
        f"Time: {time}"
        f"{google_note}"
    )


@tool
def show_events():
    """Show all calendar events."""

    events = load_events()

    if not events:
        return "No calendar events found."

    result = []
    for event in events:
        result.append(
            f"ID: {event['id']}\n"
            f"Title: {event['title']}\n"
            f"Date: {event['date']}\n"
            f"Time: {event['time']}"
        )

    return "\n\n".join(result)


@tool
def delete_event(event_id: int):
    """Delete an event by ID."""

    events = load_events()
    original_count = len(events)

    events = [e for e in events if e["id"] != event_id]

    if len(events) == original_count:
        return f"No event found with ID {event_id}."

    for idx, event in enumerate(events, start=1):
        event["id"] = idx

    save_events(events)

    return f"Event {event_id} deleted successfully."


@tool
def delete_all_events():
    """Delete all calendar events."""

    save_events([])

    return "All calendar events deleted successfully."