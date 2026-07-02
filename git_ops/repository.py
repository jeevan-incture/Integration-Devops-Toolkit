"""
Git Repository Management with modern TUI.
"""

from __future__ import annotations

import shutil
import subprocess
from collections import Counter
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

    def commit_and_push(self, artifacts: list[dict]) -> bool:
        """Commit and push changes to GitHub.

        `artifacts` is a list of artifact metadata dicts (may include mixed types).
        Each dict is expected to have at least `id` and `version`; `status` and `package`
        are used when available.
        """
        try:
            try:
                status = self._run_git_command("status", "--porcelain")
                if not status:
                    Logger.info("No changes to commit")
                    return True
            except RuntimeError:
                Logger.info("No changes to commit")
                return True

            commit_msg = self._generate_commit_message(artifacts)

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

    def _generate_commit_message(self, artifacts: list[dict]) -> str:
        """Generate a descriptive commit message for mixed artifact syncs.

        Message layout:
        - Title with optional single package name
        - Summary (total artifacts, status counts)
        - Up to first 50 artifact detail lines: [STATUS] id vVERSION (package)
        """
        total = len(artifacts)
        packages = sorted({a.get("package") for a in artifacts if a.get("package")})
        package_desc = packages[0] if len(packages) == 1 else ", ".join(packages) if packages else None

        title = "Sync Design-Time Artifacts"
        if package_desc:
            title = f"{title} - {package_desc}"

        # Status counts
        statuses = [a.get("status", "SYNC") for a in artifacts]
        status_counts = Counter(statuses)
        counts_lines = [f"{k}: {v}" for k, v in status_counts.items()]

        # Detail lines (limit to 50)
        detail_lines = []
        for a in artifacts[:50]:
            status = a.get("status", "SYNC")
            aid = a.get("id") or a.get("name") or "Unknown"
            version = a.get("version", "Unknown")
            pkg = a.get("package")
            pkg_part = f" ({pkg})" if pkg else ""
            detail_lines.append(f"[{status}] {aid} v{version}{pkg_part}")

        if total > 50:
            detail_lines.append(f"...and {total - 50} more artifacts")

        message_parts = [
            title,
            "",
            f"Total artifacts: {total}",
            *counts_lines,
            "",
            "Details:",
            *detail_lines
        ]

        return "\n".join(message_parts)

    def cleanup(self) -> None:
        """Clean up repository resources after push."""
        # try:
        #     if self.repo_path.exists():
        #         Logger.info(f"Cleaning up repository at {self.repo_path}")
        #         shutil.rmtree(self.repo_path)
        #         Logger.success("Repository cleaned up successfully")
        #     else:
        #         Logger.info("Repository folder not found, nothing to clean")
        # except Exception as e:
        #     Logger.warning(f"Cleanup warning: {e}")
        pass