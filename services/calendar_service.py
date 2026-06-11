from googleapiclient.discovery import build

from services.gmail_service import (
    get_gmail_service
)


def get_calendar_service():

    gmail_service = get_gmail_service()

    if gmail_service is None:
        return None

    creds = gmail_service._http.credentials

    return build(
        "calendar",
        "v3",
        credentials=creds
    )