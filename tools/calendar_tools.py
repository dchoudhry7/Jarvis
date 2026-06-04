import json
from pathlib import Path

from langchain_core.tools import tool


CALENDAR_FILE = Path("data/calendar.json")


@tool
def create_event(
    title: str,
    date: str,
    time: str
):
    """
    Create a calendar event.
    """

    with open(CALENDAR_FILE, "r") as f:
        events = json.load(f)

    event = {
        "id": len(events) + 1,
        "title": title,
        "date": date,
        "time": time
    }

    events.append(event)

    with open(CALENDAR_FILE, "w") as f:
        json.dump(events, f, indent=4)

    return (
        f"Event created successfully.\n\n"
        f"ID: {event['id']}\n"
        f"Title: {title}\n"
        f"Date: {date}\n"
        f"Time: {time}"
    )


@tool
def show_events():
    """
    Show all calendar events.
    """

    with open(CALENDAR_FILE, "r") as f:
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
def delete_event(event_id: int):
    """
    Delete an event by ID.
    """

    with open(CALENDAR_FILE, "r") as f:
        events = json.load(f)

    original_count = len(events)

    events = [
        event
        for event in events
        if event["id"] != event_id
    ]

    if len(events) == original_count:
        return f"No event found with ID {event_id}."

    for idx, event in enumerate(events, start=1):
        event["id"] = idx

    with open(CALENDAR_FILE, "w") as f:
        json.dump(events, f, indent=4)

    return f"Event {event_id} deleted successfully."

@tool
def delete_all_events():
    """
    Delete all calendar events.
    """

    with open(CALENDAR_FILE, "w") as f:
        json.dump([], f, indent=4)

    return "All calendar events deleted successfully."