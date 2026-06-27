"""
Manifest management.

Keeps track of synchronized IFlow versions.
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

    def save(self, iflows: list[dict]) -> None:
        """
        Persist synchronized IFlow versions.

        Rules
        -----
        - New IFlows are added.
        - Draft ('Active') versions never overwrite released versions.
        - Released versions overwrite previous released versions.
        """

        manifest = self.load()

        for flow in iflows:

            flow_id = flow["id"]
            current_version = flow["version"]

            if flow_id not in manifest:

                manifest[flow_id] = {
                    "package": flow["package"],
                    "name": flow["name"],
                    "version": current_version,
                    "last_synced": datetime.now(timezone.utc).isoformat()
                }

                continue

            # Ignore draft versions
            if current_version == "Active":
                continue

            manifest[flow_id]["version"] = current_version
            manifest[flow_id]["last_synced"] = datetime.now(timezone.utc).isoformat()

        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(manifest, file, indent=4)

    def get_iflows_to_sync(self, current_iflows: list[dict]) -> list[dict]:
        """
        Determine which IFlows require synchronization.

        Rules
        -----
        - First execution -> Sync everything.
        - New IFlow -> Sync.
        - Active -> Active -> Ignore.
        - 1.0.1 -> Active -> Ignore.
        - Active -> 1.0.1 -> Sync.
        - 1.0.1 -> 1.0.2 -> Sync.
        - Same released version -> Ignore.
        """

        previous = self.load()

        # First execution
        if not previous:
            for flow in current_iflows:
                flow["status"] = "INITIAL_SYNC"
            return current_iflows

        pending = []

        for flow in current_iflows:

            flow_id = flow["id"]
            current_version = flow["version"]

            # Newly created IFlow
            if flow_id not in previous:
                flow["status"] = "NEW_IFLOW"
                pending.append(flow)
                continue

            previous_version = previous[flow_id]["version"]

            # Ignore draft saves
            if current_version == "Active":
                continue

            # Released version changed
            if previous_version != current_version:
                flow["status"] = "VERSION_CHANGED"
                pending.append(flow)

        return pending