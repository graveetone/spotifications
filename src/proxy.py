import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth


def get_auth_manager():
    return SpotifyOAuth(
        client_id=os.environ.get("SPOTIFY_CLIENT_ID"),
        client_secret=os.environ.get("SPOTIFY_CLIENT_SECRET"),
        redirect_uri="https://google.com",
        scope="playlist-modify-public user-follow-read",
        open_browser=False,
        cache_path=None,
    )


def get_spotify_proxy():
    oauth = get_auth_manager()
    refresh_token = os.environ["SPOTIFY_REFRESH_TOKEN"]
    token_info = oauth.refresh_access_token(refresh_token)

    return spotipy.Spotify(auth=token_info["access_token"])
