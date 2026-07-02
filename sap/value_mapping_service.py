from sap.artifact_service import DesignTimeArtifactService


class ValueMappingService:
    def __init__(self):
        self.service = DesignTimeArtifactService(
            "ValueMappingDesigntimeArtifacts"
        )

    def list_value_mappings(self, package_id: str) -> list[dict]:
        return self.service.list_artifacts(package_id)

    def download_value_mapping(self, artifact: dict):
        return self.service.download(artifact)