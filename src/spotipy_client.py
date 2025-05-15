from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
import os

DEFAULT_RELEASES_GROUPS = ",".join(("album", "single", "compilation", "appears_on"))


class BaseCrawler(ABC):
    @abstractmethod
    def get_artists_ids(self): ...

    @abstractmethod
    def get_artists_releases(self, artist_id: str, newer_than: Optional[datetime]): ...

class SpotifyCrawler(BaseCrawler):
    def __init__(self, spotipy_client):
        self.client = spotipy_client

    def get_artists_ids(self):
        followed_artists_ids = []
        after = None
        while True:
            response = self.client.current_user_followed_artists(
                after=after
            )['artists']

            followed_artists_ids.extend(
                item['id'] for item in response['items']
            )

            if os.environ.get('SPOTIFICATIONS_DEBUG') or response['next'] is None:
                break

            after = followed_artists_ids[-1]

        return followed_artists_ids

    def get_artists_releases(self, artist_id: str, newer_than: Optional[datetime]):
        if newer_than is None:
            newer_than = datetime.now()

        artists_albums = []
        offset = 0
        while True:
            response = self.client.artist_albums(
                artist_id=artist_id, offset=offset, include_groups=DEFAULT_RELEASES_GROUPS,
            )

            for release in response['items']:
                release_date = self._parse_release_date(release['release_date'])
                # pydantic model for release

                if release_date > newer_than:
                    artists = ", ".join(artist['name'] for artist in release['artists'])
                    release_info = {
                        "name": release["name"],
                        "release_date": release_date.strftime("%d.%m.%Y"),
                        "artists": artists,
                        "url": release["external_urls"]["spotify"],
                    }
                    if images := release.get('images', []):
                        release_info['cover_url'] = images[0]['url']

                    artists_albums.append(release_info)

            if os.environ.get('SPOTIFICATIONS_DEBUG') or response['total'] <= offset:
                break

            offset += response['limit']

        return artists_albums

    @staticmethod
    def _parse_release_date(date: str) -> datetime:
        if len(date) == 4:
            date += "-01-01"

        return datetime.fromisoformat(date)



    def refresh_token(self):
        print("Refreshing token")
        self.client.auth_manager.refresh_token = os.environ.get("SPOTIFY_REFRESH_TOKEN")
        token_info = self.client.auth_manager.refresh_access_token(
            self.client.auth_manager.refresh_token
        )
        self.client.token = token_info['access_token']
        print("Token was successfully refreshed")
