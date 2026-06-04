from langgraph.graph import (
    StateGraph,
    END
)

from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from state import AgentState

from agents.supervisor import (
    supervisor,
    route_agent
)

from agents.chat_agent import (
    chat_agent
)

from agents.todo_agent import (
    todo_agent
)

from agents.memory_agent import (
    memory_agent
)

from agents.email_agent import (
    email_agent
)

from routers.todo_router import (
    todo_router
)

from routers.memory_router import (
    memory_router
)

from routers.email_router import (
    email_router
)

from tools.todo_tools import (
    add_todo,
    show_todos
)

from tools.memory_tools import (
    remember,
    recall_memories
)

from tools.email_tools import (
    draft_email,
    show_email_drafts,
    delete_email_draft,
    delete_all_email_drafts
)


todo_tool_node = ToolNode(
    [
        add_todo,
        show_todos
    ]
)

memory_tool_node = ToolNode(
    [
        remember,
        recall_memories
    ]
)

email_tool_node = ToolNode(
    [
        draft_email,
        show_email_drafts,
        delete_email_draft,
        delete_all_email_drafts
    ]
)

graph_builder = StateGraph(
    AgentState
)


graph_builder.add_node(
    "supervisor",
    supervisor
)

graph_builder.add_node(
    "todo_agent",
    todo_agent
)

graph_builder.add_node(
    "memory_agent",
    memory_agent
)

graph_builder.add_node(
    "chat_agent",
    chat_agent
)

graph_builder.add_node(
    "todo_tools",
    todo_tool_node
)

graph_builder.add_node(
    "memory_tools",
    memory_tool_node
)

graph_builder.add_node(
    "email_agent",
    email_agent
)

graph_builder.add_node(
    "email_tools",
    email_tool_node
)


graph_builder.set_entry_point(
    "supervisor"
)


graph_builder.add_conditional_edges(
    "supervisor",
    route_agent,
    {
        "todo": "todo_agent",
        "memory": "memory_agent",
        "chat": "chat_agent",
        "email": "email_agent"
    }
)


graph_builder.add_conditional_edges(
    "todo_agent",
    todo_router,
    {
        "todo_tools": "todo_tools",
        END: END
    }
)

graph_builder.add_conditional_edges(
    "memory_agent",
    memory_router,
    {
        "memory_tools": "memory_tools",
        END: END
    }
)

graph_builder.add_conditional_edges(
    "email_agent",
    email_router,
    {
        "email_tools": "email_tools",
        END: END
    }
)


graph_builder.add_edge(
    "todo_tools",
    "todo_agent"
)

graph_builder.add_edge(
    "memory_tools",
    "memory_agent"
)

graph_builder.add_edge(
    "email_tools",
    "email_agent"
)

graph_builder.add_edge(
    "chat_agent",
    END
)


memory = MemorySaver()

graph = graph_builder.compile(
    checkpointer=memory
)


if __name__ == "__main__":

    print(
        graph.get_graph().draw_mermaid()
    )

    png = graph.get_graph().draw_mermaid_png()

    with open(
        "graph.png",
        "wb"
    ) as f:
        f.write(png)

    print("graph.png saved")