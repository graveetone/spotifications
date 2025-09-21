from telegram import Update
from telegram.ext import Application, CallbackQueryHandler, ContextTypes
import json
from proxy import get_spotify_proxy
from clients.spotipy_client import SpotipyClient
import os
from dotenv import load_dotenv
from updater import add_release_to_playlist
load_dotenv()
spotipy_client = SpotipyClient(spotipy_client=get_spotify_proxy())


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    release_id = json.loads(query.data).get("song_id")
    if release_id is not None:
        add_release_to_playlist(release_id, spotipy_client)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"Added {release_id}"
        )


def main():
    app = Application.builder().token(os.environ['TELEGRAM_BOT_TOKEN'],).build()

    app.add_handler(CallbackQueryHandler(button_handler))
    print("Start pooler")
    app.run_polling()


if __name__ == "__main__":
    main()
