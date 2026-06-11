"""Memory agent — stores and recalls user information."""

from langchain_core.messages import SystemMessage

from config import llm
from tools.memory_tools import remember, recall_memories


# --------------- LLM with tools ---------------

memory_llm = llm.bind_tools([remember, recall_memories])


# --------------- System prompt ---------------

SYSTEM_PROMPT = """You are the Memory Agent 🧠 of Jarvis.

AVAILABLE TOOLS:
1. remember — Store important information about the user.
2. recall_memories — Retrieve all stored memories.

RULES:
- Always use tools for memory operations — never invent data.
- After storing, confirm: "🧠 Got it! I'll remember that."
- When recalling, format memories as a clean list.
- If no memories are found, say: "🤔 I don't have any memories stored yet."
- Use emojis naturally (🧠, 💡, ✅, 📝).
- Be concise and helpful.
"""


# --------------- Agent function ---------------

def memory_agent(state):

    messages = [
        SystemMessage(content=SYSTEM_PROMPT)
    ] + state["messages"]

    response = memory_llm.invoke(messages)

    return {"messages": [response]}