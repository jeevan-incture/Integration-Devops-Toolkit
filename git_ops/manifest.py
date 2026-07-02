"""
Manifest management.

Keeps track of synchronized design-time artifact versions.
"""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timezone


class Manifest:
    """Reads and writes the synchronization manifest."""

    def __init__(self, manifest_path: str | Path = "storage/manifest.json") -> None:
        """
        Parameters
        ----------
        manifest_path : str | Path, optional
            Location of the manifest file.
            Defaults to 'storage/manifest.json'.
        """
        self.file_path = Path(manifest_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> dict:
        """
        Load manifest from disk.

        Returns
        -------
        dict
            Existing manifest or an empty dictionary.
        """
        if not self.file_path.exists():
            return {}

        with self.file_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _normalize_manifest(self, manifest: dict) -> dict:
        """
        Normalize legacy flat manifests into typed sections.

        Old manifests were a flat mapping of artifact IDs.
        New manifests group artifacts by type.
        """
        if not manifest:
            return {}

        if all(
            isinstance(value, dict)
            and {"package", "name", "version", "last_synced"}.issubset(value.keys())
            for value in manifest.values()
        ):
            return {"integration_flows": manifest}

        return manifest

    def save(self, artifact_type: str, artifacts: list[dict]) -> None:
        """
        Persist synchronized artifact versions for a specific artifact type.

        Parameters
        ----------
        artifact_type : str
            One of:
            - "integration_flows"
            - "message_mappings"
            - "value_mappings"
            - "script_collections"
        artifacts : list[dict]
            List of artifact metadata dictionaries.
        """
        manifest = self._normalize_manifest(self.load())
        section = manifest.setdefault(artifact_type, {})

        for artifact in artifacts:
            artifact_id = artifact["id"]
            current_version = artifact["version"]

            if artifact_id not in section:
                section[artifact_id] = {
                    "package": artifact["package"],
                    "name": artifact["name"],
                    "version": current_version,
                    "last_synced": datetime.now(timezone.utc).isoformat(),
                }
                continue

            if current_version == "Active":
                continue

            section[artifact_id]["version"] = current_version
            section[artifact_id]["last_synced"] = datetime.now(timezone.utc).isoformat()

        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(manifest, file, indent=4)

    def get_artifacts_to_sync(
        self, artifact_type: str, current_artifacts: list[dict]
    ) -> list[dict]:
        """
        Determine which artifacts require synchronization for a specific artifact type.
        """
        previous = self._normalize_manifest(self.load()).get(artifact_type, {})

        if not previous:
            for artifact in current_artifacts:
                artifact["status"] = "INITIAL_SYNC"
            return current_artifacts

        pending = []

        for artifact in current_artifacts:
            artifact_id = artifact["id"]
            current_version = artifact["version"]

            if artifact_id not in previous:
                artifact["status"] = "NEW_ARTIFACT"
                pending.append(artifact)
                continue

            previous_version = previous[artifact_id]["version"]

            if current_version == "Active":
                continue

            if previous_version != current_version:
                artifact["status"] = "VERSION_CHANGED"
                pending.append(artifact)

        return pending

    def save_iflows(self, iflows: list[dict]) -> None:
        """Compatibility wrapper for existing IFlow sync code."""
        self.save("integration_flows", iflows)

    def get_iflows_to_sync(self, current_iflows: list[dict]) -> list[dict]:
        """Compatibility wrapper for existing IFlow sync code."""
        return self.get_artifacts_to_sync("integration_flows", current_iflows)