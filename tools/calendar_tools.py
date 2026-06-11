import json

from pathlib import Path

from datetime import (
    datetime,
    timedelta
)

from langchain_core.tools import tool

from services.calendar_service import (
    get_calendar_service
)


CALENDAR_FILE = Path(
    "data/calendar.json"
)


@tool
def create_event(
    title: str,
    date: str,
    time: str
):
    """
    Create a calendar event.

    Required:
    - title
    - date
    - time

    Use only when all required
    information is available.
    """

    service = get_calendar_service()

    if service is None:
        return "Google Calendar is not configured. OAuth credentials are required to create events."

    start = datetime.now() + timedelta(
        hours=1
    )

    end = start + timedelta(
        hours=1
    )

    google_event = {
        "summary": title,

        "description":
            f"Date: {date}\n"
            f"Time: {time}",

        "start": {
            "dateTime": start.isoformat(),
            "timeZone": "Asia/Kolkata"
        },

        "end": {
            "dateTime": end.isoformat(),
            "timeZone": "Asia/Kolkata"
        }
    }

    created_event = (
        service.events()
        .insert(
            calendarId="primary",
            body=google_event
        )
        .execute()
    )

    with open(
        CALENDAR_FILE,
        "r"
    ) as f:

        events = json.load(f)

    event = {
        "id": len(events) + 1,
        "title": title,
        "date": date,
        "time": time,
        "google_link":
            created_event["htmlLink"]
    }

    events.append(event)

    with open(
        CALENDAR_FILE,
        "w"
    ) as f:

        json.dump(
            events,
            f,
            indent=4
        )

    return (
        f"Event created successfully.\n\n"
        f"Title: {title}\n"
        f"Date: {date}\n"
        f"Time: {time}\n\n"
        f"Google Calendar event created."
    )


@tool
def show_events():
    """
    Show all calendar events.
    """

    with open(
        CALENDAR_FILE,
        "r"
    ) as f:

        events = json.load(f)

    if not events:
        return "No calendar events found."

    result = []

    for event in events:

        result.append(
            f"""
ID: {event['id']}
Title: {event['title']}
Date: {event['date']}
Time: {event['time']}
"""
        )

    return "\n".join(result)


@tool
def delete_event(
    event_id: int
):
    """
    Delete an event by ID.
    """

    with open(
        CALENDAR_FILE,
        "r"
    ) as f:

        events = json.load(f)

    original_count = len(events)

    events = [
        event
        for event in events
        if event["id"] != event_id
    ]

    if len(events) == original_count:
        return (
            f"No event found "
            f"with ID {event_id}."
        )

    for idx, event in enumerate(
        events,
        start=1
    ):
        event["id"] = idx

    with open(
        CALENDAR_FILE,
        "w"
    ) as f:

        json.dump(
            events,
            f,
            indent=4
        )

    return (
        f"Event {event_id} "
        f"deleted successfully."
    )


@tool
def delete_all_events():
    """
    Delete all calendar events.
    """

    with open(
        CALENDAR_FILE,
        "w"
    ) as f:

        json.dump(
            [],
            f,
            indent=4
        )

    return (
        "All calendar events "
        "deleted successfully."
    )