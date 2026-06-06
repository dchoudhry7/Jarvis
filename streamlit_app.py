import streamlit as st

from langchain_core.messages import HumanMessage

from graph import graph


st.set_page_config(
    page_title="Jarvis AI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Jarvis AI Assistant")

if st.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


for role, message in st.session_state.chat_history:

    with st.chat_message(role):
        st.markdown(message)


user_input = st.chat_input(
    "Talk to Jarvis..."
)

if user_input:

    st.session_state.chat_history.append(
        ("user", user_input)
    )

    with st.chat_message("user"):
        st.markdown(user_input)

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

    st.session_state.chat_history.append(
        ("assistant", response)
    )

    with st.chat_message("assistant"):
        st.markdown(response)