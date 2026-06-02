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

from tools import add_todo, show_todos

from langgraph.checkpoint.memory import MemorySaver  #MemorySaver

load_dotenv()


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


tools = [
    add_todo,
    show_todos
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
You are a todo assistant.

Rules:
1. Use add_todo only when user wants to add a task.
2. Use show_todos only when user wants to view tasks.
3. After receiving tool output, answer the user directly.
4. Never call a tool twice for the same request.
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