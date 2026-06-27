"""
Application configuration.

Loads configuration from environment variables.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings."""

    # ------------------------------------------------------------------
    # SAP Integration Suite
    # ------------------------------------------------------------------

    BTP_BASE_URL: str = os.getenv("BTP_BASE_URL", "").rstrip("/")
    BTP_TOKEN_URL: str = os.getenv("BTP_TOKEN_URL", "").rstrip("/")
    BTP_CLIENT_ID: str = os.getenv("BTP_CLIENT_ID", "")
    BTP_CLIENT_SECRET: str = os.getenv("BTP_CLIENT_SECRET", "")

    # ------------------------------------------------------------------
    # GitHub
    # ------------------------------------------------------------------

    GIT_REPOSITORY_URL: str = os.getenv("GIT_REPOSITORY_URL", "")
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    GIT_BRANCH: str = os.getenv("GIT_BRANCH", "main")

    # ------------------------------------------------------------------
    # Package Configuration
    # ------------------------------------------------------------------

    PACKAGES_CONFIG_JSON: Path = Path(
        os.getenv("PACKAGES_CONFIG_JSON", "config/packages.json")
    )

    PACKAGES_CONFIG_CSV: Path = Path(
        os.getenv("PACKAGES_CONFIG_CSV", "config/packages.csv")
    )

    SYNC_MODE: str = os.getenv("SYNC_MODE", "all")

    # ------------------------------------------------------------------
    # Local Paths
    # ------------------------------------------------------------------

    REPOSITORY_PATH: Path = Path(
        os.getenv("REPOSITORY_PATH", "repository")
    )

    MANIFEST_PATH: Path = Path(
        os.getenv(
            "MANIFEST_PATH",
            "storage/manifest.json"
        )
    )

    WORKSPACE_PATH: Path = Path(
        os.getenv("WORKSPACE_PATH", "workspace")
    )

    DOWNLOAD_PATH: Path = WORKSPACE_PATH / "downloads"

    EXTRACT_PATH: Path = WORKSPACE_PATH / "extracted"

    @classmethod
    def get_packages_config(cls, format: str = "json") -> Path:
        """
        Get packages config path based on format.

        Parameters
        ----------
        format : str
            Configuration format ("json" or "csv").

        Returns
        -------
        Path
            Path to configuration file.
        """
        if format.lower() == "json":
            return cls.PACKAGES_CONFIG_JSON
        elif format.lower() == "csv":
            return cls.PACKAGES_CONFIG_CSV
        else:
            raise ValueError(f"Unsupported format: {format}")

    @classmethod
    def validate(cls) -> None:
        """Validate mandatory settings."""

        required = {
            "BTP_BASE_URL": cls.BTP_BASE_URL,
            "BTP_TOKEN_URL": cls.BTP_TOKEN_URL,
            "BTP_CLIENT_ID": cls.BTP_CLIENT_ID,
            "BTP_CLIENT_SECRET": cls.BTP_CLIENT_SECRET,
            "GIT_REPOSITORY_URL": cls.GIT_REPOSITORY_URL,
            "GITHUB_TOKEN": cls.GITHUB_TOKEN,
        }

        missing = [key for key, value in required.items() if not value]

        if missing:
            raise ValueError(
                f"Missing environment variables: {', '.join(missing)}"
            )