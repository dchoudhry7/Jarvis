import os

from dotenv import load_dotenv

from typing import Annotated
from typing_extensions import TypedDict

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from tools import (
    add_todo,
    show_todos,
    remember,
    recall_memories
)

load_dotenv()


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    route: str


tools = [
    add_todo,
    show_todos,
    remember,
    recall_memories
]


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

llm_with_tools = llm.bind_tools(tools)


def supervisor(state: AgentState):

    user_message = state["messages"][-1].content.lower()

    if any(word in user_message for word in [
        "todo",
        "task",
        "add task",
        "show task"
    ]):
        route = "todo"

    elif any(word in user_message for word in [
        "remember",
        "memory",
        "recall"
    ]):
        route = "memory"

    else:
        route = "chat"

    print(f"\nSUPERVISOR ROUTED TO: {route}")

    return {
        "route": route
    }


def todo_agent(state: AgentState):

    print("todo_agent called")

    messages = [
        SystemMessage(
            content="""
            You manage todo tasks.
            Use todo tools whenever needed.
            """
        )
    ] + state["messages"]

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }


def memory_agent(state: AgentState):

    print("memory_agent called")

    messages = [
        SystemMessage(
            content="""
            You manage memories.
            Use remember and recall_memories tools.
            Never invent memories.
            """
        )
    ] + state["messages"]

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }


def chat_agent(state: AgentState):

    print("chat_agent called")

    response = llm.invoke(state["messages"])

    return {
        "messages": [response]
    }


tool_node = ToolNode(tools)


def route_agent(state: AgentState):
    return state["route"]


def should_continue(state: AgentState):

    last_message = state["messages"][-1]

    print("\n========== ROUTER ==========")
    print(last_message)

    if getattr(last_message, "tool_calls", None):
        print("GO TO TOOLS")
        return "tools"

    print("END GRAPH")
    return END


graph_builder = StateGraph(AgentState)

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
    "tools",
    tool_node
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
        "chat": "chat_agent"
    }
)

graph_builder.add_conditional_edges(
    "todo_agent",
    should_continue
)

graph_builder.add_conditional_edges(
    "memory_agent",
    should_continue
)

graph_builder.add_edge(
    "tools",
    "memory_agent"
)

graph_builder.add_edge(
    "tools",
    "todo_agent"
)

graph_builder.add_edge(
    "chat_agent",
    END
)

memory = MemorySaver()

graph = graph_builder.compile(
    checkpointer=memory
)
mermaid = graph.get_graph().draw_mermaid()

print(mermaid)

png = graph.get_graph().draw_mermaid_png()

with open("graph.png", "wb") as f:
    f.write(png)

print("Saved graph.png")