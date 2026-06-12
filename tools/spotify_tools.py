"""Spotify tools — JSON-only storage for playlists."""

import json
from pathlib import Path

from langchain_core.tools import tool



PLAYLIST_FILE = Path("data/playlists.json")


def load_playlists():
    if not PLAYLIST_FILE.exists():
        return []
    with open(PLAYLIST_FILE, "r") as f:
        return json.load(f)


def save_playlists(playlists):
    PLAYLIST_FILE.parent.mkdir(exist_ok=True)
    with open(PLAYLIST_FILE, "w") as f:
        json.dump(playlists, f, indent=4)



@tool
def add_song_to_playlist(playlist_name: str, song_name: str):
    """Add a song to a playlist."""

    playlists = load_playlists()

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

    save_playlists(playlists)

    return f"Added '{song_name}' to playlist '{playlist_name}'."


@tool
def show_playlists():
    """Show all playlists."""

    playlists = load_playlists()

    if not playlists:
        return "No playlists found."

    result = []
    for playlist in playlists:
        songs = "\n".join(f"- {song}" for song in playlist["songs"])
        result.append(f"Playlist: {playlist['name']}\nSongs:\n{songs}")

    return "\n\n".join(result)


@tool
def remove_song_from_playlist(playlist_name: str, song_name: str):
    """Remove a song from a playlist."""

    playlists = load_playlists()

    for playlist in playlists:
        if playlist["name"].lower() == playlist_name.lower():
            if song_name in playlist["songs"]:
                playlist["songs"].remove(song_name)
                save_playlists(playlists)
                return f"Removed '{song_name}' from '{playlist_name}'."

    return "Song or playlist not found."


@tool
def delete_playlist(playlist_name: str):
    """Delete a playlist."""

    playlists = load_playlists()

    new_playlists = [
        p for p in playlists
        if p["name"].lower() != playlist_name.lower()
    ]

    if len(new_playlists) == len(playlists):
        return "Playlist not found."

    save_playlists(new_playlists)

    return f"Playlist '{playlist_name}' deleted."
