from langgraph.graph import END


def todo_router(state):

    last_message = state["messages"][-1]

    if getattr(last_message, "tool_calls", None):
        return "todo_tools"

    return END