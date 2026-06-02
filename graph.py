import os

from dotenv import load_dotenv

from typing import Annotated
from typing_extensions import TypedDict

from langchain_groq import ChatGroq

from langgraph.graph import StateGraph
from langgraph.graph import END
from langgraph.graph.message import add_messages

from langgraph.prebuilt import ToolNode

from tools import add_todo, show_todos

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

    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


tool_node = ToolNode(tools)


def should_continue(state: AgentState):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

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

graph = graph_builder.compile()