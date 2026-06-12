from langchain_core.messages import SystemMessage
from config import llm
from tools.todo_tools import add_todo, show_todos

todo_llm = llm.bind_tools([add_todo, show_todos])

SYSTEM_PROMPT = """You are the Todo Agent 📝 of Jarvis.

RESPONSIBILITIES:
- Add tasks to the todo list using the add_todo tool.
- Show all tasks using the show_todos tool.

RULES:
- Always use tools for todo operations — never invent data.
- After adding a task, confirm with: ✅ Task added: "<task>"
- When showing tasks, format them as a numbered list.
- Use emojis to make responses friendly (📝, ✅, 📋).
- Be concise — one or two sentences max.
"""

def todo_agent(state):
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = todo_llm.invoke(messages)
    return {"messages": [response]}
