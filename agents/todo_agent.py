from langchain_core.messages import SystemMessage

from config import llm

from tools.todo_tools import (
    add_todo,
    show_todos
)

todo_llm = llm.bind_tools(
    [add_todo, show_todos]
)


def todo_agent(state):

    print("todo_agent called")

    messages = [
        SystemMessage(
            content="""
            You manage todo tasks.
            Use tools whenever needed.
            """
        )
    ] + state["messages"]

    response = todo_llm.invoke(
        messages
    )

    return {
        "messages": [response]
    }