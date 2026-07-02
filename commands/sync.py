from pathlib import Path
from typing import Optional

from git_ops.manifest import Manifest
from git_ops.repository import GitRepository
from sap.iflow_service import IFlowService
from sap.message_mapping_service import MessageMappingService
from sap.value_mapping_service import ValueMappingService
from sap.script_collection_service import ScriptCollectionService
from config.settings import Settings
from config.packages_config import PackageConfig
from ui.logger import Logger, console


def run(config_format: str = "json", package_id: str = None):
    """Synchronize design-time artifacts from configuration."""
    
    Logger.progress_section("📦 PACKAGE CONFIGURATION")

    try:
        config_path = Settings.get_packages_config(config_format)
        Logger.info(f"Loading {config_format.upper()} configuration from {config_path}")
        
        packages = PackageConfig.load(config_path)
        PackageConfig.validate_packages(packages)
        
        Logger.success(f"✓ Loaded {len(packages)} package(s)")

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

        total_synced = 0
        total_downloaded = 0
        total_pushed = 0

        for idx, pkg in enumerate(packages_to_sync, 1):
            Logger.progress_section(f"🔄 PACKAGE {idx}/{len(packages_to_sync)}: {pkg['id']}")
            result = sync_package(pkg)
            total_synced += result.get("synced", 0)
            total_downloaded += result.get("downloaded", 0)
            total_pushed += result.get("pushed", 0)

        console.print()
        Logger.success_banner(
            "🎉 Batch Sync Completed Successfully",
            f"Configuration: {config_format.upper()}"
        )
        
        Logger.stats_box({
            "Config Format": config_format.upper(),
            "Packages Processed": len(packages_to_sync),
            "Artifacts Synced": total_synced,
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

    # Wrapper services (each has `.service` which is the downloader)
    iflow_service = IFlowService()
    message_service = MessageMappingService()
    value_service = ValueMappingService()
    script_service = ScriptCollectionService()

    git_repo = GitRepository()
    manifest = Manifest(Settings.MANIFEST_PATH)

    try:
        # Step 1: Fetch current artifacts for every type
        Logger.workflow_step(1, "Fetching artifacts", "running")

        current_iflows = iflow_service.service.list_artifacts(package_id)
        current_messages = message_service.service.list_artifacts(package_id)
        current_values = value_service.service.list_artifacts(package_id)
        current_scripts = script_service.service.list_artifacts(package_id)

        counts = {
            "IFlows": len(current_iflows),
            "MessageMappings": len(current_messages),
            "ValueMappings": len(current_values),
            "ScriptCollections": len(current_scripts),
        }

        total_items = sum(counts.values())
        if total_items == 0:
            Logger.warning("No artifacts found for package")
            return stats

        Logger.info(f"Found: {counts}")
        Logger.workflow_step(1, f"Fetching artifacts ({total_items} total)", "success")

        # Step 2: Determine pending artifacts using manifest
        Logger.workflow_step(2, "Analyzing synchronization requirements", "running")

        pending_iflows = manifest.get_iflows_to_sync(current_iflows)
        pending_messages = manifest.get_artifacts_to_sync("message_mappings", current_messages)
        pending_values = manifest.get_artifacts_to_sync("value_mappings", current_values)
        pending_scripts = manifest.get_artifacts_to_sync("script_collections", current_scripts)

        total_pending = len(pending_iflows) + len(pending_messages) + len(pending_values) + len(pending_scripts)

        if total_pending == 0:
            Logger.workflow_step(2, "Analyzing synchronization requirements", "skipped")
            Logger.info("No artifacts require synchronization")
            return stats

        Logger.info(
            f"Pending - IFlows: {len(pending_iflows)}, Messages: {len(pending_messages)}, "
            f"Values: {len(pending_values)}, Scripts: {len(pending_scripts)}"
        )
        Logger.workflow_step(2, f"Found {total_pending} pending artifact(s)", "success")

        # Step 3: Download pending artifacts
        Logger.workflow_step(3, "Downloading artifacts", "running")
        downloaded = []

        with Logger.download_progress(total_pending) as progress:
            task = progress.add_task("Downloading...", total=total_pending)

            for artifact in pending_iflows:
                try:
                    fp = iflow_service.service.download(artifact)
                    downloaded.append(fp)
                    stats["downloaded"] += 1
                    progress.update(task, advance=1)
                except Exception as e:
                    Logger.error(f"Failed to download IFlow {artifact.get('id')}: {e}")
                    raise

            for artifact in pending_messages:
                try:
                    fp = message_service.service.download(artifact)
                    downloaded.append(fp)
                    stats["downloaded"] += 1
                    progress.update(task, advance=1)
                except Exception as e:
                    Logger.error(f"Failed to download Message Mapping {artifact.get('id')}: {e}")
                    raise

            for artifact in pending_values:
                try:
                    fp = value_service.service.download(artifact)
                    downloaded.append(fp)
                    stats["downloaded"] += 1
                    progress.update(task, advance=1)
                except Exception as e:
                    Logger.error(f"Failed to download Value Mapping {artifact.get('id')}: {e}")
                    raise

            for artifact in pending_scripts:
                try:
                    fp = script_service.service.download(artifact)
                    downloaded.append(fp)
                    stats["downloaded"] += 1
                    progress.update(task, advance=1)
                except Exception as e:
                    Logger.error(f"Failed to download Script Collection {artifact.get('id')}: {e}")
                    raise

        Logger.workflow_step(3, f"Downloaded {len(downloaded)} artifact(s)", "success")

        # Step 4: Initialize Git repository
        Logger.workflow_step(4, "Initializing Git repository", "running")
        git_repo.init_or_update()
        Logger.workflow_step(4, "Git repository initialized", "success")

        # Step 5: Stage and push artifacts
        Logger.workflow_step(5, "Staging and pushing artifacts", "running")
        if downloaded:
            git_repo.add_artifacts(downloaded, package_id)

            all_pending = pending_iflows + pending_messages + pending_values + pending_scripts
            if git_repo.commit_and_push(all_pending):
                Logger.workflow_step(5, "Artifacts pushed to GitHub", "success")
                stats["pushed"] = len(all_pending)
                stats["synced"] = len(all_pending)
            else:
                Logger.workflow_step(5, "No changes to push", "skipped")

        # Step 6: Update manifest per artifact type
        Logger.workflow_step(6, "Updating manifest", "running")
        manifest.save_iflows(current_iflows)
        manifest.save("message_mappings", current_messages)
        manifest.save("value_mappings", current_values)
        manifest.save("script_collections", current_scripts)
        Logger.workflow_step(6, "Manifest updated", "success")

        return stats

    except Exception as ex:
        Logger.error_banner(f"❌ Failed to sync {package_id}", str(ex))
        raise
    finally:
        git_repo.cleanup()