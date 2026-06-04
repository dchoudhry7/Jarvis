from langgraph.graph import END


def email_router(state):

    last_message = state["messages"][-1]

    print("\nEMAIL ROUTER")

    if getattr(last_message, "tool_calls", None):
        print("GO TO EMAIL TOOLS")
        return "email_tools"

    print("END")
    return END