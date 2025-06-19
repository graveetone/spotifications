from datetime import datetime
from typing import Optional
from .spotipy_clients import AuthSpotipyClient, GetSpotipyClient, PostSpotipyClient
from loguru import logger


class SpotipyClient:
    def __init__(self, spotipy_client):
        self.client = spotipy_client

        self.auth = AuthSpotipyClient(self.client)
        self.get = GetSpotipyClient(self.client)
        self.post = PostSpotipyClient(self.client)

        self.auth.refresh_token()

        logger.success("Initialized new Spotipy client")