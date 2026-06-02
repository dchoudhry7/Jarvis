from langchain_core.tools import tool


@tool
def add_todo(task: str) -> str:
    """
    Add task to todo list.
    """

    return f"Task added: {task}"