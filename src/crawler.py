import datetime
import os
import json
from dotenv import load_dotenv

from proxy import get_spotify_proxy
from clients.spotipy_client import SpotipyClient
from clients.telegram_client import TelegramClient
from constants import NOTITICATION_PATTERN, NO_UPDATES_IMAGE, SPOTIFICATIONS_PLAYLIST_LINK, TELEGRAM_CHAT_ID, EPISODE_PATTERN
from models import NotificationKeyboardButton, Release
from loguru import logger


load_dotenv()


def update_last_crawling_date(last_crawling_date):
    with open(".last_crawling_date", "w") as file:
        file.write(str(last_crawling_date))


def get_last_crawling_date():
    with open(".last_crawling_date") as file:
        return datetime.datetime.fromisoformat(file.readline())


def get_artists_latest_releases(client: SpotipyClient, newer_than: datetime):
    logger.debug("Retrieving artists ids")
    artists_ids = client.get.get_artists_ids()

    logger.debug(f"Crawling releases newer than {newer_than}")

    new_releases = []
    for i, aid in enumerate(artists_ids, start=1):
        releases = set(client.get.get_artist_releases(artist_id=aid, newer_than=newer_than))

        if releases:
            new_releases.extend(releases)
        logger.info(f"Processed {i}/{len(artists_ids)}")

    return new_releases


def get_shows_latest_episodes(client: SpotipyClient, newer_than: datetime):
    logger.debug("Retrieving shows ids")
    shows_ids = client.get.get_favorite_shows()

    logger.debug(f"Crawling episodes newer than {newer_than}")

    new_episodes = []
    for i, aid in enumerate(shows_ids, start=1):
        episodes = set(client.get.get_show_episodes(show_id=aid, newer_than=newer_than))

        if episodes:
            new_episodes.extend(episodes)
        logger.info(f"Processed {i}/{len(shows_ids)}")

    return new_episodes


def notify_no_releases(telegram_client: TelegramClient, crawling_date: datetime):
    telegram_client.send_message_with_image(
        text=f'No new releases from {crawling_date.strftime("%d.%m.%Y")}',
        image_url=NO_UPDATES_IMAGE,
        keyboard=telegram_client.compose_keyboard(
            NotificationKeyboardButton(url=SPOTIFICATIONS_PLAYLIST_LINK, text="Check ListenToMe playlist!").model_dump()
        )
    )


def send_release_notification(telegram_client: TelegramClient, release: Release):
    text = NOTITICATION_PATTERN.format(
        artists=release.artists,
        release_date=release.release_date,
        release_name=release.name,
        release_link=release.url
    ) if release.artists else (
        EPISODE_PATTERN.format(
            release_date=release.release_date,
            release_name=release.name,
            release_link=release.url
        )
    )

    telegram_client.send_message_with_image(
        text=text,
        image_url=release.cover_url,
        keyboard=telegram_client.compose_keyboard(
            NotificationKeyboardButton(url=release.url, text=release.name).model_dump(exclude_none=True),
            NotificationKeyboardButton(text="➕", callback_data=json.dumps({"song_id": release.uri})).model_dump(exclude_none=True)
        )
    )


def main():
    spotipy_client = SpotipyClient(spotipy_client=get_spotify_proxy())
    telegram_client = TelegramClient(chat_id=TELEGRAM_CHAT_ID, token=os.environ['TELEGRAM_BOT_TOKEN'])

    last_crawling_date = get_last_crawling_date()

    new_releases = get_artists_latest_releases(
        client=spotipy_client,
        newer_than=last_crawling_date,
    )

    new_episodes = get_shows_latest_episodes(
        client=spotipy_client,
        newer_than=last_crawling_date,
    )

    if not new_releases and not new_episodes:
        notify_no_releases(telegram_client=telegram_client, crawling_date=last_crawling_date)
    else:
        for release in [*new_releases, *new_episodes]:
            send_release_notification(telegram_client=telegram_client, release=release)

    now = datetime.datetime.now().date()
    update_last_crawling_date(now)
    logger.success(f"Crawling finished. Last crawling date set to: {now}")


if __name__ == "__main__":
    main()
