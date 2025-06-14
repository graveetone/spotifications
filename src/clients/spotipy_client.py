from datetime import datetime
from typing import Optional
from .spotipy_clients import AuthSpotipyClient, GetSpotipyClient, PostSpotipyClient

class SpotipyClient:
    def __init__(self, spotipy_client):
        self.client = spotipy_client

        self.auth = AuthSpotipyClient(self.client)
        self.get = GetSpotipyClient(self.client)
        self.post = PostSpotipyClient(self.client)

        self.refresh_token()

    def refresh_token(self):
        return self.auth.refresh_token()

    def get_artists_ids(self):
        return self.get.get_artists_ids()

    def get_artist_releases(self, artist_id: str, newer_than: Optional[datetime]):
        return self.get.get_artist_releases(artist_id, newer_than)

    def get_album_songs(self, album_id: str):
        return self.get.get_album_songs(album_id)

    def add_song_to_playlist(self, playlist_id: str, songs_ids: list):
        self.post.add_song_to_playlist(playlist_id, songs_ids)

