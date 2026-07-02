from sap.artifact_service import DesignTimeArtifactService


class IFlowService:
    def __init__(self):
        self.service = DesignTimeArtifactService(
            "IntegrationDesigntimeArtifacts"
        )

    def list_iflows(self, package_id: str) -> list[dict]:
        return self.service.list_artifacts(package_id)