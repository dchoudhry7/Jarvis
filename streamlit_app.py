import streamlit as st

from langchain_core.messages import HumanMessage

from graph import graph


st.set_page_config(
    page_title="Jarvis AI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Jarvis AI Assistant")


user_input = st.chat_input(
    "Talk to Jarvis..."
)

if user_input:

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content=user_input
                )
            ]
        },
        config={
            "configurable": {
                "thread_id": "user_1"
            }
        }
    )

    response = result["messages"][-1].content

    st.write(response)