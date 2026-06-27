"""
Help text and usage examples for the CLI.
"""

# Main help text
MAIN_HELP = """
SAP Integration DevOps Toolkit - Synchronize Integration Flows from SAP to GitHub
"""

MAIN_EPILOG = """
USAGE EXAMPLES:

  Interactive Mode (Prompted for Configuration & Sync Mode):
    python cli.py sync
    python -m integration_devops sync

  Specify JSON Format and Sync All Packages:
    python cli.py sync --config json
    
  Specify CSV Format and Sync All Packages:
    python cli.py sync --config csv

  Sync Single Package (JSON Format):
    python cli.py sync --config json --package CICDAutomation

  Sync Single Package (CSV Format):
    python cli.py sync --config csv --package TestPackage

  Direct Single Package Sync (Auto-detect Format):
    python cli.py sync --package CICDAutomation

CONFIGURATION FORMATS:

  JSON (config/packages.json):
    [
        {"id": "PACKAGE_1", "name": "Package 1", "description": "..."},
        {"id": "PACKAGE_2", "name": "Package 2", "description": "..."}
    ]

  CSV (config/packages.csv):
    id,name,description
    PACKAGE_1,Package 1,Description text
    PACKAGE_2,Package 2,Description text

ENVIRONMENT VARIABLES:

  Required:
    BTP_BASE_URL           - SAP BTP instance URL
    BTP_TOKEN_URL          - SAP authentication token endpoint
    BTP_CLIENT_ID          - SAP client credentials ID
    BTP_CLIENT_SECRET      - SAP client credentials secret
    GIT_REPOSITORY_URL     - GitHub repository URL
    GITHUB_TOKEN           - GitHub Personal Access Token

  Optional:
    GIT_BRANCH             - Target git branch (default: main)
    REPOSITORY_PATH        - Local repository path (default: repository)
    PACKAGES_CONFIG_JSON   - JSON config file path (default: config/packages.json)
    PACKAGES_CONFIG_CSV    - CSV config file path (default: config/packages.csv)
    MANIFEST_PATH          - Manifest file path (default: storage/manifest.json)
"""

# Sync command help
SYNC_HELP = "Synchronize Integration Flows from SAP to GitHub"

SYNC_DESCRIPTION = "Synchronize Integration Flows from SAP to GitHub"

SYNC_EPILOG = """
SYNC COMMAND EXAMPLES:

  Interactive (prompts for format and mode):
    python cli.py sync

  Interactive with JSON (prompts for single/all packages):
    python cli.py sync --config json

  Sync all packages from CSV:
    python cli.py sync --config csv

  Sync single package from JSON:
    python cli.py sync --config json --package CICDAutomation

  Sync single package from CSV:
    python cli.py sync --config csv --package TestPackage

  Sync without specifying format (auto-detect):
    python cli.py sync --package MyPackage

WORKFLOW:

  1. Fetch Integration Flows from SAP
  2. Check manifest for pending synchronizations
  3. Download pending IFlow artifacts as ZIP files
  4. Initialize Git repository (clone/pull)
  5. Stage and push artifacts to GitHub
  6. Update synchronization manifest

OUTPUT:

  - Detailed progress with workflow steps
  - Download progress bar with speed metrics
  - Summary statistics on completion
  - Error handling and logging
"""

# Argument help texts
CONFIG_HELP = "Configuration file format (json: structured | csv: spreadsheet)"
PACKAGE_HELP = "Specific package ID to sync (if not specified, syncs all packages)"