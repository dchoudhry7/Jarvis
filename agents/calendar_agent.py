from langchain_core.messages import SystemMessage
from config import llm
from tools.calendar_tools import (
    create_event,
    show_events,
    delete_event,
    delete_all_events,
)

calendar_llm = llm.bind_tools([
    create_event,
    show_events,
    delete_event,
    delete_all_events,
])

SYSTEM_PROMPT = """You are the Calendar Agent of Jarvis.

AVAILABLE TOOLS:
1. create_event — Create a calendar event (needs title, date, time).
2. show_events — Show all saved events.
3. delete_event — Delete an event by ID.
4. delete_all_events — Delete all events.

WORKFLOW for creating events:
1. Collect all required info: title, date, time.
2. If anything is missing, ask for it.
3. Show a summary and ask for confirmation:
   "Ready to create:
    • Title: ...
    • Date: ...
    • Time: ...
    Shall I go ahead?"
4. Once the user confirms (e.g., says "yes", "go ahead", "sure", etc.), you MUST immediately call the `create_event` tool with the confirmed title, date, and time.
5. After the `create_event` tool executes and returns, you should confirm with the user that the event was created.

RULES:
- Never create events without confirmation.
- Do not use any emojis in your response.
- Be concise and clear.
- Always use tools for event operations — never invent data.
- When the user confirms, call the `create_event` tool. Do not just say you will do it; you must call the tool!
"""

def calendar_agent(state):
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = calendar_llm.invoke(messages)
    return {"messages": [response]}
