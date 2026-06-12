"""
Shared Google OAuth credentials helper.

Used by both Gmail and Calendar services.
"""

from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow



SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/calendar",
]

TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "credentials.json"



def get_google_credentials():
    """
    Return valid Google OAuth credentials, or None
    if credentials are unavailable (e.g. on Streamlit Cloud).
    """

    creds = None

    if Path(TOKEN_FILE).exists():
        creds = Credentials.from_authorized_user_file(
            TOKEN_FILE, SCOPES
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        elif Path(CREDENTIALS_FILE).exists():
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)

        else:
            return None

        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return creds
