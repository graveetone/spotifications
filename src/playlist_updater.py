import requests
import json
import os
from dotenv import load_dotenv

from mock_spotipy_client import MockSpotifyCrawler
from proxy import get_spotify_proxy
from spotipy_client import SpotifyCrawler

load_dotenv()


BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
def get_updates(offset=None):
    resp = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates", params={"offset": offset})
    return resp.json()

def process_updates(crawler):
    songs_ids = []
    last_update_id = None

    updates = get_updates(last_update_id)
    if not updates.get("result"):
        print('no updates')
    else:
        for update in updates['result']:
            query = update.get('callback_query')

            if query is None:
                print('no query')
                continue

            print(query['data'])
            release_id = json.loads(query['data'])['song_id']

            songs = crawler.get_album_songs(release_id)
            songs_ids.extend(songs)

            last_update_id = update['update_id'] + 1

        # clear updates
        get_updates(last_update_id)
        crawler.add_song_to_playlist(songs_ids=songs_ids)
    print('processed')

if __name__ == "__main__":
    sp = get_spotify_proxy()

    crawler = (
        MockSpotifyCrawler(spotipy_client=sp)
        if os.environ.get("USE_MOCK_CRAWLER") == "true"
        else SpotifyCrawler(spotipy_client=sp)
    )

    crawler.refresh_token()
    process_updates(crawler)
