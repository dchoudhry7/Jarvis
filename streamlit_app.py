"""
Jarvis — Multi-Agent Personal Assistant
Streamlit UI with session-scoped data reset.
"""

import json
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
# Custom CSS — clean, minimal, Bootstrap-inspired
# ============================================================

st.markdown("""
<style>
    /* --- Global --- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* --- Hide Streamlit branding --- */
    #MainMenu, footer, header {visibility: hidden;}

    /* --- Notice box --- */
    .notice-box {
        background: linear-gradient(135deg, #1e3a5f 0%, #1a1a2e 100%);
        border: 1px solid #2d5a8e;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 24px;
        color: #cbd5e1;
        font-size: 14px;
        line-height: 1.6;
    }
    .notice-box strong { color: #60a5fa; }
    .notice-box a { color: #93c5fd; text-decoration: none; }
    .notice-box a:hover { text-decoration: underline; }

    /* --- Stat cards --- */
    .stat-row {
        display: flex;
        gap: 12px;
        margin-bottom: 24px;
    }
    .stat-card {
        flex: 1;
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }
    .stat-card .label {
        font-size: 12px;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    .stat-card .value {
        font-size: 28px;
        font-weight: 700;
        color: #f9fafb;
    }

    /* --- Section headers --- */
    .section-header {
        font-size: 16px;
        font-weight: 600;
        color: #e5e7eb;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid #1f2937;
    }

    /* --- Item cards --- */
    .item-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 8px;
        padding: 14px 16px;
        margin-bottom: 8px;
        color: #d1d5db;
        font-size: 14px;
    }
    .item-card .item-title {
        font-weight: 600;
        color: #f3f4f6;
        margin-bottom: 4px;
    }
    .item-card .item-meta {
        font-size: 12px;
        color: #6b7280;
    }

    /* --- Empty state --- */
    .empty-state {
        text-align: center;
        padding: 40px 20px;
        color: #4b5563;
        font-size: 14px;
    }
    .empty-state .icon {
        font-size: 32px;
        margin-bottom: 8px;
    }

    /* --- Tabs styling --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 8px 16px;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)


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
# Session Reset — fresh data for every new visitor
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
    reset_data_files()


# ============================================================
# Helper — load JSON safely
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

st.markdown("""
<div class="notice-box">
    📢 <strong>Want real email & calendar integration?</strong><br>
    This app uses Google OAuth which requires test-user access.
    Send a mail to <a href="mailto:dchoudhry999@gmail.com"><strong>dchoudhry999@gmail.com</strong></a>
    and I'll manually add you as a test user so you can use the full agentic features! 🚀
</div>
""", unsafe_allow_html=True)


# ============================================================
# Stats Row
# ============================================================

todos = load_json(TODO_FILE)
emails = load_json(EMAIL_FILE)
events = load_json(CALENDAR_FILE)
playlists = load_json(PLAYLIST_FILE)

st.markdown(f"""
<div class="stat-row">
    <div class="stat-card">
        <div class="label">Agents</div>
        <div class="value">6</div>
    </div>
    <div class="stat-card">
        <div class="label">Todos</div>
        <div class="value">{len(todos)}</div>
    </div>
    <div class="stat-card">
        <div class="label">Emails</div>
        <div class="value">{len(emails)}</div>
    </div>
    <div class="stat-card">
        <div class="label">Events</div>
        <div class="value">{len(events)}</div>
    </div>
    <div class="stat-card">
        <div class="label">Playlists</div>
        <div class="value">{len(playlists)}</div>
    </div>
</div>
""", unsafe_allow_html=True)


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
        reset_data_files()
        st.rerun()

    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(message)

    user_input = st.chat_input("Talk to Jarvis...")

    if user_input:
        st.session_state.chat_history.append(("user", user_input))

        result = graph.invoke(
            {"messages": [HumanMessage(content=user_input)]},
        )

        response = result["messages"][-1].content
        st.session_state.chat_history.append(("assistant", response))
        st.rerun()


# -------------------- Todos Tab --------------------

with todo_tab:

    st.markdown('<div class="section-header">📝 Todo List</div>', unsafe_allow_html=True)

    todos = load_json(TODO_FILE)

    if todos:
        for todo in todos:
            st.markdown(f"""
            <div class="item-card">
                <div class="item-title">☐ {todo.get("task", "")}</div>
                <div class="item-meta">ID: {todo.get("id", "")}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="icon">📝</div>
            No todos yet. Ask Jarvis to add one!
        </div>
        """, unsafe_allow_html=True)


# -------------------- Emails Tab --------------------

with email_tab:

    st.markdown('<div class="section-header">📧 Email Drafts</div>', unsafe_allow_html=True)

    emails = load_json(EMAIL_FILE)

    if emails:
        for draft in emails:
            subject = draft.get("subject", "No Subject")
            recipient = draft.get("recipient", "Unknown")
            content = draft.get("content", "")

            with st.expander(f"📧 {subject}"):
                st.markdown(f"**To:** {recipient}")
                st.markdown(f"**Draft ID:** {draft.get('id', '')}")
                st.markdown("---")
                st.write(content)
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="icon">📧</div>
            No email drafts. Ask Jarvis to draft one!
        </div>
        """, unsafe_allow_html=True)


# -------------------- Calendar Tab --------------------

with calendar_tab:

    st.markdown('<div class="section-header">📅 Calendar Events</div>', unsafe_allow_html=True)

    events = load_json(CALENDAR_FILE)

    if events:
        for event in events:
            title = event.get("title", "Untitled")
            date = event.get("date", "")
            time = event.get("time", "")

            st.markdown(f"""
            <div class="item-card">
                <div class="item-title">📅 {title}</div>
                <div class="item-meta">🗓️ {date} &nbsp;•&nbsp; ⏰ {time}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="icon">📅</div>
            No events yet. Ask Jarvis to create one!
        </div>
        """, unsafe_allow_html=True)


# -------------------- Spotify Tab --------------------

with spotify_tab:

    st.markdown('<div class="section-header">🎵 Playlists</div>', unsafe_allow_html=True)

    playlists = load_json(PLAYLIST_FILE)

    if playlists:
        for playlist in playlists:
            name = playlist.get("name", "Unnamed")
            songs = playlist.get("songs", [])

            with st.expander(f"🎵 {name}"):
                if songs:
                    for song in songs:
                        st.write(f"• {song}")
                else:
                    st.info("No songs in this playlist.")
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="icon">🎵</div>
            No playlists yet. Ask Jarvis to create one!
        </div>
        """, unsafe_allow_html=True)