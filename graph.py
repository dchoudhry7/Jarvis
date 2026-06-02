import os

from dotenv import load_dotenv

from typing import Annotated
from typing_extensions import TypedDict

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph
from langgraph.graph import END
from langgraph.graph.message import add_messages

from langgraph.prebuilt import ToolNode

from tools import (
    add_todo,
    show_todos,
    remember,
    recall_memories
)

from langgraph.checkpoint.memory import MemorySaver  # MemorySaver

load_dotenv()


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


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


def chatbot(state: AgentState):
    messages = [
                   SystemMessage(
                       content="""
                                You are Jarvis.
                                Rules:
                                1. If user says "remember" or asks you to store information, use remember tool.
                                2. If user asks about stored information, use recall_memories tool.
                                3. Use todo tools only for todo operations.
                                4. Never invent memories.
                                """
                   )
               ] + state["messages"]

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }


tool_node = ToolNode(tools)


def should_continue(state: AgentState):
    last_message = state["messages"][-1]

    print("\n========== ROUTER ==========")
    print(last_message)

    if last_message.tool_calls:
        print("GO TO TOOLS")
        return "tools"

    print("END GRAPH")
    return END


graph_builder = StateGraph(AgentState)

graph_builder.add_node(
    "chatbot",
    chatbot
)

graph_builder.add_node(
    "tools",
    tool_node
)

graph_builder.set_entry_point(
    "chatbot"
)

graph_builder.add_conditional_edges(
    "chatbot",
    should_continue
)

graph_builder.add_edge(
    "tools",
    "chatbot"
)

memory = MemorySaver()

graph = graph_builder.compile(
    checkpointer=memory
)
