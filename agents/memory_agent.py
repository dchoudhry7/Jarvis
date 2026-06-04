from langchain_core.messages import SystemMessage

from config import llm

from tools.memory_tools import (
    remember,
    recall_memories
)

memory_llm = llm.bind_tools(
    [remember, recall_memories]
)


def memory_agent(state):

    print("memory_agent called")

    messages = [
        SystemMessage(
            content="""
            You are the Memory Agent.

            Responsibilities:
            - Store information using remember.
            - Retrieve information using recall_memories.
            - Never invent memories.
            - If information is not found, say so.
            - Use tools whenever memory operations are required.
            """
        )
    ] + state["messages"]

    response = memory_llm.invoke(
        messages
    )

    return {
        "messages": [response]
    }