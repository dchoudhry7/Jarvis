from langchain_core.tools import tool

from database import conn, cursor


@tool
def remember(memory: str) -> str:
    """
    Store important information about the user.
    """

    cursor.execute(
        "INSERT INTO memories(memory) VALUES (?)",
        (memory,)
    )

    conn.commit()

    return f"Memory stored: {memory}"


@tool
def recall_memories() -> str:
    """
    Retrieve all stored memories.
    """

    cursor.execute(
        "SELECT memory FROM memories"
    )

    rows = cursor.fetchall()

    if not rows:
        return "No memories found."

    return "\n".join(
        row[0]
        for row in rows
    )