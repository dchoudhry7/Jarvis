import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def _get_api_key():
    """Get GROQ_API_KEY from Streamlit secrets, .env, or environment."""
    try:
        import streamlit as st
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        pass

    return os.getenv("GROQ_API_KEY")


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=_get_api_key()
)
