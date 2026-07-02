from pathlib import Path

from sap.client import SAPClient


class DesignTimeArtifactService:
    DOWNLOAD_DIRECTORY = Path("workspace/downloads")

    def __init__(self, artifact_collection: str):
        self.client = SAPClient()
        self.artifact_collection = artifact_collection
        self.DOWNLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)

    def list_artifacts(self, package_id: str) -> list[dict]:
        endpoint = (
            f"/api/v1/IntegrationPackages('{package_id}')/"
            f"{self.artifact_collection}?$format=json"
        )

        response = self.client.get(endpoint)
        results = response.json()["d"]["results"]

        return [
            {
                "id": item.get("Id"),
                "name": item.get("Name"),
                "package": item.get("PackageId"),
                "version": item.get("Version"),
                "description": item.get("Description"),
                "download_url": item["__metadata"]["media_src"],
            }
            for item in results
        ]

    def download(self, artifact: dict) -> Path:
        endpoint = (
            f"/api/v1/{self.artifact_collection}"
            f"(Id='{artifact['id']}',Version='{artifact['version']}')/$value"
        )

        response = self.client.get(
            endpoint,
            stream=True,
            headers={"Accept": "application/octet-stream"},
        )

        zip_path = self.DOWNLOAD_DIRECTORY / f"{artifact['id']}.zip"

        with open(zip_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

        return zip_path

    def download_all(self, artifacts: list[dict]) -> list[Path]:
        return [self.download(artifact) for artifact in artifacts]

