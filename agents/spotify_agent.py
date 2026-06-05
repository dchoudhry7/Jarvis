from langchain_core.messages import SystemMessage

from config import llm

from tools.spotify_tools import (
    add_song_to_playlist,
    show_playlists,
    remove_song_from_playlist,
    delete_playlist
)


spotify_llm = llm.bind_tools(
    [
        add_song_to_playlist,
        show_playlists,
        remove_song_from_playlist,
        delete_playlist
    ]
)


def spotify_agent(state):

    print("spotify_agent called")

    messages = [
        SystemMessage(
            content="""
            You are a Spotify Agent.

            Responsibilities:
            - Add songs to playlists
            - Show playlists
            - Remove songs from playlists
            - Delete playlists

            Always use tools when playlist operations
            are requested.

            Never invent playlist data.
            """
        )
    ] + state["messages"]

    response = spotify_llm.invoke(
        messages
    )

    return {
        "messages": [response]
    }