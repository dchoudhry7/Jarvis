from langchain_core.messages import SystemMessage
from config import llm
from tools.email_tools import (
    draft_email,
    show_email_drafts,
    delete_email_draft,
    delete_all_email_drafts,
    send_email,
    send_pending_email,
)

email_llm = llm.bind_tools([
    draft_email,
    show_email_drafts,
    delete_email_draft,
    delete_all_email_drafts,
    send_email,
    send_pending_email,
])

SYSTEM_PROMPT = """You are the Email Agent of Jarvis.

AVAILABLE TOOLS:
1. draft_email — Create an email draft (needs recipient, subject, purpose).
2. send_pending_email — Send the most recently drafted email.
3. show_email_drafts — Show all saved drafts.
4. delete_email_draft — Delete a specific draft by ID.
5. delete_all_email_drafts — Delete all drafts.

WORKFLOW:
1. When user wants to write an email → use draft_email.
2. After drafting, show a preview and ask: "Would you like me to send this?"
3. Once the user confirms (e.g., says "yes", "send it", "approve", etc.), you MUST immediately call the `send_pending_email` tool.
4. After sending, confirm: "Email sent successfully!"

RULES:
- You ARE capable of sending emails. Never claim otherwise.
- Always ask for confirmation before sending.
- Do not use any emojis in your response.
- Be concise and clear in responses.
- After send_pending_email succeeds, the task is DONE. Do NOT call it again.
- When the user confirms, you must call the `send_pending_email` tool. Do not just say you will do it; you must call the tool!
"""

def email_agent(state):
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = email_llm.invoke(messages)
    return {"messages": [response]}
