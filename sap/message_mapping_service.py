from sap.artifact_service import DesignTimeArtifactService


class MessageMappingService:
    def __init__(self):
        self.service = DesignTimeArtifactService(
            "MessageMappingDesigntimeArtifacts"
        )

    def list_message_mappings(self, package_id: str) -> list[dict]:
        return self.service.list_artifacts(package_id)

    def download_message_mapping(self, artifact: dict):
        return self.service.download(artifact)