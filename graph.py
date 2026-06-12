from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

from state import AgentState

from agents.supervisor import supervisor, route_agent
from agents.chat_agent import chat_agent
from agents.todo_agent import todo_agent
from agents.memory_agent import memory_agent
from agents.email_agent import email_agent
from agents.calendar_agent import calendar_agent
from agents.spotify_agent import spotify_agent

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

graph_builder = StateGraph(AgentState)

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

graph_builder.set_entry_point("supervisor")

graph_builder.add_conditional_edges("supervisor", route_agent, {
    "todo": "todo_agent",
    "memory": "memory_agent",
    "chat": "chat_agent",
    "email": "email_agent",
    "calendar": "calendar_agent",
    "spotify": "spotify_agent",
})

graph_builder.add_conditional_edges("todo_agent", tools_condition, {
    "tools": "todo_tools", "__end__": END
})
graph_builder.add_conditional_edges("memory_agent", tools_condition, {
    "tools": "memory_tools", "__end__": END
})
graph_builder.add_conditional_edges("email_agent", tools_condition, {
    "tools": "email_tools", "__end__": END
})
graph_builder.add_conditional_edges("calendar_agent", tools_condition, {
    "tools": "calendar_tools", "__end__": END
})
graph_builder.add_conditional_edges("spotify_agent", tools_condition, {
    "tools": "spotify_tools", "__end__": END
})

graph_builder.add_edge("todo_tools", "todo_agent")
graph_builder.add_edge("memory_tools", "memory_agent")
graph_builder.add_edge("email_tools", "email_agent")
graph_builder.add_edge("calendar_tools", "calendar_agent")
graph_builder.add_edge("spotify_tools", "spotify_agent")

graph_builder.add_edge("chat_agent", END)

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

if __name__ == "__main__":
    try:
        mermaid = graph.get_graph().draw_mermaid()
        print(mermaid)
        png = graph.get_graph().draw_mermaid_png()
        with open("graph.png", "wb") as f:
            f.write(png)
        print("graph.png saved successfully!")
    except Exception as e:
        print(f"Mermaid drawing skipped/failed: {e}")