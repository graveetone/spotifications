class PostSpotipyClient:
    def __init__(self, spotipy_client):
        self.client = spotipy_client

    def add_song_to_playlist(self, playlist_id: str, songs_ids: list):
        self.client.playlist_add_items(playlist_id, songs_ids)
