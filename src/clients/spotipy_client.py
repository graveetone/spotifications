from .spotipy_clients import GetSpotipyClient, PostSpotipyClient
from loguru import logger


class SpotipyClient:
    def __init__(self, spotipy_client):
        self.client = spotipy_client

        self.get = GetSpotipyClient(self.client)
        self.post = PostSpotipyClient(self.client)

        logger.success("Initialized new Spotipy client")
