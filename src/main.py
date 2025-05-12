import datetime
from dotenv import load_dotenv

from proxy import get_spotify_proxy
from spotipy_client import SpotifyCrawler

load_dotenv()

if __name__ == "__main__":
    sp = get_spotify_proxy()
    last_crawling_date = datetime.datetime.fromisoformat("2025-05-01")
    crawler = SpotifyCrawler(spotipy_client=sp)
    crawler.refresh_token()

    new_releases = []
    print("Retrieving artists ids")
    artists_ids = crawler.get_artists_ids()

    print(f"Crawling releases newer than {last_crawling_date}")

    for i, aid in enumerate(artists_ids):
        new_releases.append(crawler.get_artists_releases(artist_id=aid, newer_than=last_crawling_date))
        print(f"Processed {i}/{len(artists_ids)}")

    from pprint import pprint
    pprint(new_releases)
