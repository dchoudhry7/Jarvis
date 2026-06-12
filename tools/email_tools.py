"""Email tools — draft, send, and manage emails."""

import json
import base64
from pathlib import Path
from email.mime.text import MIMEText

from langchain_core.tools import tool

from config import llm
from services.gmail_service import get_gmail_service
from utils.pending_mail import (
    save_pending_email,
    clear_pending_email,
    load_pending_email,
)


# --------------- Storage ---------------

DRAFT_FILE = Path("data/email_drafts.json")


def load_drafts():
    if not DRAFT_FILE.exists():
        return []
    with open(DRAFT_FILE, "r") as f:
        return json.load(f)


def save_drafts(drafts):
    DRAFT_FILE.parent.mkdir(exist_ok=True)
    with open(DRAFT_FILE, "w") as f:
        json.dump(drafts, f, indent=4)


# --------------- Tools ---------------

@tool
def draft_email(recipient: str, subject: str, purpose: str):
    """
    Create and save a new email draft.

    Args:
        recipient: Person or organization receiving the email.
        subject: Email subject line.
        purpose: Reason for the email — used to generate the content.

    Use when the user wants to draft/write/compose an email.
    Do not use for viewing or deleting drafts.
    After creating the draft, do not call this tool again.
    """

    prompt = f"""
    Write a professional email.
    Recipient: {recipient}
    Subject: {subject}
    Purpose: {purpose}
    """

    email_text = llm.invoke(prompt).content

    save_pending_email(recipient, subject, email_text)

    drafts = load_drafts()

    draft = {
        "id": len(drafts) + 1,
        "recipient": recipient,
        "subject": subject,
        "content": email_text,
    }

    drafts.append(draft)
    save_drafts(drafts)

    return (
        f"Draft saved successfully.\n\n"
        f"Draft ID: {draft['id']}\n"
        f"Subject: {subject}\n\n"
        f"{email_text}"
    )


@tool
def show_email_drafts():
    """
    Display all saved email drafts.

    Use when the user wants to see/list/view drafts.
    Do not use for creating or deleting drafts.
    """

    drafts = load_drafts()

    if not drafts:
        return "No email drafts found."

    result = []
    for draft in drafts:
        result.append(
            f"Draft ID: {draft['id']}\n"
            f"Recipient: {draft['recipient']}\n"
            f"Subject: {draft['subject']}\n"
            f"Content:\n{draft['content']}"
        )

    return "\n\n".join(result)


@tool
def delete_email_draft(draft_id: int):
    """
    Delete a specific email draft by ID.

    Use only when the user provides a draft ID to delete.
    Do not use for deleting all drafts.
    """

    drafts = load_drafts()
    original_count = len(drafts)

    drafts = [d for d in drafts if d["id"] != draft_id]

    if len(drafts) == original_count:
        return f"No draft found with ID {draft_id}."

    for idx, draft in enumerate(drafts, start=1):
        draft["id"] = idx

    save_drafts(drafts)

    return f"Draft {draft_id} deleted successfully."


@tool
def delete_all_email_drafts():
    """
    Delete every saved email draft.

    Use only when the user explicitly asks to delete/clear all drafts.
    """

    save_drafts([])

    return "All email drafts deleted successfully."


@tool
def send_email(recipient: str, subject: str, body: str):
    """
    Send an email via Gmail API.

    Do not use unless a draft already exists.
    """

    service = get_gmail_service()

    if service is None:
        return "Gmail is not configured. Google OAuth credentials are required to send emails."

    message = MIMEText(body)
    message["to"] = recipient
    message["subject"] = subject

    raw_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    service.users().messages().send(
        userId="me",
        body={"raw": raw_message},
    ).execute()

    return f"Email sent successfully to {recipient}"


@tool
def send_pending_email():
    """
    Send the most recently drafted email.

    IMPORTANT: After this tool executes successfully,
    the email has already been sent. Do NOT call again.

    Use only when the user confirms: yes / send it / approve.
    """

    email = load_pending_email()

    if not email:
        return "No pending email found."

    result = send_email.invoke({
        "recipient": email["recipient"],
        "subject": email["subject"],
        "body": email["body"],
    })

    clear_pending_email()

    return result