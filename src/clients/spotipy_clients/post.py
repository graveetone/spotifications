from loguru import logger


class PostSpotipyClient:
    def __init__(self, spotipy_client):
        self.client = spotipy_client

    def add_songs_to_playlist(self, playlist_id: str, songs_ids: list):
        self.client.playlist_add_items(playlist_id, songs_ids)
        logger.debug(f"Add songs {songs_ids} to playlist {playlist_id}")

    def delete_track(self, playlist_id: str, track_id: str):
        self.client.playlist_remove_all_occurrences_of_items(
            playlist_id=playlist_id,
            items=[track_id]
        )
        logger.debug(f"Deleted track {track_id}")
