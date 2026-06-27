"""
SAP Integration Package service.
"""

from sap.client import SAPClient


class PackageService:

    def __init__(self):
        self.client = SAPClient()

    def exists(self, package_id: str) -> bool:

        endpoint = f"/api/v1/IntegrationPackages('{package_id}')?$format=json"

        response = self.client.get(endpoint)

        return response.status_code == 200