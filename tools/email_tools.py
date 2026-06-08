import json
from pathlib import Path

from langchain_core.tools import tool

from config import llm


DRAFT_FILE = Path("data/email_drafts.json")


@tool
def draft_email(
    recipient: str,
    subject: str,
    purpose: str
):
    """
    Create and save a new email draft.

    Args:
        recipient: Person or organization receiving the email.
        subject: Email subject line.
        purpose: Reason for the email. This will be used to generate the content.

    Use this tool when the user wants to:
    - draft an email
    - write an email
    - compose an email
    - create an email
    - generate an email

    Required inputs:
    - recipient
    - subject
    - purpose

    Do not use this tool for:
    - viewing drafts
    - deleting drafts

    After creating the draft successfully, do not call this tool again
    unless the user requests another draft.
    """

    prompt = f"""
    Write a professional email.

    Recipient: {recipient}

    Subject: {subject}

    Purpose:
    {purpose}
    """

    email_text = llm.invoke(prompt).content

    with open(DRAFT_FILE, "r") as f:
        drafts = json.load(f)

    draft = {
        "id": len(drafts) + 1,
        "recipient": recipient,
        "subject": subject,
        "content": email_text
    }

    drafts.append(draft)

    with open(DRAFT_FILE, "w") as f:
        json.dump(drafts, f, indent=4)

    return f"""
Draft saved successfully.

Draft ID: {draft['id']}
Subject: {subject}

{email_text}
"""

@tool
def show_email_drafts():
    """
    Display all saved email drafts.

    Use this tool when the user wants to:
    - see drafts
    - list drafts
    - show drafts
    - view drafts
    - check saved emails

    Do not use this tool for creating or deleting drafts.
    """
    with open(DRAFT_FILE, "r") as f:
        drafts = json.load(f)

    if not drafts:
        return "No email drafts found."

    result = []

    for draft in drafts:

        result.append(
            f"""
Draft ID: {draft['id']}

Recipient: {draft['recipient']}

Subject: {draft['subject']}

Content:
{draft['content']}
"""
        )

    return "\n\n".join(result)

@tool
def delete_email_draft(draft_id: int):
    """
    Delete a specific email draft.

    Use this tool only when the user wants to remove
    one particular draft and provides the draft ID.

    Examples:
    - Delete draft 2
    - Remove draft number 5

    Do not use this tool for:
    - deleting all drafts
    - creating drafts
    - viewing drafts
    """

    with open(DRAFT_FILE, "r") as f:
        drafts = json.load(f)

    original_count = len(drafts)

    drafts = [
        draft
        for draft in drafts
        if draft["id"] != draft_id
    ]

    if len(drafts) == original_count:
        return f"No draft found with ID {draft_id}."

    for idx, draft in enumerate(drafts, start=1):
        draft["id"] = idx

    with open(DRAFT_FILE, "w") as f:
        json.dump(drafts, f, indent=4)

    return f"Draft {draft_id} deleted successfully."

@tool
def delete_all_email_drafts():
    """
    Delete every saved email draft.

    Use this tool only when the user explicitly asks to:
    - delete all drafts
    - remove all drafts
    - clear all drafts

    This action removes all saved drafts.

    Never use this tool unless the user clearly requests
    deletion of every draft.
    """

    with open(DRAFT_FILE, "w") as f:
        json.dump([], f, indent=4)

    return "All email drafts deleted successfully."