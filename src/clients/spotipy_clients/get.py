from datetime import datetime
from typing import Optional
import os

DEFAULT_RELEASES_GROUPS = ",".join(("album", "single", "compilation", "appears_on"))
VARIOUS_ARTISTS = "Various Artists"


class GetSpotipyClient:
    def __init__(self, spotipy_client):
        self.client = spotipy_client

    def get_artist_releases(self, artist_id: str, newer_than: Optional[datetime]):
        """Get specific artist's releases newer than provided date"""
        artist_releases = []
        offset = 0
        while True:
            releases, limit, total = self._get_artist_releases(artist_id, newer_than, offset)
            artist_releases.extend(releases)

            if os.environ.get('SPOTIFICATIONS_DEBUG'):
                break

            if total <= offset:
                break

            offset += limit

        return artist_releases

    def get_artists_ids(self):
        """Get ids of artists that user follows """

        followed_artists_ids = []
        after = None
        while True:
            ids, has_next = self._get_artists_ids(after=after)
            followed_artists_ids.extend(ids)

            if os.environ.get('SPOTIFICATIONS_DEBUG'):
                break

            if not has_next:
                break

            after = ids[-1]

        return followed_artists_ids

    def get_album_songs(self, album_id: str):
        """Get songs from specific album"""
        album_songs = self.client.album_tracks(album_id)['items']
        return [song['uri'] for song in album_songs]

    def favorite_artist_song(self, song_id: str) -> bool:
        song = self.client.track(song_id)
        artists_ids = [artist['id'] for artist in song['artists']]

        return any(self.client.current_user_following_artists(artists_ids))

    def _get_artists_ids(self, after=None) -> tuple:
        artists = self.client.current_user_followed_artists(after=after)['artists']
        return [item['id'] for item in artists['items']], artists['next']

    def _get_artist_releases(self, artist_id: str, newer_than: Optional[datetime], offset=None,):
        if newer_than is None:
            newer_than = datetime.now()

        response = self.client.artist_albums(
            artist_id=artist_id, offset=offset, include_groups=DEFAULT_RELEASES_GROUPS,
        )

        return [
            self.parse_release_info(release)
            for release in response["items"]
            if not self.skip_release(release, newer_than)
        ], response['limit'], response['total']

    @staticmethod
    def _parse_release_date(date: str) -> datetime:
        if len(date) == 4:
            date += "-01-01"

        return datetime.fromisoformat(date)

    @staticmethod
    def skip_release(release, newer_than) -> bool:
        return any((
            VARIOUS_ARTISTS in {artists['name'] for artists in release['artists']},
            GetSpotipyClient._parse_release_date(release['release_date']) <= newer_than,
        ))

    @staticmethod
    def parse_release_info(release: dict):
        release_date = GetSpotipyClient._parse_release_date(release['release_date'])
        artists = ", ".join(artist['name'] for artist in release['artists'])
        release_info = {
            "name": release["name"],
            "release_date": release_date.strftime("%d.%m.%Y"),
            "artists": artists,
            "url": release["external_urls"]["spotify"],
            "song_id": release["uri"]
        }
        if images := release.get('images', []):
            release_info['cover_url'] = images[0]['url']

        return release_info
