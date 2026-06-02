from langchain_core.tools import tool

from database import conn, cursor


@tool
def add_todo(task: str) -> str:
    """
    Add task to todo list.
    """

    cursor.execute(
        "INSERT INTO todos(task) VALUES (?)",
        (task,)
    )

    conn.commit()

    return f"Task added: {task}"


@tool
def show_todos() -> str:
    """
    Show all todo items.
    """

    cursor.execute(
        "SELECT task FROM todos"
    )

    rows = cursor.fetchall()

    if not rows:
        return "Todo list is empty."

    return "\n".join(
        row[0]
        for row in rows
    )