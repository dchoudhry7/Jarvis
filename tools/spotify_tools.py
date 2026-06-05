import json
from pathlib import Path

from langchain_core.tools import tool


PLAYLIST_FILE = Path("data/playlists.json")


@tool
def add_song_to_playlist(
    playlist_name: str,
    song_name: str
):
    """
    Add a song to a playlist.
    """

    with open(PLAYLIST_FILE, "r") as f:
        playlists = json.load(f)

    playlist_found = False

    for playlist in playlists:

        if playlist["name"].lower() == playlist_name.lower():

            playlist["songs"].append(song_name)

            playlist_found = True
            break

    if not playlist_found:

        playlists.append(
            {
                "name": playlist_name,
                "songs": [song_name]
            }
        )

    with open(PLAYLIST_FILE, "w") as f:
        json.dump(playlists, f, indent=4)

    return (
        f"Added '{song_name}' "
        f"to playlist '{playlist_name}'."
    )

@tool
def show_playlists():
    """
    Show all playlists.
    """

    with open(PLAYLIST_FILE, "r") as f:
        playlists = json.load(f)

    if not playlists:
        return "No playlists found."

    result = []

    for playlist in playlists:

        songs = "\n".join(
            f"- {song}"
            for song in playlist["songs"]
        )

        result.append(
            f"""
Playlist: {playlist['name']}

Songs:
{songs}
"""
        )

    return "\n".join(result)

@tool
def remove_song_from_playlist(
    playlist_name: str,
    song_name: str
):
    """
    Remove a song from a playlist.
    """

    with open(PLAYLIST_FILE, "r") as f:
        playlists = json.load(f)

    for playlist in playlists:

        if playlist["name"].lower() == playlist_name.lower():

            if song_name in playlist["songs"]:

                playlist["songs"].remove(song_name)

                with open(PLAYLIST_FILE, "w") as f:
                    json.dump(playlists, f, indent=4)

                return (
                    f"Removed '{song_name}' "
                    f"from '{playlist_name}'."
                )

    return "Song or playlist not found."

@tool
def delete_playlist(
    playlist_name: str
):
    """
    Delete a playlist.
    """

    with open(PLAYLIST_FILE, "r") as f:
        playlists = json.load(f)

    new_playlists = [
        playlist
        for playlist in playlists
        if playlist["name"].lower()
        != playlist_name.lower()
    ]

    if len(new_playlists) == len(playlists):
        return "Playlist not found."

    with open(PLAYLIST_FILE, "w") as f:
        json.dump(new_playlists, f, indent=4)

    return (
        f"Playlist '{playlist_name}' deleted."
    )