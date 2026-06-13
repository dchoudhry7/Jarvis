"""Spotify tools — JSON-only storage for playlists."""

import json
from pathlib import Path

from langchain_core.tools import tool



from langchain_core.runnables import RunnableConfig

def get_playlist_file(config: RunnableConfig = None) -> Path:
    thread_id = None
    if config:
        thread_id = config.get("configurable", {}).get("thread_id")
    if thread_id:
        return Path("data") / thread_id / "playlists.json"
    return Path("data/playlists.json")


def load_playlists(config: RunnableConfig = None):
    playlist_file = get_playlist_file(config)
    if not playlist_file.exists():
        return []
    with open(playlist_file, "r") as f:
        return json.load(f)


def save_playlists(playlists, config: RunnableConfig = None):
    playlist_file = get_playlist_file(config)
    playlist_file.parent.mkdir(exist_ok=True, parents=True)
    with open(playlist_file, "w") as f:
        json.dump(playlists, f, indent=4)



@tool
def add_song_to_playlist(playlist_name: str, song_name: str, config: RunnableConfig = None):
    """Add a song to a playlist."""

    playlists = load_playlists(config)

    playlist_found = False
    for playlist in playlists:
        if playlist["name"].lower() == playlist_name.lower():
            playlist["songs"].append(song_name)
            playlist_found = True
            break

    if not playlist_found:
        playlists.append({
            "name": playlist_name,
            "songs": [song_name],
        })

    save_playlists(playlists, config)

    return f"Added '{song_name}' to playlist '{playlist_name}'."


@tool
def show_playlists(config: RunnableConfig = None):
    """Show all playlists."""

    playlists = load_playlists(config)

    if not playlists:
        return "No playlists found."

    result = []
    for playlist in playlists:
        songs = "\n".join(f"- {song}" for song in playlist["songs"])
        result.append(f"Playlist: {playlist['name']}\nSongs:\n{songs}")

    return "\n\n".join(result)


@tool
def remove_song_from_playlist(playlist_name: str, song_name: str, config: RunnableConfig = None):
    """Remove a song from a playlist."""

    playlists = load_playlists(config)

    for playlist in playlists:
        if playlist["name"].lower() == playlist_name.lower():
            if song_name in playlist["songs"]:
                playlist["songs"].remove(song_name)
                save_playlists(playlists, config)
                return f"Removed '{song_name}' from '{playlist_name}'."

    return "Song or playlist not found."


@tool
def delete_playlist(playlist_name: str, config: RunnableConfig = None):
    """Delete a playlist."""

    playlists = load_playlists(config)

    new_playlists = [
        p for p in playlists
        if p["name"].lower() != playlist_name.lower()
    ]

    if len(new_playlists) == len(playlists):
        return "Playlist not found."

    save_playlists(new_playlists, config)

    return f"Playlist '{playlist_name}' deleted."

