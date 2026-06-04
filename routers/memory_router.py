from langgraph.graph import END


def memory_router(state):

    last_message = state["messages"][-1]

    print("\nMEMORY ROUTER")

    if getattr(last_message, "tool_calls", None):
        print("GO TO MEMORY TOOLS")
        return "memory_tools"

    print("END")
    return END