import requests
import json
import os
from dotenv import load_dotenv

from proxy import get_spotify_proxy
from constants import TELEGRAM_CHAT_ID, PLAYLIST_UPDATED_IMAGE, SPOTIFICATIONS_PLAYLIST_LINK, SPOTIFICATIONS_PLAYLIST_ID
from clients.spotipy_client import SpotipyClient
from clients.telegram_client import TelegramClient
from models import NotificationKeyboardButton
from loguru import logger


load_dotenv()

BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']


def get_updates(offset=None):
    resp = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates", params={"offset": offset})
    return resp.json()


def process_updates(spotipy_client: SpotipyClient, telegram_client: TelegramClient):
    songs_ids = set()
    episodes_ids = set()
    last_update_id = None

    updates = get_updates(last_update_id)
    if not updates.get("result"):
        logger.info('No updates for Telegram bot')
    else:
        for update in updates['result']:
            query = update.get('callback_query')
            last_update_id = update['update_id'] + 1

            if query is None:
                logger.warning('Skipping updates with no callback query')
                continue

            logger.info(f"Found update with callback query: {query['data']}")
            release_id = json.loads(query['data'])['song_id']

            if "episode" in release_id:
                episodes_ids.add(release_id)
            else:
                songs = spotipy_client.get.get_album_songs(release_id)
                songs_ids.update(songs)

        # clear updates
        get_updates(last_update_id)

        songs_ids = {
            song for song in songs_ids
            if spotipy_client.get.favorite_artist_song(song)
        }
        songs_ids.update(episodes_ids)

        if not songs_ids:
            logger.info("No songs or episodes to add to playlist")
            exit()

        spotipy_client.post.add_songs_to_playlist(playlist_id=SPOTIFICATIONS_PLAYLIST_ID, songs_ids=songs_ids)
        telegram_client.send_message_with_image(
            text=f'Playlist was updated with {len(songs_ids)} new item(s)!',
            image_url=PLAYLIST_UPDATED_IMAGE,
            keyboard=telegram_client.compose_keyboard(
                NotificationKeyboardButton(url=SPOTIFICATIONS_PLAYLIST_LINK, text="Check updates!").model_dump()
            )
        )
    logger.success('Updates processed successfully')


def main():
    spotipy_client = SpotipyClient(spotipy_client=get_spotify_proxy())
    telegram_client = TelegramClient(chat_id=TELEGRAM_CHAT_ID, token=os.environ['TELEGRAM_BOT_TOKEN'])

    process_updates(spotipy_client=spotipy_client, telegram_client=telegram_client)


if __name__ == "__main__":
    main()