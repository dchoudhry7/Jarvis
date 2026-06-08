import json
from pathlib import Path

PENDING_FILE = Path(
    "data/pending_email.json"
)


def save_pending_email(
    recipient,
    subject,
    body
):

    data = {
        "recipient": recipient,
        "subject": subject,
        "body": body
    }

    with open(
        PENDING_FILE,
        "w"
    ) as f:
        json.dump(
            data,
            f,
            indent=4
        )


def load_pending_email():

    with open(
        PENDING_FILE,
        "r"
    ) as f:
        return json.load(f)


def clear_pending_email():

    with open(
        PENDING_FILE,
        "w"
    ) as f:
        json.dump(
            {},
            f
        )