"""
Package configuration loader.

Supports JSON and CSV formats for defining packages to sync.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import List, Dict


class PackageConfig:
    """Loads package configuration from JSON or CSV."""

    @staticmethod
    def load_json(file_path: str | Path) -> List[Dict]:
        """
        Load packages from JSON file.

        Expected format:
        [
            {"id": "PACKAGE_1", "name": "Package 1"},
            {"id": "PACKAGE_2", "name": "Package 2"}
        ]

        Parameters
        ----------
        file_path : str | Path
            Path to JSON config file.

        Returns
        -------
        List[Dict]
            List of package configurations.
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Config file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        if not isinstance(config, list):
            raise ValueError("JSON config must be an array of package objects")

        return config

    @staticmethod
    def load_csv(file_path: str | Path) -> List[Dict]:
        """
        Load packages from CSV file.

        Expected format:
        id,name
        PACKAGE_1,Package 1
        PACKAGE_2,Package 2

        Parameters
        ----------
        file_path : str | Path
            Path to CSV config file.

        Returns
        -------
        List[Dict]
            List of package configurations.
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Config file not found: {file_path}")

        packages = []
        
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            
            if not reader.fieldnames or "id" not in reader.fieldnames:
                raise ValueError("CSV must have 'id' column")
            
            for row in reader:
                if row.get("id"):  # Skip empty rows
                    packages.append(row)

        return packages

    @staticmethod
    def load(file_path: str | Path) -> List[Dict]:
        """
        Auto-detect format and load config.

        Parameters
        ----------
        file_path : str | Path
            Path to config file (JSON or CSV).

        Returns
        -------
        List[Dict]
            List of package configurations.

        Raises
        ------
        ValueError
            If file format is not supported.
        """
        file_path = Path(file_path)
        
        if file_path.suffix.lower() == ".json":
            return PackageConfig.load_json(file_path)
        elif file_path.suffix.lower() == ".csv":
            return PackageConfig.load_csv(file_path)
        else:
            raise ValueError(f"Unsupported format: {file_path.suffix}")

    @staticmethod
    def validate_packages(packages: List[Dict]) -> bool:
        """
        Validate package configurations.

        Parameters
        ----------
        packages : List[Dict]
            Package configurations to validate.

        Returns
        -------
        bool
            True if valid.

        Raises
        ------
        ValueError
            If validation fails.
        """
        if not packages:
            raise ValueError("No packages configured")

        for pkg in packages:
            if "id" not in pkg or not pkg["id"].strip():
                raise ValueError("Each package must have an 'id' field")

        return True