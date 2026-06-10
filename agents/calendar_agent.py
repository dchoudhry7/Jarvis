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
                
                RULES:
                
                1. Before creating an event, make sure you know:
                   - title
                   - date
                   - time
                
                2. If any required information is missing,
                   ask the user for it.
                
                3. Do NOT call create_event until all required
                   information has been collected.
                
                4. Once all information is available,
                   show a summary and ask for confirmation.
                
                Example:
                
                Title: Project Discussion
                Date: Tomorrow
                Time: 5 PM
                
                Would you like me to create this event?
                
                5. Only call create_event after the user clearly confirms.
                
                Examples of confirmation:
                
                - yes
                - yes create it
                - create it
                - confirm
                - go ahead
                
                6. Never create an event without confirmation.
                
                7. Always use tools for:
                   - creating events
                   - viewing events
                   - deleting events
                
                8. If information is missing, ask questions instead
                   of calling tools.
                """
        )
    ] + state["messages"]

    response = calendar_llm.invoke(
        messages
    )

    return {
        "messages": [response]
    }