import json

from pathlib import Path


PENDING_FILE = Path(
    "data/pending_event.json"
)


def save_pending_event(data):

    with open(
        PENDING_FILE,
        "w"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )


def load_pending_event():

    with open(
        PENDING_FILE,
        "r"
    ) as f:

        return json.load(f)


def clear_pending_event():

    with open(
        PENDING_FILE,
        "w"
    ) as f:

        json.dump(
            {},
            f
        )