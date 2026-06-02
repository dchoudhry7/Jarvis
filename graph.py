import os

from dotenv import load_dotenv

from typing import Annotated
from typing_extensions import TypedDict

from langchain_groq import ChatGroq

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

load_dotenv()


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)


def chatbot(state: AgentState):
    response = llm.invoke(state["messages"])

    return {
        "messages": [response]
    }


graph_builder = StateGraph(AgentState)

graph_builder.add_node("chatbot", chatbot)

graph_builder.set_entry_point("chatbot")

graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()
