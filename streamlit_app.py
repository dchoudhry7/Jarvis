"""
Jarvis — Multi-Agent Personal Assistant
Streamlit UI with session-scoped data reset.
"""

import json
import uuid
from pathlib import Path

import streamlit as st
from langchain_core.messages import HumanMessage

from graph import graph


# ============================================================
# Page Config
# ============================================================

st.set_page_config(
    page_title="Jarvis AI",
    page_icon="🤖",
    layout="centered",
)


# ============================================================
# Data File Paths
# ============================================================

DATA_DIR = Path("data")
TODO_FILE = DATA_DIR / "todos.json"
EMAIL_FILE = DATA_DIR / "email_drafts.json"
CALENDAR_FILE = DATA_DIR / "calendar.json"
PLAYLIST_FILE = DATA_DIR / "playlists.json"
MEMORY_FILE = DATA_DIR / "memories.json"
PENDING_EMAIL_FILE = DATA_DIR / "pending_email.json"
PENDING_EVENT_FILE = DATA_DIR / "pending_event.json"


# ============================================================
# Session Initialization
# ============================================================

def reset_data_files():
    """Reset all JSON data files to empty state."""
    DATA_DIR.mkdir(exist_ok=True)
    for f in [TODO_FILE, EMAIL_FILE, CALENDAR_FILE, PLAYLIST_FILE, MEMORY_FILE]:
        f.write_text("[]")
    for f in [PENDING_EMAIL_FILE, PENDING_EVENT_FILE]:
        f.write_text("{}")


if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.chat_history = []
    st.session_state.thread_id = str(uuid.uuid4())
    reset_data_files()


# ============================================================
# Helper
# ============================================================

def load_json(path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return []


# ============================================================
# Header
# ============================================================

st.markdown("## 🦾 JARVIS")
st.caption("Multi-Agent Personal Assistant powered by LangGraph")


# ============================================================
# Notice Box
# ============================================================

st.info(
    "📢 **Want real email & calendar integration?** "
    "This app uses Google OAuth which requires test-user access. "
    "Send a mail to **dchoudhry999@gmail.com** "
    "and I'll manually add you as a test user so you can use the full agentic features! 🚀"
)


# ============================================================
# Stats Row
# ============================================================

todos = load_json(TODO_FILE)
emails = load_json(EMAIL_FILE)
events = load_json(CALENDAR_FILE)
playlists = load_json(PLAYLIST_FILE)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Agents", 6)
c2.metric("Todos", len(todos))
c3.metric("Emails", len(emails))
c4.metric("Events", len(events))
c5.metric("Playlists", len(playlists))


# ============================================================
# Tabs
# ============================================================

chat_tab, todo_tab, email_tab, calendar_tab, spotify_tab = st.tabs([
    "💬 Chat", "📝 Todos", "📧 Emails", "📅 Calendar", "🎵 Spotify"
])


# -------------------- Chat Tab --------------------

with chat_tab:

    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(message)

    user_input = st.chat_input("Talk to Jarvis...")

    if user_input:
        st.session_state.chat_history.append(("user", user_input))

        result = graph.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config={"configurable": {"thread_id": st.session_state.thread_id}},
        )

        response = result["messages"][-1].content
        st.session_state.chat_history.append(("assistant", response))
        st.rerun()


# -------------------- Todos Tab --------------------

with todo_tab:

    st.subheader("📝 Todo List")

    todos = load_json(TODO_FILE)

    if todos:
        for todo in todos:
            st.write(f"☐ **{todo.get('task', '')}**")
    else:
        st.info("No todos yet. Ask Jarvis to add one!")


# -------------------- Emails Tab --------------------

with email_tab:

    st.subheader("📧 Email Drafts")

    emails = load_json(EMAIL_FILE)

    if emails:
        for draft in emails:
            with st.expander(f"📧 {draft.get('subject', 'No Subject')}"):
                st.write(f"**To:** {draft.get('recipient', 'Unknown')}")
                st.write(f"**Draft ID:** {draft.get('id', '')}")
                st.divider()
                st.write(draft.get("content", ""))
    else:
        st.info("No email drafts. Ask Jarvis to draft one!")


# -------------------- Calendar Tab --------------------

with calendar_tab:

    st.subheader("📅 Calendar Events")

    events = load_json(CALENDAR_FILE)

    if events:
        for event in events:
            st.write(f"📅 **{event.get('title', 'Untitled')}** — {event.get('date', '')} at {event.get('time', '')}")
    else:
        st.info("No events yet. Ask Jarvis to create one!")


# -------------------- Spotify Tab --------------------

with spotify_tab:

    st.subheader("🎵 Playlists")

    playlists = load_json(PLAYLIST_FILE)

    if playlists:
        for playlist in playlists:
            with st.expander(f"🎵 {playlist.get('name', 'Unnamed')}"):
                songs = playlist.get("songs", [])
                if songs:
                    for song in songs:
                        st.write(f"• {song}")
                else:
                    st.info("No songs in this playlist.")
    else:
        st.info("No playlists yet. Ask Jarvis to create one!")