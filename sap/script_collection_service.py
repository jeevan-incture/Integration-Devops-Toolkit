from sap.artifact_service import DesignTimeArtifactService


class ScriptCollectionService:
    def __init__(self):
        self.service = DesignTimeArtifactService(
            "ScriptCollectionDesigntimeArtifacts"
        )

    def list_script_collections(self, package_id: str) -> list[dict]:
        return self.service.list_artifacts(package_id)

    def download_script_collection(self, artifact: dict):
        return self.service.download(artifact)