import requests
import os
import json

CHAT_ID = "787823881"
BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
SEND_PHOTO_ENDPOINT = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'

def send_image(caption, button_caption, button_link, image_url):
    response = requests.post(
        SEND_PHOTO_ENDPOINT,
        data={
            'chat_id': CHAT_ID,
            'photo': image_url,
            'caption': caption,
            'parse_mode': 'HTML',
            'reply_markup': json.dumps({
                'inline_keyboard': [[
                    {
                        'text': button_caption,
                        'url': button_link
                    },
                    # {
                    #     'text': "Listen Later",
                    #     'url': button_link
                    # }
                ]]
            })
        }
    )
    print(f"[TELEGRAM_NOTIFIER] {response.status_code} {response.json()}")

