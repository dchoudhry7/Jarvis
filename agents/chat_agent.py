from config import llm


def chat_agent(state):

    print("chat_agent called")

    response = llm.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }