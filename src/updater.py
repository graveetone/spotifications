from fastapi import FastAPI, Request

import json
from src.proxy import get_spotify_proxy
from src.clients.spotipy_client import SpotipyClient
import os
from dotenv import load_dotenv
from src.models import NotificationKeyboardButton
from src.clients.telegram_client import TelegramClient
from src.constants import SPOTIFICATIONS_PLAYLIST_LINK, SPOTIFICATIONS_PLAYLIST_ID
from loguru import logger


load_dotenv()
spotipy_client = SpotipyClient(spotipy_client=get_spotify_proxy())
telegram_client = TelegramClient(chat_id=None, token=os.environ['TELEGRAM_BOT_TOKEN'])
app = FastAPI()


def add_release_to_playlist(release_id: str, spotipy_client: SpotipyClient):
    songs_to_add_ids = []

    if "episode" in release_id:
        songs_to_add_ids.append(release_id)
    else:
        songs_ids = spotipy_client.get.get_album_songs(release_id)
        songs_to_add_ids.extend(songs_ids)

        songs_to_add_ids = [
            song for song in songs_to_add_ids
            if spotipy_client.get.favorite_artist_song(song)
        ]

    if not songs_to_add_ids:
        logger.info("No songs or episodes to add to playlist")
        return

    spotipy_client.post.add_songs_to_playlist(
        playlist_id=SPOTIFICATIONS_PLAYLIST_ID,
        songs_ids=songs_to_add_ids,
    )
    logger.info(f"Added to playlist: {songs_to_add_ids}")


@app.post("/api/webhook")
async def telegram_webhook(request: Request):
    webhook_response = await request.json()
    query = webhook_response['callback_query']

    release_uri = json.loads(query['data']).get("release_uri")
    if release_uri is not None:
        add_release_to_playlist(release_uri, spotipy_client)
        release = spotipy_client.get.get_release(release_uri=release_uri)

        telegram_client.chat_id = query['message']['chat']['id']
        telegram_client.send_message_with_image(
            image_url=release.cover_url,
            text=f"🎧 Added to playlist!\n\n🎶<b>{release.name}</b> by <b>{release.artists}</b>",
            keyboard=telegram_client.compose_keyboard(
                NotificationKeyboardButton(
                    url=SPOTIFICATIONS_PLAYLIST_LINK,
                    text="Check ListenToMe playlist!",
                ).model_dump()
            )
        )
        return {"ok": True}
