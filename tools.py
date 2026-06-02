from langchain_core.tools import tool

todos = []


@tool
def add_todo(task: str) -> str:
    """
    Add a task to the list of todos
    :param task:
    :return:
    """
    print("ADD TODO TOOL CALLED:", task)

    todos.append(task)

    return f"Task added: {task}"


@tool
def show_todos() -> str:
    """
    Show the list of todos
    :return:
    """
    print("SHOW TODOS TOOL CALLED")

    if not todos:
        return "Todo list is empty."

    return "\n".join(todos)