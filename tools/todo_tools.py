"""Todo tools — JSON-only storage."""

import json
from pathlib import Path

from langchain_core.tools import tool


# --------------- Storage ---------------

TODO_FILE = Path("data/todos.json")


def load_todos():
    if not TODO_FILE.exists():
        return []
    with open(TODO_FILE, "r") as f:
        return json.load(f)


def save_todos(todos):
    TODO_FILE.parent.mkdir(exist_ok=True)
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f, indent=4)


# --------------- Tools ---------------

@tool
def add_todo(task: str) -> str:
    """
    Add a new task to the todo list.

    Use this tool when the user wants to:
    - add a task
    - create a todo
    - remember something to do
    - save a task

    Args:
        task: The task to be added.

    Do not use this tool for viewing tasks.
    """

    todos = load_todos()

    todos.append({
        "id": len(todos) + 1,
        "task": task,
    })

    save_todos(todos)

    return f"Task added: {task}"


@tool
def show_todos() -> str:
    """
    Show all saved todo items.

    Use this tool when the user wants to:
    - see todos
    - list tasks
    - show tasks
    - view todo list

    Do not use this tool for adding tasks.
    """

    todos = load_todos()

    if not todos:
        return "Todo list is empty."

    return "\n".join(
        f"{todo['id']}. {todo['task']}"
        for todo in todos
    )