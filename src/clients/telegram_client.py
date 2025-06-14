import requests
import os
import json
from enum import Enum
from pprint import pprint


class TelegramClient:
    def __init__(self, chat_id: str, token: str):
        self.chat_id = chat_id
        self.token = token

    def send_message_with_image(self, text: str, image_url: str, keyboard: list):
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
        print(f"[TELEGRAM_NOTIFIER] {response.status_code}")

    @property
    def send_photo_endpoint(self):
        return f'https://api.telegram.org/bot{self.token}/sendPhoto'

    @staticmethod
    def compose_keyboard(*buttons):
        return [[button] for button in buttons]

def send_image(caption, button_caption, button_link, image_url, song_id=None):
    keyboard = [[
                    {
                        'text': button_caption,
                        'url': button_link
                    }
                ]]
    if song_id is not None:
        keyboard.append(                    [{
                        'text': "+",
                        'callback_data': json.dumps({"song_id": song_id})
                    }])
    response = requests.post(
        SEND_PHOTO_ENDPOINT,
        data={
            'chat_id': CHAT_ID,
            'photo': image_url,
            'caption': caption,
            'parse_mode': 'HTML',
            'reply_markup': json.dumps({
                'inline_keyboard': keyboard
            })
        }
    )
    print(f"[TELEGRAM_NOTIFIER] {response.status_code}")
    pprint(response.json())

