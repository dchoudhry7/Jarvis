"""Google Calendar API service."""

from googleapiclient.discovery import build

from services.google_auth import get_google_credentials


def get_calendar_service():
    """Build and return the Calendar API service, or None if unavailable."""

    creds = get_google_credentials()

    if creds is None:
        return None

    return build("calendar", "v3", credentials=creds)
