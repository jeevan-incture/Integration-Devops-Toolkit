"""
SAP Integration Flow service.
"""

from sap.client import SAPClient


class IFlowService:

    def __init__(self):
        self.client = SAPClient()

    def list_iflows(self, package_id: str) -> list[dict]:

        endpoint = (
            f"/api/v1/IntegrationPackages('{package_id}')"
            "/IntegrationDesigntimeArtifacts?$format=json"
        )

        response = self.client.get(endpoint)

        results = response.json()["d"]["results"]

        return [
            {
                "id": item["Id"],
                "name": item["Name"],
                "package": item["PackageId"],
                "version": item["Version"],
                "modified_at": item["ModifiedAt"],
                "download_url": item["__metadata"]["media_src"],
            }
            for item in results
        ]
    