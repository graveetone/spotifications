import requests
import json
import os
from dotenv import load_dotenv

from proxy import get_spotify_proxy
from spotipy_client import SpotifyCrawler
from telegram_notifier import send_image

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
            songs_ids.extend(songs) # make it set to ensure unique releases only

            last_update_id = update['update_id'] + 1

        # clear updates
        get_updates(last_update_id)
        crawler.add_song_to_playlist(songs_ids=songs_ids)
        send_image(
            caption=f'Playlist was updated with {len(songs_ids)} new songs!',
            image_url="https://blog.happyfox.com/wp-content/uploads/2014/11/How-to-Rock-Customer-Engagement-like-Spotify.png",
            button_link="https://open.spotify.com/playlist/3vtxCgkU9wpiyppMvbWJow?si=fe201e9ebfd84316",
            button_caption="Check updates",
        )
    print('processed')

if __name__ == "__main__":
    sp = get_spotify_proxy()

    crawler = SpotifyCrawler(spotipy_client=sp)

    crawler.refresh_token()
    process_updates(crawler)
