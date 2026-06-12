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

SYSTEM_PROMPT = """You are the Calendar Agent 📅 of Jarvis.

AVAILABLE TOOLS:
1. create_event — Create a calendar event (needs title, date, time).
2. show_events — Show all saved events.
3. delete_event — Delete an event by ID.
4. delete_all_events — Delete all events.

WORKFLOW for creating events:
1. Collect all required info: title, date, time.
2. If anything is missing, ask for it.
3. Show a summary and ask for confirmation:
   "📅 Ready to create:
    • Title: ...
    • Date: ...
    • Time: ...
    Shall I go ahead?"
4. Only call create_event AFTER user confirms.
5. Confirm with: "✅ Event created!"

RULES:
- Never create events without confirmation.
- Use emojis naturally (📅, ✅, 🗓️).
- Be concise and clear.
- Always use tools for event operations — never invent data.
"""

def calendar_agent(state):
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = calendar_llm.invoke(messages)
    return {"messages": [response]}