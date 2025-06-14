import os

class AuthSpotipyClient:
    def __init__(self, spotipy_client):
        self.client = spotipy_client

    def refresh_token(self):
        print("Refreshing token")
        self.client.auth_manager.refresh_token = os.environ.get("SPOTIFY_REFRESH_TOKEN")
        token_info = self.client.auth_manager.refresh_access_token(
            self.client.auth_manager.refresh_token
        )
        self.client.token = token_info['access_token']
        print("Token was successfully refreshed")
