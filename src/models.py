from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Release(BaseModel):
    artists: str
    release_date: str
    name: str
    url: str
    uri: str  # aka song_id
    cover_url: Optional[str] = None

    @classmethod
    def from_spotipy(cls, release: dict) -> "Release":
        release_date = cls.parse_release_date(release['release_date'])
        artists = ", ".join(artist['name'] for artist in release.get('artists', []))

        release_object = cls(
            name=release["name"],
            release_date=release_date.strftime("%d.%m.%Y"),
            artists=artists,
            url=release["external_urls"]["spotify"],
            uri=release["uri"]
        )

        if images := release.get('images', []):
            release_object.cover_url = images[0]['url']

        return release_object

    @staticmethod
    def parse_release_date(date: str) -> datetime:
        if len(date) == 4:
            date += "-01-01"

        return datetime.fromisoformat(date)

    def __hash__(self):
        return hash(self.uri)


class NotificationKeyboardButton(BaseModel):
    text: str
    url: Optional[str] = None
    callback_data: Optional[str] = None
