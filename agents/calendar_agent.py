from langchain_core.messages import SystemMessage

from config import llm

from tools.calendar_tools import (
    create_event,
    show_events,
    delete_event,
    delete_all_events
)


calendar_llm = llm.bind_tools(
    [
        create_event,
        show_events,
        delete_event,
        delete_all_events
    ]
)


def calendar_agent(state):

    print("calendar_agent called")

    messages = [
        SystemMessage(
            content="""
            You are a Calendar Agent.

            Available tools:

            - create_event
            - show_events
            - delete_event
            - delete_all_events

            Always use tools for calendar operations.
            """
        )
    ] + state["messages"]

    response = calendar_llm.invoke(
        messages
    )

    return {
        "messages": [response]
    }