import json
from spotipy_client import BaseCrawler
from datetime import datetime
from typing import Optional


class MockSpotifyCrawler(BaseCrawler):
    def __init__(self, spotipy_client):
        self.client = spotipy_client

    def get_artists_ids(self):
        return ["5tGG1slV9pkcydU5eQSIvm"]

    def get_artists_releases(self, artist_id: str, newer_than: Optional[datetime]):
        artists_albums = []
        response = {}
        try:
            with open(f"{artist_id}.json") as f:
                response = json.load(fp=f)
        except FileNotFoundError:
            print(f"Response for {artist_id} was not mocked yet!")

        for release in response['items']:
            artists = ", ".join(artist['name'] for artist in release['artists'])
            artists_albums.append(
                f"{artists} - {release['name']}"
            )

        return artists_albums



    @staticmethod
    def _parse_release_date(date: str) -> datetime:
        if len(date) == 4:
            date += "-01-01"

        return datetime.fromisoformat(date)


    def refresh_token(self):
        print("[MOCK] Refreshing token")
        # self.client.auth_manager.refresh_token = os.environ.get("SPOTIFY_REFRESH_TOKEN")
        # token_info = self.client.auth_manager.refresh_access_token(
        #     self.client.auth_manager.refresh_token
        # )
        # self.client.token = token_info['access_token']
        # print("Token was successfully refreshed")