"""
LangGraph multi-agent workflow.

Supervisor routes messages to specialized agents,
each with their own tool nodes and routing logic.
"""

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from state import AgentState

# --------------- Agents ---------------

from agents.supervisor import supervisor, route_agent
from agents.chat_agent import chat_agent
from agents.todo_agent import todo_agent
from agents.memory_agent import memory_agent
from agents.email_agent import email_agent
from agents.calendar_agent import calendar_agent
from agents.spotify_agent import spotify_agent

# --------------- Routers ---------------

from routers.todo_router import todo_router
from routers.memory_router import memory_router
from routers.email_router import email_router
from routers.calendar_router import calendar_router
from routers.spotify_router import spotify_router

# --------------- Tools ---------------

from tools.todo_tools import add_todo, show_todos
from tools.memory_tools import remember, recall_memories
from tools.email_tools import (
    draft_email, show_email_drafts, delete_email_draft,
    delete_all_email_drafts, send_email, send_pending_email,
)
from tools.calendar_tools import (
    create_event, show_events, delete_event, delete_all_events,
)
from tools.spotify_tools import (
    add_song_to_playlist, show_playlists,
    remove_song_from_playlist, delete_playlist,
)


# ============================================================
# Tool Nodes
# ============================================================

todo_tool_node = ToolNode([add_todo, show_todos])
memory_tool_node = ToolNode([remember, recall_memories])

email_tool_node = ToolNode([
    draft_email, show_email_drafts, delete_email_draft,
    delete_all_email_drafts, send_email, send_pending_email,
])

calendar_tool_node = ToolNode([
    create_event, show_events, delete_event, delete_all_events,
])

spotify_tool_node = ToolNode([
    add_song_to_playlist, show_playlists,
    remove_song_from_playlist, delete_playlist,
])


# ============================================================
# Build Graph
# ============================================================

graph_builder = StateGraph(AgentState)

# --- Nodes ---

graph_builder.add_node("supervisor", supervisor)
graph_builder.add_node("chat_agent", chat_agent)

graph_builder.add_node("todo_agent", todo_agent)
graph_builder.add_node("todo_tools", todo_tool_node)

graph_builder.add_node("memory_agent", memory_agent)
graph_builder.add_node("memory_tools", memory_tool_node)

graph_builder.add_node("email_agent", email_agent)
graph_builder.add_node("email_tools", email_tool_node)

graph_builder.add_node("calendar_agent", calendar_agent)
graph_builder.add_node("calendar_tools", calendar_tool_node)

graph_builder.add_node("spotify_agent", spotify_agent)
graph_builder.add_node("spotify_tools", spotify_tool_node)

# --- Entry point ---

graph_builder.set_entry_point("supervisor")

# --- Supervisor routing ---

graph_builder.add_conditional_edges("supervisor", route_agent, {
    "todo": "todo_agent",
    "memory": "memory_agent",
    "chat": "chat_agent",
    "email": "email_agent",
    "calendar": "calendar_agent",
    "spotify": "spotify_agent",
})

# --- Agent → Tool routing ---

graph_builder.add_conditional_edges("todo_agent", todo_router, {
    "todo_tools": "todo_tools", END: END,
})
graph_builder.add_conditional_edges("memory_agent", memory_router, {
    "memory_tools": "memory_tools", END: END,
})
graph_builder.add_conditional_edges("email_agent", email_router, {
    "email_tools": "email_tools", END: END,
})
graph_builder.add_conditional_edges("calendar_agent", calendar_router, {
    "calendar_tools": "calendar_tools", END: END,
})
graph_builder.add_conditional_edges("spotify_agent", spotify_router, {
    "spotify_tools": "spotify_tools", END: END,
})

# --- Tool → Agent edges ---

graph_builder.add_edge("todo_tools", "todo_agent")
graph_builder.add_edge("memory_tools", "memory_agent")
graph_builder.add_edge("email_tools", "email_agent")
graph_builder.add_edge("calendar_tools", "calendar_agent")
graph_builder.add_edge("spotify_tools", "spotify_agent")

# --- Chat ends directly ---

graph_builder.add_edge("chat_agent", END)


# ============================================================
# Compile
# ============================================================

graph = graph_builder.compile()