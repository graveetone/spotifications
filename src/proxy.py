import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials


# def get_spotify_proxy1():
#     auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
#     return spotipy.Spotify(auth_manager=auth_manager)

def get_auth_manager():
    return SpotifyOAuth(
        client_id=os.environ.get("SPOTIFY_CLIENT_ID"),
        client_secret=os.environ.get("SPOTIFY_CLIENT_SECRET"),
        redirect_uri="https://google.com",
        scope="user-follow-read"
    )


def get_spotify_proxy():
    return spotipy.Spotify(
        auth_manager=get_auth_manager()
    )
