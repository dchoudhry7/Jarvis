"""Todo tools — JSON-only storage."""

import json
from pathlib import Path

from langchain_core.tools import tool



from langchain_core.runnables import RunnableConfig

def get_todo_file(config: RunnableConfig = None) -> Path:
    thread_id = None
    if config:
        thread_id = config.get("configurable", {}).get("thread_id")
    if thread_id:
        return Path("data") / thread_id / "todos.json"
    return Path("data/todos.json")


def load_todos(config: RunnableConfig = None):
    todo_file = get_todo_file(config)
    if not todo_file.exists():
        return []
    with open(todo_file, "r") as f:
        return json.load(f)


def save_todos(todos, config: RunnableConfig = None):
    todo_file = get_todo_file(config)
    todo_file.parent.mkdir(exist_ok=True, parents=True)
    with open(todo_file, "w") as f:
        json.dump(todos, f, indent=4)



@tool
def add_todo(task: str, config: RunnableConfig = None) -> str:
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

    todos = load_todos(config)

    todos.append({
        "id": len(todos) + 1,
        "task": task,
    })

    save_todos(todos, config)

    return f"Task added: {task}"


@tool
def show_todos(config: RunnableConfig = None) -> str:
    """
    Show all saved todo items.

    Use this tool when the user wants to:
    - see todos
    - list tasks
    - show tasks
    - view todo list

    Do not use this tool for adding tasks.
    """

    todos = load_todos(config)

    if not todos:
        return "Todo list is empty."

    return "\n".join(
        f"{todo['id']}. {todo['task']}"
        for todo in todos
    )

