"""Gmail API service."""

from googleapiclient.discovery import build

from services.google_auth import get_google_credentials


def get_gmail_service():
    """Build and return the Gmail API service, or None if unavailable."""

    creds = get_google_credentials()

    if creds is None:
        return None

    return build("gmail", "v1", credentials=creds)