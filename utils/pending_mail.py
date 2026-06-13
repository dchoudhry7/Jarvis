import json
from pathlib import Path
from langchain_core.runnables import RunnableConfig

def get_pending_file(config: RunnableConfig = None) -> Path:
    thread_id = None
    if config:
        thread_id = config.get("configurable", {}).get("thread_id")
    if thread_id:
        return Path("data") / thread_id / "pending_email.json"
    return Path("data/pending_email.json")


def save_pending_email(recipient, subject, body, config: RunnableConfig = None):
    data = {
        "recipient": recipient,
        "subject": subject,
        "body": body
    }

    pending_file = get_pending_file(config)
    pending_file.parent.mkdir(exist_ok=True, parents=True)
    with open(pending_file, "w") as f:
        json.dump(data, f, indent=4)


def load_pending_email(config: RunnableConfig = None):
    pending_file = get_pending_file(config)
    if not pending_file.exists():
        return {}
    with open(pending_file, "r") as f:
        return json.load(f)


def clear_pending_email(config: RunnableConfig = None):
    pending_file = get_pending_file(config)
    pending_file.parent.mkdir(exist_ok=True, parents=True)
    with open(pending_file, "w") as f:
        json.dump({}, f)

