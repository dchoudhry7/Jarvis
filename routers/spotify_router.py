from langgraph.graph import END


def spotify_router(state):

    last_message = state["messages"][-1]

    print("\nSPOTIFY ROUTER")

    if getattr(last_message, "tool_calls", None):

        print("GO TO SPOTIFY TOOLS")

        return "spotify_tools"

    print("END")

    return END