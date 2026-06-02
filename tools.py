from langchain_core.tools import tool

todos = []


@tool
def add_todo(task: str) -> str:
    """
    Add a task to todo list.
    """

    todos.append(task)

    return f"Added task: {task}"


@tool
def show_todos() -> str:
    """
    Show all todo items.
    """

    if not todos:
        return "Todo list is empty."

    return "\n".join(todos)