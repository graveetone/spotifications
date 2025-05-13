import requests
import os

CHAT_ID = "787823881"
BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
SEND_PHOTO_ENDPOINT = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'

def send_image(caption, image_url):
    response = requests.post(
        SEND_PHOTO_ENDPOINT,
        data={
            'chat_id': CHAT_ID,
            'photo': image_url,
            'caption': caption,
            'parse_mode': 'HTML'
        }
    )
    print(f"[TELEGRAM_NOTIFIER] {response.status_code} {response.json()}")

