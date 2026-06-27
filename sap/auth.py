import requests

from config.settings import Settings


class AuthenticationError(Exception):
    """Raised when SAP authentication fails."""


class SAPAuth:

    def __init__(self):
        self.settings = Settings

    def get_token(self) -> str:

        payload = {
            "grant_type": "client_credentials",
            "client_id": self.settings.BTP_CLIENT_ID,
            "client_secret": self.settings.BTP_CLIENT_SECRET,
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.post(
            self.settings.BTP_TOKEN_URL,
            headers=headers,
            data=payload,
            timeout=30,
        )

        if response.status_code != 200:
            raise AuthenticationError(response.text)

        body = response.json()

        return body["access_token"]