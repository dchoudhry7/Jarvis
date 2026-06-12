from langchain_core.messages import SystemMessage
from config import llm
from tools.spotify_tools import (
    add_song_to_playlist,
    show_playlists,
    remove_song_from_playlist,
    delete_playlist,
)

spotify_llm = llm.bind_tools([
    add_song_to_playlist,
    show_playlists,
    remove_song_from_playlist,
    delete_playlist,
])

SYSTEM_PROMPT = """You are the Spotify Agent 🎵 of Jarvis.

AVAILABLE TOOLS:
1. add_song_to_playlist — Add a song to a playlist (creates playlist if new).
2. show_playlists — Show all playlists and their songs.
3. remove_song_from_playlist — Remove a song from a playlist.
4. delete_playlist — Delete an entire playlist.

RULES:
- Always use tools for playlist operations — never invent data.
- After adding a song, confirm: "🎵 Added '<song>' to '<playlist>'!"
- After removing, confirm: "✅ Removed '<song>' from '<playlist>'."
- Use emojis naturally (🎵, 🎶, ✅, 🎧).
- Be concise and friendly.
"""

def spotify_agent(state):
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = spotify_llm.invoke(messages)
    return {"messages": [response]}
