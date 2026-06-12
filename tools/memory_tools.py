"""Memory tools — JSON-only storage."""

import json
from pathlib import Path

from langchain_core.tools import tool



MEMORY_FILE = Path("data/memories.json")


def load_memories():
    if not MEMORY_FILE.exists():
        return []
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memories(memories):
    MEMORY_FILE.parent.mkdir(exist_ok=True)
    with open(MEMORY_FILE, "w") as f:
        json.dump(memories, f, indent=4)



@tool
def remember(memory: str) -> str:
    """
    Store important information about the user.
    """

    memories = load_memories()
    memories.append({"id": len(memories) + 1, "memory": memory})
    save_memories(memories)

    return f"Memory stored: {memory}"


@tool
def recall_memories() -> str:
    """
    Retrieve all stored memories.
    """

    memories = load_memories()

    if not memories:
        return "No memories found."

    return "\n".join(
        f"{m['id']}. {m['memory']}"
        for m in memories
    )
