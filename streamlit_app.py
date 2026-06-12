import json
import uuid
import time
from pathlib import Path
import streamlit as st
from langchain_core.messages import HumanMessage
from graph import graph

st.set_page_config(
    page_title="Jarvis AI",
    page_icon=":material/rocket:",
    layout="centered",
)

DATA_DIR = Path("data")
TODO_FILE = DATA_DIR / "todos.json"
EMAIL_FILE = DATA_DIR / "email_drafts.json"
CALENDAR_FILE = DATA_DIR / "calendar.json"
PLAYLIST_FILE = DATA_DIR / "playlists.json"
MEMORY_FILE = DATA_DIR / "memories.json"
PENDING_EMAIL_FILE = DATA_DIR / "pending_email.json"
PENDING_EVENT_FILE = DATA_DIR / "pending_event.json"

def reset_data_files():
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

def load_json(path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return []

def render_chat_message(role, text):
    if role == "user":
        st.markdown(
            f"""
            <div style="display: flex; justify-content: flex-end; margin-bottom: 12px;">
                <div style="
                    background-color: rgba(128, 128, 128, 0.08); 
                    border: 1px solid rgba(128, 128, 128, 0.15); 
                    border-radius: 12px; 
                    padding: 10px 14px; 
                    max-width: 80%;
                ">
                    {text}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="display: flex; justify-content: flex-start; margin-bottom: 12px;">
                <div style="
                    background-color: rgba(96, 165, 250, 0.1); 
                    border: 1px solid rgba(96, 165, 250, 0.25); 
                    border-radius: 12px; 
                    padding: 10px 14px; 
                    max-width: 80%;
                ">
                    {text}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

with st.sidebar:
    st.title("**JARVIS**")
    st.caption("Multi-Agent Personal Assistant powered by LangGraph")
    st.markdown("---")
    
    with st.expander("Todos", icon=":material/task:", expanded=True):
        st.write("**Active Tasks**")
        todos = load_json(TODO_FILE)
        if todos:
            for todo in todos:
                st.write(f"- {todo.get('task', '')}")
        else:
            st.info("No todos yet.")
            
    with st.expander("Calendar Events", icon=":material/calendar_today:", expanded=False):
        st.write("**Scheduled Events**")
        events = load_json(CALENDAR_FILE)
        if events:
            for event in events:
                st.write(f"**{event.get('title', 'Untitled')}**")
                st.caption(f"{event.get('date', '')} at {event.get('time', '')}")
        else:
            st.info("No events scheduled.")
            
    with st.expander("Email Drafts", icon=":material/email:", expanded=False):
        st.write("**Pending Mail**")
        emails = load_json(EMAIL_FILE)
        if emails:
            for draft in emails:
                st.write(f"**To:** {draft.get('recipient', 'Unknown')}")
                st.write(f"**Subject:** {draft.get('subject', 'No Subject')}")
                st.divider()
        else:
            st.info("No email drafts.")

    with st.expander("Spotify Playlists", icon=":material/music_note:", expanded=False):
        st.write("**Saved Music**")
        playlists = load_json(PLAYLIST_FILE)
        if playlists:
            for playlist in playlists:
                st.write(f"**{playlist.get('name', 'Unnamed')}** ({len(playlist.get('songs', []))} songs)")
        else:
            st.info("No playlists.")
            
    st.markdown("---")
    st.info(
        "**Want real email & calendar integration?** "
        "This app uses Google OAuth which requires test-user access. "
        "Send a mail to **dchoudhry999@gmail.com** "
        "and I'll manually add you as a test user!",
        icon=":material/info:"
    )

if not st.session_state.chat_history:
    st.markdown("# :material/rocket: JARVIS")
    st.caption("LangGraph-powered Personal AI Assistant")
    st.write("---")
    st.write("### Try asking:")
    
    col1, col2 = st.columns(2)
    s1 = col1.button("Add a todo: buy milk and eggs", icon=":material/task:", use_container_width=True)
    s2 = col2.button("Schedule team sync tomorrow at 10 AM", icon=":material/calendar_today:", use_container_width=True)
    s3 = col1.button("Draft an email to manager about updates", icon=":material/email:", use_container_width=True)
    s4 = col2.button("Create a playlist for study sessions", icon=":material/music_note:", use_container_width=True)
    
    prompt = None
    if s1:
        prompt = "Add a todo: buy milk and eggs"
    elif s2:
        prompt = "Schedule team sync tomorrow at 10 AM"
    elif s3:
        prompt = "Draft an email to manager about updates"
    elif s4:
        prompt = "Create a playlist for study sessions"
        
    user_input = st.chat_input("Talk to Jarvis...")
    if user_input:
        prompt = user_input
        
    if prompt:
        st.session_state.chat_history.append(("user", prompt))
        render_chat_message("user", prompt)
            
        response_text = ""
        try:
            with st.spinner("Thinking..."):
                result = graph.invoke(
                    {"messages": [HumanMessage(content=prompt)]},
                    config={"configurable": {"thread_id": st.session_state.thread_id}},
                )
                response_text = result["messages"][-1].content
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "rate limit" in error_msg.lower():
                response_text = "Groq API Rate Limit Reached: The tokens-per-day (TPD) limit for the LLM has been reached. Please try again in a few minutes!"
            else:
                response_text = f"Error invoking Jarvis: {error_msg}. Please check your connection or try again."
                
        words = response_text.split(" ")
        current_text = ""
        placeholder = st.empty()
        for word in words:
            current_text += word + " "
            placeholder.markdown(
                f"""
                <div style="display: flex; justify-content: flex-start; margin-bottom: 12px;">
                    <div style="
                        background-color: rgba(96, 165, 250, 0.1); 
                        border: 1px solid rgba(96, 165, 250, 0.25); 
                        border-radius: 12px; 
                        padding: 10px 14px; 
                        max-width: 80%;
                    ">
                        {current_text}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            time.sleep(0.03)
            
        st.session_state.chat_history.append(("assistant", response_text))
        st.rerun()

else:
    col_title, col_reset = st.columns([0.8, 0.2])
    with col_title:
        st.subheader("Chat with Jarvis")
    with col_reset:
        if st.button("Clear Chat", icon=":material/delete:", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.thread_id = str(uuid.uuid4())
            st.rerun()
            
    st.markdown("---")

    for role, message in st.session_state.chat_history:
        render_chat_message(role, message)

    user_input = st.chat_input("Talk to Jarvis...")
    if user_input:
        st.session_state.chat_history.append(("user", user_input))
        render_chat_message("user", user_input)
            
        response_text = ""
        try:
            with st.spinner("Thinking..."):
                result = graph.invoke(
                    {"messages": [HumanMessage(content=user_input)]},
                    config={"configurable": {"thread_id": st.session_state.thread_id}},
                )
                response_text = result["messages"][-1].content
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "rate limit" in error_msg.lower():
                response_text = "Groq API Rate Limit Reached: The tokens-per-day (TPD) limit for the LLM has been reached. Please try again in a few minutes!"
            else:
                response_text = f"Error invoking Jarvis: {error_msg}. Please check your connection or try again."
                
        words = response_text.split(" ")
        current_text = ""
        placeholder = st.empty()
        for word in words:
            current_text += word + " "
            placeholder.markdown(
                f"""
                <div style="display: flex; justify-content: flex-start; margin-bottom: 12px;">
                    <div style="
                        background-color: rgba(96, 165, 250, 0.1); 
                        border: 1px solid rgba(96, 165, 250, 0.25); 
                        border-radius: 12px; 
                        padding: 10px 14px; 
                        max-width: 80%;
                    ">
                        {current_text}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            time.sleep(0.03)
            
        st.session_state.chat_history.append(("assistant", response_text))
        st.rerun()