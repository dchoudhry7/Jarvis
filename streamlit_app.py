import streamlit as st
import json

from pathlib import Path

from langchain_core.messages import HumanMessage

from graph import graph


def load_json(file_path):

    path = Path(file_path)

    if not path.exists():
        return []

    try:
        with open(path, "r") as f:
            return json.load(f)

    except:
        return []

st.set_page_config(
    page_title="Jarvis AI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Jarvis")

st.caption(
    "Multi-Agent Personal Assistant powered by LangGraph"
)

todos = load_json(
    "data/todos.json"
)

emails = load_json(
    "data/email_drafts.json"
)

events = load_json(
    "data/calendar.json"
)

playlists = load_json(
    "data/playlists.json"
)


col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Agents",
        "6"
    )

with col2:
    st.metric(
        "Todos",
        len(todos)
    )

with col3:
    st.metric(
        "Emails",
        len(emails)
    )

with col4:
    st.metric(
        "Events",
        len(events)
    )

with col5:
    st.metric(
        "Playlists",
        len(playlists)
    )

chat_tab, todo_tab, email_tab, calendar_tab, spotify_tab = st.tabs(
    [
        "💬 Chat",
        "📝 Todos",
        "📧 Emails",
        "📅 Calendar",
        "🎵 Spotify"
    ]
)

with chat_tab:
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

        st.rerun()

with todo_tab:

    st.subheader("Todo List")

    TODO_FILE = Path(
        "data/todos.json"
    )

    if TODO_FILE.exists():

        with open(TODO_FILE, "r") as f:
            todos = json.load(f)

        if todos:

            for todo in todos:
                st.checkbox(
                    todo["task"],
                    value=False,
                    disabled=False
                )

        else:

            st.info(
                "No todos found."
            )

    else:

        st.warning(
            "todos.json not found."
        )

with email_tab:

    st.subheader("Email Drafts")

    EMAIL_FILE = Path(
        "data/email_drafts.json"
    )

    if EMAIL_FILE.exists():

        with open(
            EMAIL_FILE,
            "r"
        ) as f:

            drafts = json.load(f)

        if drafts:

            for draft in drafts:

                subject = draft.get(
                    "subject",
                    "No Subject"
                )

                recipient = draft.get(
                    "recipient",
                    "Unknown Recipient"
                )

                content = draft.get(
                    "content",
                    ""
                )

                with st.expander(
                    f"📧 {subject}"
                ):

                    st.write(
                        f"**Recipient:** {recipient}"
                    )

                    st.write(
                        f"**Draft ID:** {draft['id']}"
                    )

                    st.markdown("---")

                    st.write(content)

        else:

            st.info(
                "No email drafts found."
            )

    else:

        st.warning(
            "email_drafts.json not found."
        )

with calendar_tab:

    st.subheader("Calendar Events")

    CALENDAR_FILE = Path(
        "data/calendar.json"
    )

    if CALENDAR_FILE.exists():

        with open(
            CALENDAR_FILE,
            "r"
        ) as f:

            events = json.load(f)

        if events:

            calendar_data = []

            for event in events:

                calendar_data.append(
                    {
                        "ID": event["id"],
                        "Title": event["title"],
                        "Date": event["date"],
                        "Time": event["time"]
                    }
                )

            for event in events:
                with st.container():
                    st.markdown(
                        f"""
            ### 📅 {event['title']}

            **Date:** {event['date']}

            **Time:** {event['time']}
            """
                    )

                    st.markdown("---")

        else:

            st.info(
                "No calendar events found."
            )

    else:

        st.warning(
            "calendar.json not found."
        )

with spotify_tab:

    st.subheader("Spotify Playlists")

    PLAYLIST_FILE = Path(
        "data/playlists.json"
    )

    if PLAYLIST_FILE.exists():

        with open(
            PLAYLIST_FILE,
            "r"
        ) as f:

            playlists = json.load(f)

        if playlists:

            for playlist in playlists:

                playlist_name = playlist.get(
                    "name",
                    "Unnamed Playlist"
                )

                songs = playlist.get(
                    "songs",
                    []
                )

                with st.expander(
                    f"🎵 {playlist_name}"
                ):

                    if songs:

                        for song in songs:

                            st.write(
                                f"• {song}"
                            )

                    else:

                        st.info(
                            "No songs found."
                        )

        else:

            st.info(
                "No playlists found."
            )

    else:

        st.warning(
            "playlists.json not found."
        )