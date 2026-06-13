"""Memory tools — JSON-only storage."""

import json
from pathlib import Path

from langchain_core.tools import tool



from langchain_core.runnables import RunnableConfig

def get_memory_file(config: RunnableConfig = None) -> Path:
    thread_id = None
    if config:
        thread_id = config.get("configurable", {}).get("thread_id")
    if thread_id:
        return Path("data") / thread_id / "memories.json"
    return Path("data/memories.json")


def load_memories(config: RunnableConfig = None):
    memory_file = get_memory_file(config)
    if not memory_file.exists():
        return []
    with open(memory_file, "r") as f:
        return json.load(f)


def save_memories(memories, config: RunnableConfig = None):
    memory_file = get_memory_file(config)
    memory_file.parent.mkdir(exist_ok=True, parents=True)
    with open(memory_file, "w") as f:
        json.dump(memories, f, indent=4)



@tool
def remember(memory: str, config: RunnableConfig = None) -> str:
    """
    Store important information about the user.
    """

    memories = load_memories(config)
    memories.append({"id": len(memories) + 1, "memory": memory})
    save_memories(memories, config)

    return f"Memory stored: {memory}"


@tool
def recall_memories(config: RunnableConfig = None) -> str:
    """
    Retrieve all stored memories.
    """

    memories = load_memories(config)

    if not memories:
        return "No memories found."

    return "\n".join(
        f"{m['id']}. {m['memory']}"
        for m in memories
    )

