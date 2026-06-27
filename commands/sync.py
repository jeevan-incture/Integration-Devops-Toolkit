from pathlib import Path
from typing import Optional

from git_ops.manifest import Manifest
from git_ops.repository import GitRepository
from sap.artifact_service import ArtifactService
from sap.iflow_service import IFlowService
from config.settings import Settings
from config.packages_config import PackageConfig
from ui.logger import Logger, console


def run(config_format: str = "json", package_id: str = None):
    """Synchronize Integration Flows from configuration."""
    
    Logger.progress_section("📦 PACKAGE CONFIGURATION")

    try:
        # Get config path based on format
        config_path = Settings.get_packages_config(config_format)
        Logger.info(f"Loading {config_format.upper()} configuration from {config_path}")
        
        # Load package configuration
        packages = PackageConfig.load(config_path)
        PackageConfig.validate_packages(packages)
        
        Logger.success(f"✓ Loaded {len(packages)} package(s)")

        # Determine which packages to sync
        if package_id:
            packages_to_sync = [p for p in packages if p["id"] == package_id]
            if not packages_to_sync:
                Logger.error(f"Package not found in config: {package_id}")
                return
            Logger.info(f"Syncing single package: {package_id}")
        else:
            packages_to_sync = packages
            Logger.info(f"Syncing all {len(packages_to_sync)} packages")

        Logger.table_packages(packages_to_sync)

        # Sync each package
        total_synced = 0
        total_downloaded = 0
        total_pushed = 0

        for idx, pkg in enumerate(packages_to_sync, 1):
            Logger.progress_section(f"🔄 PACKAGE {idx}/{len(packages_to_sync)}: {pkg['id']}")
            result = sync_package(pkg)
            total_synced += result.get("synced", 0)
            total_downloaded += result.get("downloaded", 0)
            total_pushed += result.get("pushed", 0)

        # Final summary
        console.print()
        Logger.success_banner(
            "🎉 Batch Sync Completed Successfully",
            f"Configuration: {config_format.upper()}"
        )
        
        Logger.stats_box({
            "Config Format": config_format.upper(),
            "Packages Processed": len(packages_to_sync),
            "IFlows Synced": total_synced,
            "Artifacts Downloaded": total_downloaded,
            "Changes Pushed": total_pushed,
            "Target Branch": Settings.GIT_BRANCH
        })

    except FileNotFoundError as e:
        Logger.error_banner("❌ Configuration Error", str(e))
        raise
    except ValueError as e:
        Logger.error_banner("❌ Validation Error", str(e))
        raise
    except Exception as ex:
        Logger.error_banner("❌ Synchronization Failed", str(ex))
        raise


def sync_package(package: dict) -> dict:
    """Synchronize a single package and return stats."""
    
    package_id = package["id"]
    stats = {"synced": 0, "downloaded": 0, "pushed": 0}

    iflow_service = IFlowService()
    artifact_service = ArtifactService()
    git_repo = GitRepository()
    manifest = Manifest(Settings.MANIFEST_PATH)

    downloaded = []

    try:
        # Step 1
        Logger.workflow_step(1, "Fetching Integration Flows", "running")
        current_iflows = iflow_service.list_iflows(package_id)

        if not current_iflows:
            Logger.warning("No Integration Flows found")
            return stats

        Logger.workflow_step(1, f"Fetching Integration Flows ({len(current_iflows)} found)", "success")

        # Step 2
        Logger.workflow_step(2, "Analyzing synchronization requirements", "running")
        pending_iflows = manifest.get_iflows_to_sync(current_iflows)

        if not pending_iflows:
            Logger.workflow_step(2, "Analyzing synchronization requirements", "skipped")
            Logger.info("No IFlows require synchronization")
            return stats

        Logger.workflow_step(2, f"Found {len(pending_iflows)} pending IFlow(s)", "success")
        Logger.table_iflows(pending_iflows)

        # Step 3
        Logger.workflow_step(3, "Downloading Integration Flow artifacts", "running")
        
        with Logger.download_progress(len(pending_iflows)) as progress:
            task = progress.add_task("Downloading...", total=len(pending_iflows))
            
            for iflow in pending_iflows:
                try:
                    zip_file = artifact_service.download(iflow)
                    downloaded.append(zip_file)
                    stats["downloaded"] += 1
                    progress.update(task, advance=1)
                except Exception as e:
                    Logger.error(f"Failed to download {iflow['id']}: {e}")
                    raise

        Logger.workflow_step(3, f"Downloaded {len(downloaded)} artifact(s)", "success")

        # Step 4
        Logger.workflow_step(4, "Initializing Git repository", "running")
        git_repo.init_or_update()
        Logger.workflow_step(4, "Git repository initialized", "success")

        # Step 5
        Logger.workflow_step(5, "Staging and pushing artifacts", "running")
        if downloaded:
            git_repo.add_artifacts(downloaded, package_id)
            if git_repo.commit_and_push(pending_iflows):
                Logger.workflow_step(5, "Artifacts pushed to GitHub", "success")
                stats["pushed"] = len(pending_iflows)
                stats["synced"] = len(pending_iflows)
            else:
                Logger.workflow_step(5, "No changes to push", "skipped")

        # Step 6
        Logger.workflow_step(6, "Updating manifest", "running")
        manifest.save(current_iflows)
        Logger.workflow_step(6, "Manifest updated", "success")

        return stats

    except Exception as ex:
        Logger.error_banner(f"❌ Failed to sync {package_id}", str(ex))
        raise
    finally:
        git_repo.cleanup()