import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

def get_auth_manager():
    return SpotifyOAuth(
        client_id=os.environ.get("SPOTIFY_CLIENT_ID"),
        client_secret=os.environ.get("SPOTIFY_CLIENT_SECRET"),
        redirect_uri="https://google.com",
        scope="playlist-modify-public user-follow-read",
        open_browser=False
    )


def get_spotify_proxy():
    return spotipy.Spotify(
        auth_manager=get_auth_manager()
    )
