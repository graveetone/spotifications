import requests
import json
import os
from dotenv import load_dotenv

from proxy import get_spotify_proxy
from constants import TELEGRAM_CHAT_ID, PLAYLIST_UPDATED_IMAGE, SPOTIFICATIONS_PLAYLIST_LINK, SPOTIFICATIONS_PLAYLIST_ID
from clients.spotipy_client import SpotipyClient
from clients.telegram_client import TelegramClient

load_dotenv()

BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']


def get_updates(offset=None):
    resp = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates", params={"offset": offset})
    return resp.json()


def process_updates(spotipy_client: SpotipyClient, telegram_client: TelegramClient):
    songs_ids = []
    last_update_id = None

    updates = get_updates(last_update_id)
    if not updates.get("result"):
        print('No updates for Telegram bot')
    else:
        for update in updates['result']:
            query = update.get('callback_query')

            if query is None:
                print('Skipping updates with no callback query')
                continue

            print(f"Found update with callback query: {query['data']}")
            release_id = json.loads(query['data'])['song_id']

            songs = spotipy_client.get_album_songs(release_id)
            # skip songs that do not have favorite artists among all artists
            songs_ids.extend(songs)

            last_update_id = update['update_id'] + 1

        # clear updates
        get_updates(last_update_id)
        if not songs_ids:
            print("No songs to add to playlist")
            exit()

        songs_ids = set(songs_ids)
        spotipy_client.add_song_to_playlist(playlist_id=SPOTIFICATIONS_PLAYLIST_ID, songs_ids=songs_ids)
        telegram_client.send_message_with_image(
            text=f'Playlist was updated with {len(songs_ids)} new songs!',
            image_url=PLAYLIST_UPDATED_IMAGE,
            keyboard=telegram_client.compose_keyboard(
                dict(url=SPOTIFICATIONS_PLAYLIST_LINK, text="Check updates!")
            )
        )
    print('Updates processed successfully')


def main():
    spotipy_client = SpotipyClient(spotipy_client=get_spotify_proxy())
    telegram_client = TelegramClient(chat_id=TELEGRAM_CHAT_ID, token=os.environ['TELEGRAM_BOT_TOKEN'])

    process_updates(spotipy_client=spotipy_client, telegram_client=telegram_client)


if __name__ == "__main__":
    main()