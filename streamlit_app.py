import json
import uuid
import time
from pathlib import Path
import streamlit as st
import pandas as pd
from langchain_core.messages import HumanMessage
from graph import graph
from tools.todo_tools import add_todo
from tools.calendar_tools import create_event, delete_event, delete_all_events
from tools.email_tools import draft_email, delete_email_draft, delete_all_email_drafts, send_email, send_pending_email
from tools.spotify_tools import add_song_to_playlist, remove_song_from_playlist, delete_playlist
from tools.memory_tools import remember


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
    st.session_state.active_page = "Chat"
    reset_data_files()

def load_json(path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return []

def record_task_log(tool_name, args):
    agent_map = {
        "add_todo": "Todo Agent",
        "create_event": "Calendar Agent",
        "delete_event": "Calendar Agent",
        "delete_all_events": "Calendar Agent",
        "draft_email": "Email Agent",
        "delete_email_draft": "Email Agent",
        "delete_all_email_drafts": "Email Agent",
        "send_email": "Email Agent",
        "send_pending_email": "Email Agent",
        "add_song_to_playlist": "Spotify Agent",
        "remove_song_from_playlist": "Spotify Agent",
        "delete_playlist": "Spotify Agent",
        "remember": "Memory Agent"
    }
    if tool_name not in agent_map:
        return
    agent = agent_map[tool_name]
    if tool_name == "add_todo":
        desc = f"Added task: {args.get('task', '')}"
    elif tool_name == "create_event":
        desc = f"Created event: {args.get('title', '')} on {args.get('date', '')} at {args.get('time', '')}"
    elif tool_name == "delete_event":
        desc = f"Deleted event ID {args.get('event_id', '')}"
    elif tool_name == "delete_all_events":
        desc = "Deleted all events"
    elif tool_name == "draft_email":
        desc = f"Drafted email to {args.get('recipient', '')} - '{args.get('subject', '')}'"
    elif tool_name == "delete_email_draft":
        desc = f"Deleted email draft ID {args.get('draft_id', '')}"
    elif tool_name == "delete_all_email_drafts":
        desc = "Deleted all email drafts"
    elif tool_name == "send_email":
        desc = f"Sent email to {args.get('recipient', '')} - '{args.get('subject', '')}'"
    elif tool_name == "send_pending_email":
        desc = "Sent pending email"
    elif tool_name == "add_song_to_playlist":
        desc = f"Added song '{args.get('song_name', '')}' to playlist '{args.get('playlist_name', '')}'"
    elif tool_name == "remove_song_from_playlist":
        desc = f"Removed song '{args.get('song_name', '')}' from playlist '{args.get('playlist_name', '')}'"
    elif tool_name == "delete_playlist":
        desc = f"Deleted playlist '{args.get('playlist_name', '')}'"
    elif tool_name == "remember":
        desc = f"Stored memory: {args.get('memory', '')}"
    else:
        desc = f"Executed {tool_name}"
    log_file = Path("data/ai_tasks_log.json")
    log_file.parent.mkdir(exist_ok=True)
    logs = []
    if log_file.exists():
        try:
            with open(log_file, "r") as f:
                logs = json.load(f)
        except Exception:
            pass
    from datetime import datetime
    logs.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "agent": agent,
        "task": desc
    })
    with open(log_file, "w") as f:
        json.dump(logs, f, indent=4)

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

    if st.button(":material/chat_bubble: Chat", use_container_width=True):
        st.session_state.active_page = "Chat"
        st.rerun()

    st.markdown("---")

    with st.expander("Todos", icon=":material/task:", expanded=True):
        st.write("**Active Tasks**")
        todos = load_json(TODO_FILE)
        if todos:
            for todo in todos:
                st.write(f"- {todo.get('task', '')}")
        else:
            st.info("No todos yet.")
        if st.button("View & Manage Todos", key="nav_todos", use_container_width=True):
            st.session_state.active_page = "Todo Agent"
            st.rerun()
            
    with st.expander("Calendar Events", icon=":material/calendar_today:", expanded=False):
        st.write("**Scheduled Events**")
        events = load_json(CALENDAR_FILE)
        if events:
            for event in events:
                st.write(f"**{event.get('title', 'Untitled')}**")
                st.caption(f"{event.get('date', '')} at {event.get('time', '')}")
        else:
            st.info("No events scheduled.")
        if st.button("View & Manage Events", key="nav_calendar", use_container_width=True):
            st.session_state.active_page = "Calendar Agent"
            st.rerun()
            
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
        if st.button("View & Manage Drafts", key="nav_emails", use_container_width=True):
            st.session_state.active_page = "Email Agent"
            st.rerun()

    with st.expander("Spotify Playlists", icon=":material/music_note:", expanded=False):
        st.write("**Saved Music**")
        playlists = load_json(PLAYLIST_FILE)
        if playlists:
            for playlist in playlists:
                st.write(f"**{playlist.get('name', 'Unnamed')}** ({len(playlist.get('songs', []))} songs)")
        else:
            st.info("No playlists.")
        if st.button("View & Manage Playlists", key="nav_spotify", use_container_width=True):
            st.session_state.active_page = "Spotify Agent"
            st.rerun()

    with st.expander("Stored Memories", icon=":material/psychology:", expanded=False):
        st.write("**Recall Info**")
        memories = load_json(MEMORY_FILE)
        if memories:
            for memory in memories:
                st.write(f"- {memory.get('memory', '')}")
        else:
            st.info("No memories stored.")
        if st.button("View & Manage Memories", key="nav_memories", use_container_width=True):
            st.session_state.active_page = "Memory Agent"
            st.rerun()

    st.markdown("---")

    st.info(
        "**Want real email & calendar integration?** "
        "This app uses Google OAuth which requires test-user access. "
        "Send a mail to **dchoudhry999@gmail.com** "
        "and I'll manually add you as a test user!",
        icon=":material/info:"
    )

if st.session_state.active_page == "Chat":
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
                    for msg in result["messages"]:
                        if hasattr(msg, "tool_calls") and msg.tool_calls:
                            for tc in msg.tool_calls:
                                record_task_log(tc.get("name"), tc.get("args", {}))
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
                    for msg in result["messages"]:
                        if hasattr(msg, "tool_calls") and msg.tool_calls:
                            for tc in msg.tool_calls:
                                record_task_log(tc.get("name"), tc.get("args", {}))
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

elif st.session_state.active_page == "Todo Agent":
    st.subheader("Todo Agent Page")
    todos = load_json(TODO_FILE)
    if todos:
        df = pd.DataFrame(todos)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No todos found.")
    
    st.write("---")
    st.write("### Add Todo Task")
    new_task = st.text_input("Task Description", key="new_todo_task_input")
    if st.button("Add Todo", key="add_todo_btn"):
        if new_task:
            res = add_todo.invoke({"task": new_task})
            record_task_log("add_todo", {"task": new_task})
            st.success(res)
            st.rerun()

elif st.session_state.active_page == "Calendar Agent":
    st.subheader("Calendar Agent Page")
    events = load_json(CALENDAR_FILE)
    if events:
        df = pd.DataFrame(events)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No events found.")
    
    st.write("---")
    st.write("### Create Event")
    title = st.text_input("Title", key="cal_title_input")
    c_date = st.text_input("Date (e.g. YYYY-MM-DD)", key="cal_date_input")
    c_time = st.text_input("Time (e.g. HH:MM)", key="cal_time_input")
    if st.button("Create Event", key="create_event_btn"):
        if title and c_date and c_time:
            res = create_event.invoke({"title": title, "date": c_date, "time": c_time})
            record_task_log("create_event", {"title": title, "date": c_date, "time": c_time})
            st.success(res)
            st.rerun()
            
    st.write("---")
    st.write("### Delete Event")
    del_id = st.number_input("Event ID to Delete", min_value=1, step=1, key="cal_del_id_input")
    if st.button("Delete Event", key="delete_event_btn"):
        res = delete_event.invoke({"event_id": int(del_id)})
        record_task_log("delete_event", {"event_id": int(del_id)})
        st.success(res)
        st.rerun()
        
    st.write("---")
    if st.button("Delete All Events", key="delete_all_events_btn"):
        res = delete_all_events.invoke({})
        record_task_log("delete_all_events", {})
        st.success(res)
        st.rerun()

elif st.session_state.active_page == "Email Agent":
    st.subheader("Email Agent Page")
    drafts = load_json(EMAIL_FILE)
    if drafts:
        df = pd.DataFrame(drafts)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No email drafts found.")
        
    st.write("---")
    st.write("### Compose/Draft Email")
    recipient = st.text_input("Recipient Email", key="email_rec_input")
    subject = st.text_input("Subject", key="email_sub_input")
    purpose = st.text_area("Purpose", key="email_pur_input")
    if st.button("Draft Email", key="draft_email_btn"):
        if recipient and subject and purpose:
            res = draft_email.invoke({"recipient": recipient, "subject": subject, "purpose": purpose})
            record_task_log("draft_email", {"recipient": recipient, "subject": subject, "purpose": purpose})
            st.success(res)
            st.rerun()
            
    st.write("---")
    st.write("### Send Custom Email")
    s_recipient = st.text_input("Recipient Email", key="send_email_rec_input")
    s_subject = st.text_input("Subject", key="send_email_sub_input")
    s_body = st.text_area("Body", key="send_email_body_input")
    if st.button("Send Email", key="send_email_btn"):
        if s_recipient and s_subject and s_body:
            res = send_email.invoke({"recipient": s_recipient, "subject": s_subject, "body": s_body})
            record_task_log("send_email", {"recipient": s_recipient, "subject": s_subject, "body": s_body})
            st.success(res)
            st.rerun()
            
    st.write("---")
    st.write("### Manage Drafts & Pending Emails")
    del_draft_id = st.number_input("Draft ID to Delete", min_value=1, step=1, key="email_del_id_input")
    if st.button("Delete Draft", key="delete_draft_btn"):
        res = delete_email_draft.invoke({"draft_id": int(del_draft_id)})
        record_task_log("delete_email_draft", {"draft_id": int(del_draft_id)})
        st.success(res)
        st.rerun()
        
    if st.button("Send Pending Email", key="send_pending_email_btn"):
        res = send_pending_email.invoke({})
        record_task_log("send_pending_email", {})
        st.success(res)
        st.rerun()
        
    if st.button("Delete All Email Drafts", key="delete_all_drafts_btn"):
        res = delete_all_email_drafts.invoke({})
        record_task_log("delete_all_email_drafts", {})
        st.success(res)
        st.rerun()

elif st.session_state.active_page == "Spotify Agent":
    st.subheader("Spotify Agent Page")
    playlists = load_json(PLAYLIST_FILE)
    if playlists:
        flat_data = []
        for p in playlists:
            name = p.get("name", "")
            songs = p.get("songs", [])
            if songs:
                for song in songs:
                    flat_data.append({"Playlist Name": name, "Song": song})
            else:
                flat_data.append({"Playlist Name": name, "Song": "(Empty)"})
        df = pd.DataFrame(flat_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No playlists found.")
        
    st.write("---")
    st.write("### Add Song to Playlist")
    pl_name = st.text_input("Playlist Name", key="spot_pl_add_input")
    song_name = st.text_input("Song Name", key="spot_song_add_input")
    if st.button("Add Song", key="add_song_btn"):
        if pl_name and song_name:
            res = add_song_to_playlist.invoke({"playlist_name": pl_name, "song_name": song_name})
            record_task_log("add_song_to_playlist", {"playlist_name": pl_name, "song_name": song_name})
            st.success(res)
            st.rerun()
            
    st.write("---")
    st.write("### Remove Song from Playlist")
    pl_rem_name = st.text_input("Playlist Name", key="spot_pl_rem_input")
    song_rem_name = st.text_input("Song Name", key="spot_song_rem_input")
    if st.button("Remove Song", key="remove_song_btn"):
        if pl_rem_name and song_rem_name:
            res = remove_song_from_playlist.invoke({"playlist_name": pl_rem_name, "song_name": song_rem_name})
            record_task_log("remove_song_from_playlist", {"playlist_name": pl_rem_name, "song_name": song_rem_name})
            st.success(res)
            st.rerun()
            
    st.write("---")
    st.write("### Delete Playlist")
    pl_del_name = st.text_input("Playlist Name", key="spot_pl_del_input")
    if st.button("Delete Playlist", key="delete_playlist_btn"):
        if pl_del_name:
            res = delete_playlist.invoke({"playlist_name": pl_del_name})
            record_task_log("delete_playlist", {"playlist_name": pl_del_name})
            st.success(res)
            st.rerun()

elif st.session_state.active_page == "Memory Agent":
    st.subheader("Memory Agent Page")
    memories = load_json(MEMORY_FILE)
    if memories:
        df = pd.DataFrame(memories)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No memories stored.")
        
    st.write("---")
    st.write("### Store Memory")
    memory_text = st.text_area("Memory Content", key="mem_content_input")
    if st.button("Remember", key="remember_btn"):
        if memory_text:
            res = remember.invoke({"memory": memory_text})
            record_task_log("remember", {"memory": memory_text})
            st.success(res)
            st.rerun()