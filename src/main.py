import datetime
import os

from dotenv import load_dotenv

from proxy import get_spotify_proxy
from spotipy_client import SpotifyCrawler
from mock_spotipy_client import MockSpotifyCrawler
from telegram_notifier import send_image

load_dotenv()

NOTITICATION_PATTERN = """
ᯤ New release from {artists}!
[{release_date}]
"""

def update_last_crawling_date(last_crawling_date):
    with open(".last_crawling_date", "w") as file:
        file.write(str(last_crawling_date))

def get_last_crawling_date():
    with open(".last_crawling_date") as file:
        return datetime.datetime.fromisoformat(file.readline())

if __name__ == "__main__":
    sp = get_spotify_proxy()
    last_crawling_date = get_last_crawling_date()

    crawler = (
        MockSpotifyCrawler(spotipy_client=sp)
        if os.environ.get("USE_MOCK_CRAWLER") == "true"
        else SpotifyCrawler(spotipy_client=sp)
    )

    crawler.refresh_token()

    new_releases = []
    print("Retrieving artists ids")
    artists_ids = crawler.get_artists_ids()

    print(f"Crawling releases newer than {last_crawling_date}")

    for i, aid in enumerate(artists_ids, start=1):
        releases = crawler.get_artists_releases(artist_id=aid, newer_than=last_crawling_date)

        if releases:
            new_releases.extend(releases)
        print(f"Processed {i}/{len(artists_ids)}")

    update_last_crawling_date(datetime.datetime.now())

    if not new_releases:
        send_image(
            caption=f'No new releases from {last_crawling_date.strftime("%d.%m.%Y")}',
            image_url="https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D2NHuUzVqIFU&psig=AOvVaw0r9OqqtwemztU4Y-CqgIUB&ust=1747341520769000&source=images&cd=vfe&opi=89978449&ved=0CBAQjRxqFwoTCKDV7cboo40DFQAAAAAdAAAAABAE",
            button_link="https://open.spotify.com/playlist/1aXheOUOZAgiOfvEjCD31N?si=1e450a0460274895",
            button_caption="Check ListenToMe playlist!",
        )
        exit(0)

    for release in new_releases:
        send_image(
            caption=NOTITICATION_PATTERN.format(
                artists=release['artists'],
                release_date=release['release_date'],
            ),
            image_url=release['cover_url'],
            button_link=release['url'],
            button_caption=release['name'],
        )

