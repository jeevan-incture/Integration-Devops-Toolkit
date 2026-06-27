"""
Git Repository Management with modern TUI.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Optional

from config.settings import Settings
from ui.logger import Logger


class GitRepository:
    """Manages Git operations using Git CLI with rich TUI."""

    def __init__(self):
        """Initialize Git repository manager."""
        self.repo_path = Settings.REPOSITORY_PATH
        self.repo_url = Settings.GIT_REPOSITORY_URL
        self.git_branch = Settings.GIT_BRANCH
        self.token = Settings.GITHUB_TOKEN

    def _run_git_command(self, *args) -> str:
        """Execute Git command."""
        cmd = ["git", "-C", str(self.repo_path), *args]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode != 0:
            raise RuntimeError(f"Git command failed: {result.stderr}")

        return result.stdout.strip()

    def _get_authenticated_url(self) -> str:
        """Build GitHub URL with authentication token."""
        if "https://" in self.repo_url:
            base_url = self.repo_url.replace("https://", "")
            return f"https://x-access-token:{self.token}@{base_url}"
        return self.repo_url

    def init_or_update(self) -> None:
        """Clone repository or pull latest changes."""
        try:
            if self.repo_path.exists():
                Logger.info(f"Repository exists at {self.repo_path}")
                self._pull()
            else:
                Logger.info(f"Cloning repository...")
                auth_url = self._get_authenticated_url()
                subprocess.run(
                    ["git", "clone", "--branch", self.git_branch, auth_url, str(self.repo_path)],
                    check=True,
                    capture_output=True
                )
                Logger.success("Repository cloned successfully")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to initialize repository: {e.stderr}")

    def _pull(self) -> None:
        """Pull latest changes from remote."""
        try:
            Logger.info(f"Pulling latest changes from {self.git_branch}")
            self._run_git_command("pull", "origin", self.git_branch)
            Logger.success("Pull completed")
        except RuntimeError as e:
            Logger.warning(f"Pull warning: {e}")

    def add_artifacts(self, zip_files: list[Path], package_id: str) -> None:
        """Add ZIP artifacts to repository."""
        package_dir = self.repo_path / "packages" / package_id
        package_dir.mkdir(parents=True, exist_ok=True)

        added_files = []

        for zip_file in zip_files:
            if not zip_file.exists():
                Logger.warning(f"ZIP file not found: {zip_file}")
                continue

            dest_file = package_dir / zip_file.name
            shutil.copy2(zip_file, dest_file)
            added_files.append(str(dest_file.relative_to(self.repo_path)))
            Logger.success(f"Added: {zip_file.name}")

        if added_files:
            for file_path in added_files:
                self._run_git_command("add", file_path)
            Logger.success(f"Staged {len(added_files)} file(s)")

    def commit_and_push(self, iflows: list[dict]) -> bool:
        """Commit and push changes to GitHub."""
        try:
            try:
                status = self._run_git_command("status", "--porcelain")
                if not status:
                    Logger.info("No changes to commit")
                    return True
            except RuntimeError:
                Logger.info("No changes to commit")
                return True

            commit_msg = self._generate_commit_message(iflows)

            Logger.info("Creating commit...")
            self._run_git_command("commit", "-m", commit_msg)
            Logger.success("Commit created")

            Logger.info(f"Pushing to {self.git_branch}...")
            self._run_git_command("push", "origin", self.git_branch)
            Logger.success("Push completed")

            return True

        except RuntimeError as e:
            Logger.error(f"Commit/Push failed: {e}")
            return False

    def _generate_commit_message(self, iflows: list[dict]) -> str:
        """Generate descriptive commit message."""
        flow_details = []

        for iflow in iflows:
            status = iflow.get("status", "SYNC")
            flow_id = iflow.get("id", "Unknown")
            version = iflow.get("version", "Unknown")
            flow_details.append(f"[{status}] {flow_id} v{version}")

        message = "Sync Integration Flows\n\n"
        message += "\n".join(flow_details)

        return message

    def cleanup(self) -> None:
        """Clean up repository resources."""
        pass