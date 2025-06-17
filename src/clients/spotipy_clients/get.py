from datetime import datetime
from typing import Optional, List, Tuple
from pathlib import Path
import os
import sys

sys.path.append(str(Path(__file__).resolve().parents[3]))

from src.models import Release

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
                artist_releases = artist_releases[0:1]
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
                followed_artists_ids = followed_artists_ids[0:1]
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

    def _get_artist_releases(
            self, artist_id: str, newer_than: Optional[datetime], offset=None
    ) -> Tuple[List[Release], str, str]:
        if newer_than is None:
            newer_than = datetime.now()

        response = self.client.artist_albums(
            artist_id=artist_id, offset=offset, include_groups=DEFAULT_RELEASES_GROUPS,
        )

        return [
            Release.from_spotipy(release)
            for release in response["items"]
            if not self.skip_release(release, newer_than)
        ], response['limit'], response['total']

    @staticmethod
    def skip_release(release, newer_than) -> bool:
        return any((
            VARIOUS_ARTISTS in {artists['name'] for artists in release['artists']},
            Release.parse_release_date(release['release_date']) <= newer_than,
        ))
