import requests
import os
import json
from enum import Enum
from pprint import pprint
from loguru import logger


class TelegramClient:
    def __init__(self, chat_id: str, token: str):
        self.chat_id = chat_id
        self.token = token

    def send_message_with_image(self, text: str, image_url: str, keyboard: list):
        logger.debug("Sending telegram notification")
        response = requests.post(
            url=self.send_photo_endpoint,
            data={
                'chat_id': self.chat_id,
                'photo': image_url,
                'caption': text,
                'parse_mode': 'HTML',
                'reply_markup': json.dumps({
                    'inline_keyboard': keyboard
                })
            }
        )
        logger.debug(f"[TELEGRAM_NOTIFIER] {response.status_code}")

    @property
    def send_photo_endpoint(self):
        return f'https://api.telegram.org/bot{self.token}/sendPhoto'

    @staticmethod
    def compose_keyboard(*buttons):
        return [[button] for button in buttons]
