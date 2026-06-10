from datetime import (
    datetime,
    timedelta
)

from services.calendar_service import (
    get_calendar_service
)

service = get_calendar_service()

start = datetime.now() + timedelta(
    hours=1
)

end = start + timedelta(
    hours=1
)

event = {
    "summary": "Jarvis Test Event",

    "start": {
        "dateTime": start.isoformat(),
        "timeZone": "Asia/Kolkata"
    },

    "end": {
        "dateTime": end.isoformat(),
        "timeZone": "Asia/Kolkata"
    }
}

created_event = service.events().insert(
    calendarId="primary",
    body=event
).execute()

print(
    "EVENT CREATED"
)

print(
    created_event["htmlLink"]
)