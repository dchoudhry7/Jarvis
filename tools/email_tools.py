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
    Draft and save an email.
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
    Show all drafts.
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
    Delete a specific email draft by its ID.
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
    Delete all saved email drafts.
    """

    with open(DRAFT_FILE, "w") as f:
        json.dump([], f, indent=4)

    return "All email drafts deleted successfully."