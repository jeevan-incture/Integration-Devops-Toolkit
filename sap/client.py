import requests

from config.settings import Settings
from sap.auth import SAPAuth


class SAPClient:

    def __init__(self):
        token = SAPAuth().get_token()

        self.base_url = Settings.BTP_BASE_URL

        self.session = requests.Session()

        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        })

    def get(self, endpoint: str, **kwargs):

        response = self.session.get(
            f"{self.base_url}{endpoint}",
            timeout=60,
            **kwargs
        )

        response.raise_for_status()

        return response

    def post(self, endpoint: str, **kwargs):

        response = self.session.post(
            f"{self.base_url}{endpoint}",
            timeout=60,
            **kwargs
        )

        response.raise_for_status()

        return response