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
<a href='{url}'>{name}</a> [{release_date}]
"""

if __name__ == "__main__":
    sp = get_spotify_proxy()
    last_crawling_date = datetime.datetime.fromisoformat("2025-05-01")

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
        # breakpoint()
        if releases:
            new_releases.extend(releases)
        print(f"Processed {i}/{len(artists_ids)}")

    # from pprint import pprint
    # pprint(new_releases)
    # breakpoint()
    for release in new_releases:
        send_image(
            caption=NOTITICATION_PATTERN.format(
                artists=release['artists'],
                name=release['name'],
                release_date=release['release_date'],
                url=release['url'],
            ),
            image_url=release['cover_url'],
        )

