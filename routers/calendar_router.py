from langgraph.graph import END


def calendar_router(state):

    last_message = state["messages"][-1]

    print("\nCALENDAR ROUTER")

    if getattr(last_message, "tool_calls", None):
        print("GO TO CALENDAR TOOLS")
        return "calendar_tools"

    print("END")
    return END