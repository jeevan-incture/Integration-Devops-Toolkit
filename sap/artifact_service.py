"""
SAP Artifact Service.

Responsible for downloading Integration Flow ZIP artifacts.
"""

from pathlib import Path

from sap.client import SAPClient


class ArtifactService:
    """Downloads Integration Flow artifacts."""

    DOWNLOAD_DIRECTORY = Path("workspace/downloads")

    def __init__(self):
        self.client = SAPClient()
        self.DOWNLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)

    def download(self, iflow: dict) -> Path:
        """
        Download an Integration Flow artifact ZIP.

        Parameters
        ----------
        iflow : dict
            {
                "id": "...",
                "version": "1.0.2"
            }

        Returns
        -------
        Path
            Downloaded ZIP path.
        """

        endpoint = (
            "/api/v1/IntegrationDesigntimeArtifacts"
            f"(Id='{iflow['id']}',Version='{iflow['version']}')/$value"
        )

        response = self.client.get(
            endpoint,
            stream=True,
            headers={
                "Accept": "application/octet-stream"
            }
        )

        zip_path = self.DOWNLOAD_DIRECTORY / f"{iflow['id']}.zip"

        with open(zip_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

        return zip_path

    def download_all(self, iflows: list[dict]) -> list[Path]:
        """
        Download multiple Integration Flow ZIPs.
        """

        downloaded = []

        for iflow in iflows:
            downloaded.append(self.download(iflow))

        return downloaded