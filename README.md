# 🚀 SAP Integration DevOps Toolkit

**Seamless synchronization of SAP Integration Flows to GitHub**

A Python-based CLI application that automates the synchronization of SAP Cloud Platform Integration (CPI) flows to GitHub repositories, enabling version control, collaborative development, and CI/CD automation for SAP integration landscapes.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Module Documentation](#module-documentation)
- [Data Flow](#data-flow)
- [Manifest System](#manifest-system)
- [GitHub Actions Integration](#github-actions-integration)
- [API Reference](#api-reference)
- [Development Guide](#development-guide)
- [Future Roadmap](#future-roadmap)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## Overview

### What Does It Do?

The SAP Integration DevOps Toolkit automates the following workflow:

```
SAP BTP System
    ↓ (Fetch Integration Flows)
Manifest Tracking System
    ↓ (Identify Changes)
Download Artifacts
    ↓ (ZIP Files)
Git Repository Management
    ↓ (Commit & Push)
GitHub Repository
```

### Key Capabilities

- **🔄 Automatic Synchronization**: Fetch integration flows from SAP BTP on schedule or on-demand
- **📊 Version Tracking**: Manifest-based change detection (only syncs modified flows)
- **📦 Multi-Package Support**: Sync single or multiple packages in batch operations
- **🎯 Smart Differentials**: Ignores unchanged flows and draft versions
- **🔐 Secure Credentials**: Environment-based configuration with no hardcoded secrets
- **🎨 Rich Terminal UI**: Modern TUI with progress bars, tables, and color-coded output
- **⚙️ Flexible Configuration**: Support for JSON or CSV package definitions
- **🤖 CI/CD Ready**: GitHub Actions workflow included for automated daily syncs
- **📈 Scalable Architecture**: Extensible plugin-based design for future integrations

---

## Architecture

### High-Level Design

```
┌────────────────────────────────────────────────────────────┐
│                      CLI Layer                             │
│                    (cli.py, help.py)                       │
│  - Parse arguments                                         │
│  - Display interactive menus                              │
│  - Show rich TUI output                                   │
└────────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────────┐
│                   Orchestration Layer                       │
│                    (commands/sync.py)                       │
│  - Load package configuration                              │
│  - Coordinate sync workflow                                │
│  - Manage statistics & summaries                           │
└────────────────────────────────────────────────────────────┘
                          ↓
        ┌─────────────────┴─────────────────┐
        ↓                                   ↓
┌──────────────────────┐          ┌──────────────────────┐
│    SAP Services      │          │   Git Services       │
│  (sap/ folder)       │          │ (git_ops/ folder)    │
│  - Authentication    │          │ - Manifest tracking  │
│  - IFlow Retrieval   │          │ - Repository sync    │
│  - Artifact Download │          │ - Commit/Push        │
└──────────────────────┘          └──────────────────────┘
        ↓                                   ↓
┌────────────────────────────────────────────────────────────┐
│              Infrastructure Layer                           │
│  - HTTP Clients     - File I/O       - Git CLI             │
│  - Config Loading   - Error Handling  - Progress Tracking  │
└────────────────────────────────────────────────────────────┘
```

### Design Patterns

| Pattern | Usage | Example |
|---------|-------|---------|
| **Service Layer** | Encapsulate external API calls | `SAPClient`, `IFlowService`, `GitRepository` |
| **Repository Pattern** | Abstract data persistence | `Manifest` class for state tracking |
| **Configuration Object** | Centralized settings | `Settings` class with environment loading |
| **Factory Pattern** | Format-agnostic loading | `PackageConfig.load(path)` auto-detects format |
| **Workflow Pattern** | Multi-step orchestration | 6-step sync pipeline in `sync_package()` |
| **Logging Facade** | Consistent UI output | `Logger` class with rich formatting |

---

## Features

### ✅ Current Features (v1.0.0)

- [x] OAuth 2.0 authentication with SAP BTP
- [x] List integration flows from SAP packages
- [x] Download IFlow artifacts as ZIP files
- [x] Version-aware manifest tracking (JSON format)
- [x] Differential synchronization (only sync changed flows)
- [x] Clone/pull Git repositories
- [x] Commit and push changes to GitHub
- [x] Dual-format package configuration (JSON & CSV)
- [x] Interactive CLI with menu-driven mode
- [x] Command-line arguments for automation
- [x] Rich terminal UI with colors and progress bars
- [x] Batch processing (all packages or single package)
- [x] Comprehensive error handling and validation
- [x] GitHub Actions workflow (daily scheduled sync)
- [x] Detailed workflow step tracking

### 🚧 Future Features (Roadmap)

- [ ] **Multi-Repository Support**: Sync to different GitHub repos based on package
- [ ] **Branch Strategy**: Auto-create branches for PRs instead of direct pushes
- [ ] **Rollback Capability**: Revert to previous manifest versions
- [ ] **Extract & Parse ZIPs**: Decompose artifacts into versioned structure
- [ ] **Dependency Analysis**: Track IFlow dependencies and integration patterns
- [ ] **Conflict Detection**: Alert on simultaneous SAP/Git modifications
- [ ] **Webhook Triggers**: Real-time sync on SAP flow updates via callbacks
- [ ] **Database Logging**: Persist sync history and metrics to database
- [ ] **Slack/Email Notifications**: Alert on sync success/failure
- [ ] **Web Dashboard**: Visual monitoring of sync status and statistics
- [ ] **Multi-Tenant Support**: Handle multiple SAP systems in single instance
- [ ] **Docker Containerization**: Easy deployment and scaling
- [ ] **API Server**: REST endpoints for programmatic sync control
- [ ] **Plugin System**: Custom handlers for post-sync actions
- [ ] **Advanced Filtering**: Sync by flow name patterns, creation date ranges
- [ ] **Azure DevOps Support**: Additional Git platform beyond GitHub
- [ ] **SAP Release Management**: Integration with SAP's transport system
- [ ] **Performance Metrics**: Track sync times, data volumes, success rates
- [ ] **Encryption**: Secret management for credentials in GitHub

---

## Installation

### Prerequisites

- **Python 3.9+** (tested on 3.11)
- **Git 2.30+** (must be in PATH)
- **SAP BTP Access**: Valid client credentials for integration suite
- **GitHub Account**: Repository with push access

### Setup Steps

#### 1. Clone Repository

```bash
git clone https://github.com/jeevan-incture/sap-integration-devops.git
cd sap-integration-devops
```

#### 2. Create Virtual Environment

```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/macOS (Bash)
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**requirements.txt contents**:
```
requests
python-dotenv
rich
```

#### 4. Configure Environment

Create `.env` file in project root:

```env
# SAP BTP Configuration
BTP_BASE_URL=
BTP_TOKEN_URL=
BTP_CLIENT_ID=
BTP_CLIENT_SECRET

# GitHub Configuration
GIT_REPOSITORY_URL=
GITHUB_TOKEN=
GIT_BRANCH=

# Paths
REPOSITORY_PATH=repository
MANIFEST_PATH=storage/manifest.json
PACKAGES_CONFIG_JSON=config/packages.json
PACKAGES_CONFIG_CSV=config/packages.csv
WORKSPACE_PATH=workspace
```

#### 5. Create Package Configuration

**Option A: JSON format** (`config/packages.json`):
```json
[
  {
    "id": "CICDAutomation",
    "name": "CICD Automation Package",
    "description": "Integration flows for CICD automation"
  },
  {
    "id": "TestPackage",
    "name": "Test Package",
    "description": "Test integration flows"
  }
]
```

**Option B: CSV format** (`config/packages.csv`):
```csv
id,name,description
CICDAutomation,CICD Automation Package,Integration flows for CICD automation
TestPackage,Test Package,Test integration flows
```

#### 6. Add to .gitignore

```gitignore
# Environment
.env
.env.local
*.key

# Downloads
workspace/downloads/
workspace/extracted/

# Repository
repository/

# Python
__pycache__/
*.pyc
venv/
.venv/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

---

## Configuration

### Environment Variables

#### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `BTP_BASE_URL` | SAP BTP instance root URL | `https://inccpidev.it-cpi001.cfapps.eu10.hana.ondemand.com` |
| `BTP_TOKEN_URL` | OAuth 2.0 token endpoint | `https://inccpidev.authentication.eu10.hana.ondemand.com/oauth/token` |
| `BTP_CLIENT_ID` | Service account client ID | `sb-xxxx!b63626\|it!b16077` |
| `BTP_CLIENT_SECRET` | Service account secret | `21d76727-xxx$IgvdYL0OkQmv0...` |
| `GIT_REPOSITORY_URL` | GitHub repository HTTPS URL | `https://github.com/org/repo.git` |
| `GITHUB_TOKEN` | GitHub Personal Access Token (repo scope) | `ghp_xxxxxxxxxxxx` |

#### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GIT_BRANCH` | Target Git branch | `main` |
| `REPOSITORY_PATH` | Local repo directory | `repository` |
| `MANIFEST_PATH` | Manifest file location | `storage/manifest.json` |
| `PACKAGES_CONFIG_JSON` | JSON config path | `config/packages.json` |
| `PACKAGES_CONFIG_CSV` | CSV config path | `config/packages.csv` |
| `WORKSPACE_PATH` | Working directory | `workspace` |

### Package Configuration Formats

#### JSON Format (`config/packages.json`)

```json
[
  {
    "id": "PACKAGE_ID_1",
    "name": "Human Readable Name",
    "description": "Optional description for documentation"
  }
]
```

**Advantages**:
- Structured, hierarchical data
- Comments support (though not in standard JSON)
- Better for complex metadata

#### CSV Format (`config/packages.csv`)

```csv
id,name,description
PACKAGE_ID_1,Human Readable Name,Optional description
PACKAGE_ID_2,Another Package,Another description
```

**Advantages**:
- Easy to edit in spreadsheet applications
- Familiar to non-technical users
- Simpler to version control diffs

### SAP BTP Setup

#### 1. Get Service Account Credentials

1. Login to SAP BTP cockpit
2. Navigate: **Subaccount → Services → Service Instances**
3. Create new instance for "Cloud Integration"
4. Note: `clientid`, `clientsecret`, `tokenendpoint`, `landscape_id`

#### 2. Obtain API Endpoints

1. Go to **Cloud Integration → Integrations**
2. Copy instance URL (this is `BTP_BASE_URL`)
3. Token endpoint is typically: `https://{landscape_id}.authentication.{region}.hana.ondemand.com/oauth/token`

### GitHub Setup

#### 1. Create Personal Access Token (PAT)

1. GitHub Settings → Developer settings → Personal access tokens
2. Click "Generate new token"
3. Scopes needed: `repo` (full repository access)
4. Copy token and add to `.env` as `GITHUB_TOKEN`

#### 2. Create Repository

```bash
# Create new repo
git init Incture-Integration-Repository
cd Incture-Integration-Repository
git branch -M main
git remote add origin https://github.com/org/repo.git
```

---

## Usage

### Interactive Mode (Recommended for Learning)

```bash
python cli.py sync
```

**Flow**:
1. Display banner and system info
2. Prompt: "Choose configuration format" (JSON or CSV)
3. Prompt: "Choose sync mode" (All packages or Single package)
4. If single: "Enter Package ID"
5. Execute sync workflow
6. Display statistics and summary

### Command-Line Arguments (Automation)

```bash
# Sync all packages (JSON format)
python cli.py sync --config json

# Sync all packages (CSV format)
python cli.py sync --config csv

# Sync single package
python cli.py sync --config json --package CICDAutomation

# Auto-detect format and sync single package
python cli.py sync --package TestPackage
```

### Usage Examples

#### Example 1: First-Time Sync (All Packages)

```bash
# Interactive mode
$ python cli.py sync

# Output:
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📦 PACKAGE CONFIGURATION
# ✓ Loaded 2 package(s)
# ℹ Syncing all 2 packages
#
# 🔄 PACKAGE 1/2: CICDAutomation
# ✓ [1] Fetching Integration Flows (5 found)
# ✓ [2] Found 3 pending IFlow(s)
# ✓ [3] Downloaded 3 artifact(s)
# ✓ [4] Git repository initialized
# ✓ [5] Artifacts pushed to GitHub
# ✓ [6] Manifest updated
#
# 🎉 Batch Sync Completed Successfully
```

#### Example 2: Sync Specific Package with Version Check

```bash
python cli.py sync --config json --package CICDAutomation
# Only syncs flows that have version changes from previous sync
```

#### Example 3: CSV Configuration

```bash
# Use CSV instead of JSON
python cli.py sync --config csv
# Will load config/packages.csv instead of packages.json
```

### Help & Documentation

```bash
# Main help
python cli.py --help

# Sync command help
python cli.py sync --help

# Output includes:
# - Argument descriptions
# - Usage examples
# - Configuration formats
# - Environment variables
# - Workflow description
```

---

## Project Structure

```
sap-integration-devops/
├── README.md                          # This file
├── .env                               # Environment configuration (NOT versioned)
├── .gitignore                         # Git ignore rules
├── requirements.txt                   # Python dependencies
│
├── cli.py                             # CLI entry point with banner and menus
├── storage/                           # Data storage
│   └── manifest.json                  # Version tracking (generated)
│
├── config/                            # Configuration modules
│   ├── __init__.py
│   ├── settings.py                    # Environment settings loader
│   ├── packages.json                  # JSON package configuration
│   ├── packages.csv                   # CSV package configuration
│   └── packages_config.py             # Config parser (JSON/CSV)
│
├── commands/                          # Command implementations
│   ├── __init__.py
│   └── sync.py                        # Main sync orchestration
│
├── sap/                               # SAP Integration Suite modules
│   ├── __init__.py
│   ├── auth.py                        # OAuth 2.0 authentication
│   ├── client.py                      # HTTP client with auth
│   ├── package_service.py             # Package validation
│   ├── iflow_service.py               # List integration flows
│   └── artifact_service.py            # Download IFlow ZIPs
│
├── git_ops/                           # Git repository operations
│   ├── __init__.py
│   ├── manifest.py                    # Version tracking & diff logic
│   └── repository.py                  # Git clone/pull/push operations
│
├── ui/                                # User interface modules
│   ├── __init__.py
│   ├── logger.py                      # Rich TUI output formatting
│   └── help.py                        # CLI help text and examples
│
├── workspace/                         # Runtime working directory
│   ├── downloads/                     # Downloaded ZIP files (temporary)
│   ├── extracted/                     # Extracted artifacts (future)
│   └── logs/                          # Execution logs (future)
│
├── repository/                        # Local Git repository (cloned from GitHub)
│   └── packages/
│       ├── CICDAutomation/            # Package directory
│       │   ├── IF_Automation_Test.zip
│       │   └── IF_Automation_Test2.zip
│       └── TestPackage/
│
└── .github/
    └── workflows/
        └── sync-integration-flows.yml # GitHub Actions workflow
```

---

## Module Documentation

### Core Modules

#### `cli.py` - Command-Line Interface

**Responsibility**: Parse arguments, display TUI, coordinate CLI workflow

**Key Functions**:
- `display_banner()`: Shows ASCII art banner with styled title
- `display_system_info()`: Displays version, status, environment info
- `display_config_menu()`: Interactive JSON/CSV selector
- `display_sync_menu()`: Interactive all/single package selector
- `create_parser()`: Creates argparse parser with help text
- `main()`: Entry point - handles all CLI logic

**Dependencies**: `argparse`, `rich`, `ui.help`, `ui.logger`

**Exit Codes**:
- `0`: Success
- `1`: General error
- `KeyboardInterrupt`: User cancelled

---

#### `config/settings.py` - Configuration Management

**Responsibility**: Load and provide access to all configuration from `.env` and defaults

**Key Classes**:
- `Settings`: Dataclass-like configuration holder

**Key Methods**:
- `get_packages_config(format)`: Returns path to JSON or CSV config
- `validate()`: Checks required variables are set

**Configuration Variables**:
```python
# SAP
BTP_BASE_URL
BTP_TOKEN_URL
BTP_CLIENT_ID
BTP_CLIENT_SECRET

# GitHub
GIT_REPOSITORY_URL
GITHUB_TOKEN
GIT_BRANCH

# Paths
REPOSITORY_PATH
MANIFEST_PATH
PACKAGES_CONFIG_JSON
PACKAGES_CONFIG_CSV
WORKSPACE_PATH
```

---

#### `config/packages_config.py` - Package Configuration Loader

**Responsibility**: Load package definitions from JSON or CSV files with validation

**Key Classes**:
- `PackageConfig`: Factory for loading and validating package configs

**Key Methods**:
- `load_json(file_path)`: Parse JSON array of package objects
- `load_csv(file_path)`: Parse CSV with id/name/description columns
- `load(file_path)`: Auto-detect format and load
- `validate_packages(packages)`: Ensure all packages have "id" field

**Expected Package Structure**:
```python
{
    "id": "PACKAGE_ID",
    "name": "Human Readable Name",
    "description": "Optional description"
}
```

---

#### `commands/sync.py` - Synchronization Orchestration

**Responsibility**: Coordinate entire sync workflow from config to manifest update

**Key Functions**:
- `run(config_format, package_id)`: Main entry point
  - Loads package config
  - Filters packages (all or single)
  - Displays package table
  - Loops through packages calling `sync_package()`
  - Aggregates statistics
  - Displays summary

- `sync_package(package)`: 6-step sync pipeline for single package
  ```
  1. Fetch IFlows from SAP
  2. Analyze sync requirements (manifest diff)
  3. Download pending artifacts
  4. Initialize Git repository
  5. Stage and push to GitHub
  6. Update manifest
  ```

**Error Handling**:
- `FileNotFoundError`: Config file missing
- `ValueError`: Validation failure
- Generic `Exception`: Wrapped in error banner

**Return Value** (from `sync_package`):
```python
{
    "synced": 0,      # Number of flows synchronized
    "downloaded": 0,  # Number of artifacts downloaded
    "pushed": 0       # Number of changes pushed to Git
}
```

---

#### `sap/auth.py` - SAP Authentication

**Responsibility**: Obtain OAuth 2.0 tokens for SAP BTP API calls

**Key Classes**:
- `SAPAuth`: Handles token acquisition
- `AuthenticationError`: Custom exception for auth failures

**Key Methods**:
- `get_token()`: Client credentials flow
  - POST to `BTP_TOKEN_URL`
  - Payload: `grant_type=client_credentials`, `client_id`, `client_secret`
  - Returns: Bearer token string
  - Timeout: 30 seconds

---

#### `sap/client.py` - HTTP Client

**Responsibility**: Authenticated HTTP layer for all SAP API calls

**Key Classes**:
- `SAPClient`: Wraps requests.Session with Bearer token

**Key Methods**:
- `get(endpoint, **kwargs)`: GET request with auto-auth
- `post(endpoint, **kwargs)`: POST request with auto-auth

**Features**:
- Automatic Bearer token injection
- 60-second timeout on all requests
- Status code checking (raises HTTPError on non-2xx)
- Kwargs pass-through for streaming, headers, etc.

---

#### `sap/iflow_service.py` - Integration Flow Retrieval

**Responsibility**: Fetch list of integration flows from SAP package

**Key Classes**:
- `IFlowService`: High-level flow listing

**Key Methods**:
- `list_iflows(package_id)`: Get flows for package
  - Endpoint: `/api/v1/IntegrationPackages('{id}')/IntegrationDesigntimeArtifacts?$format=json`
  - Returns: List of flow dicts with: `id`, `name`, `package`, `version`, `modified_at`, `download_url`

**OData Response Format**:
```json
{
  "d": {
    "results": [
      {
        "Id": "FLOW_ID",
        "Name": "Flow Name",
        "PackageId": "PKG_ID",
        "Version": "1.0.2",
        "ModifiedAt": "/Date(1234567890000)/",
        "__metadata": {"media_src": "..."}
      }
    ]
  }
}
```

---

#### `sap/artifact_service.py` - Artifact Download

**Responsibility**: Download integration flow artifacts as ZIP files

**Key Classes**:
- `ArtifactService`: Manages artifact downloads

**Key Methods**:
- `download(iflow)`: Download single flow
  - Endpoint: `/api/v1/IntegrationDesigntimeArtifacts(Id='...',Version='...')/$value`
  - Streams ZIP content in 8KB chunks
  - Saves to: `workspace/downloads/{iflow_id}.zip`
  - Returns: `Path` object

- `download_all(iflows)`: Batch download helper
  - Loops through flows calling `download()`
  - Returns: List of Path objects

---

#### `git_ops/manifest.py` - Version Tracking

**Responsibility**: Track synchronized IFlow versions to enable differential syncs

**Key Classes**:
- `Manifest`: Reads/writes manifest.json

**Key Methods**:
- `load()`: Read manifest from disk
  - Returns: Dict with structure `{flow_id: {package, name, version, last_synced}}`
  - Returns: Empty dict if file missing

- `save(iflows)`: Persist synchronized flows
  - Updates existing entries with new version/timestamp
  - Ignores draft ('Active') versions
  - Preserves previous data for unmodified flows

- `get_iflows_to_sync(current_iflows)`: Determine pending syncs
  - Compares current flows vs. manifest
  - Rules:
    - **First execution**: Sync all (status: `INITIAL_SYNC`)
    - **New flow**: Sync (status: `NEW_IFLOW`)
    - **Version changed**: Sync (status: `VERSION_CHANGED`)
    - **Draft save**: Ignore
    - **Same version**: Ignore
  - Returns: List of flows with `status` field added

**Manifest File Format**:
```json
{
  "IF_Automation_Test": {
    "package": "CICDAutomation",
    "name": "IF_Automation_Test",
    "version": "1.0.2",
    "last_synced": "2026-06-27T10:07:41.610821+00:00"
  }
}
```

---

#### `git_ops/repository.py` - Git Operations

**Responsibility**: Clone/pull GitHub repo and push synchronized artifacts

**Key Classes**:
- `GitRepository`: Wraps Git CLI operations

**Key Methods**:
- `init_or_update()`: Clone if missing, else pull
  - Uses authenticated URL with token
  - Clones specific branch via `--branch` flag
  - Pulls latest from remote if repo exists

- `add_artifacts(zip_files, package_id)`: Copy ZIPs to repo
  - Creates: `packages/{package_id}/`
  - Copies each ZIP file there
  - Stages files with `git add`

- `commit_and_push(iflows)`: Commit and push to GitHub
  - Checks `git status --porcelain` for changes
  - Creates commit with formatted message (see below)
  - Pushes to `origin {branch}`

- `_generate_commit_message(iflows)`: Format commit message
  ```
  Sync Integration Flows

  [INITIAL_SYNC] IF_Automation_Test v1.0.0
  [VERSION_CHANGED] IF_Automation_Test2 v1.0.2
  ```

**Git Workflow**:
```bash
git clone --branch main https://x-access-token:{token}@github.com/org/repo.git
cd repository
git pull origin main
cp /path/to/IF_*.zip packages/CICDAutomation/
git add packages/CICDAutomation/*.zip
git commit -m "Sync Integration Flows\n\n[INITIAL_SYNC] IF_Automation_Test v1.0.0"
git push origin main
```

---

#### `ui/logger.py` - Terminal UI

**Responsibility**: Provide consistent rich terminal output with colors, icons, tables

**Key Classes**:
- `Logger`: Static methods for all UI output

**Output Methods**:
- `success(msg)`: ✓ Green message
- `error(msg)`: ✗ Red message
- `warning(msg)`: ⚠ Yellow message
- `info(msg)`: ℹ Blue message
- `step(num, msg)`: → Numbered step
- `section(title)`: Divider line
- `table_iflows(iflows)`: Status/ID/Name/Version table
- `table_packages(packages)`: ID/Name/Description table
- `download_progress(total)`: Progress bar context manager
- `task_progress()`: Generic task progress bar
- `summary(title, items)`: Summary panel
- `success_banner(title, msg)`: Green success panel
- `error_panel(title, msg)`: Red error panel
- `error_banner(title, msg)`: Alias for error_panel
- `json_output(data)`: Syntax-highlighted JSON
- `workflow_step(step_num, title, status)`: Workflow step with icon
  - Status: "pending" (⏳), "running" (🔄), "success" (✓), "error" (✗), "skipped" (⊘)
- `progress_section(section_name)`: Section divider
- `stats_box(stats)`: Statistics display

**Dependencies**: `rich` library (Progress, Console, Table, Panel, Syntax, etc.)

---

### Service Layer Pattern

All SAP and Git operations follow a service layer pattern:

```python
# Service classes encapsulate external integrations
class SAPAuth:
    def get_token(self) -> str:
        # OAuth logic

class IFlowService:
    def list_iflows(self, package_id: str) -> list[dict]:
        # SAP API interaction

class GitRepository:
    def init_or_update(self) -> None:
        # Git operations

# Orchestrator coordinates services
def sync_package(package: dict):
    iflow_service = IFlowService()  # Create service
    git_repo = GitRepository()       # Create service
    
    # Use services
    iflows = iflow_service.list_iflows(package["id"])
    git_repo.add_artifacts(artifacts, package["id"])
```

---

## Data Flow

### Complete Synchronization Workflow

```
START
  │
  ├─ Load Configuration
  │  ├─ Load .env file
  │  ├─ Parse --config (json|csv) argument
  │  └─ Parse --package argument (optional)
  │
  ├─ Load Package List
  │  ├─ Load JSON or CSV config file
  │  └─ Validate: each package has "id" field
  │
  ├─ Filter Packages
  │  ├─ If --package specified: filter to single package
  │  └─ Else: use all packages
  │
  └─→ FOR EACH PACKAGE:
     │
     ├─ Step 1: Fetch IFlows from SAP
     │  ├─ SAPAuth: Get OAuth token
     │  ├─ IFlowService: Query /api/v1/IntegrationPackages/.../Artifacts
     │  └─ Extract: id, name, version, etc.
     │
     ├─ Step 2: Analyze Sync Requirements
     │  ├─ Manifest: Load previous sync state
     │  ├─ Manifest: Compare current vs. previous versions
     │  └─ Determine: INITIAL_SYNC, NEW_IFLOW, VERSION_CHANGED, SKIP
     │
     ├─ Step 3: Download Artifacts
     │  ├─ For each pending IFlow:
     │  │  ├─ ArtifactService: GET /api/v1/IntegrationDesigntimeArtifacts/$value
     │  │  └─ Stream ZIP to workspace/downloads/{id}.zip
     │  └─ Display: progress bar with speed metrics
     │
     ├─ Step 4: Initialize Git Repository
     │  ├─ GitRepository: Check if local repo exists
     │  ├─ If missing: Clone from GitHub with token auth
     │  └─ If exists: Pull latest from origin
     │
     ├─ Step 5: Stage & Push Artifacts
     │  ├─ Copy ZIPs to packages/{package_id}/ directory
     │  ├─ Git add: stage files
     │  ├─ Git commit: with formatted message including flow details
     │  └─ Git push: origin {branch}
     │
     ├─ Step 6: Update Manifest
     │  ├─ Manifest: Update storage/manifest.json
     │  ├─ Persist: new versions and timestamps
     │  └─ File: JSON format with ISO8601 timestamps
     │
     ├─ Aggregate: Statistics (synced, downloaded, pushed)
     │
     └─ Display: Workflow step indicators with status
  
  ├─ Aggregate Results
  │  └─ Combine statistics from all packages
  │
  ├─ Display Summary
  │  ├─ Success banner
  │  ├─ Statistics table
  │  └─ Total counts
  │
  └─ END (exit 0) or ERROR (exit 1)
```

### Error Handling Flow

```
Exception Occurs
  │
  ├─ FileNotFoundError
  │  ├─ Config file not found
  │  ├─ Display: Error panel
  │  └─ Exit: 1
  │
  ├─ ValueError
  │  ├─ Validation failed (missing "id" in package)
  │  ├─ Display: Error panel
  │  └─ Exit: 1
  │
  ├─ GitCommandError
  │  ├─ Git operation failed (bad credentials, network)
  │  ├─ Display: Error message
  │  └─ Continue: with next package (may affect aggregate)
  │
  ├─ RequestException
  │  ├─ HTTP error from SAP (timeout, 401, 500)
  │  ├─ Display: Error message
  │  └─ Exit: 1 (with context about which package failed)
  │
  └─ Generic Exception
     ├─ Unexpected error
     ├─ Display: Error panel with traceback
     └─ Exit: 1
```

---

## Manifest System

### Purpose

The manifest tracks which IFlow versions have been synchronized, enabling:
- **Differential Syncs**: Only changed flows are downloaded
- **Version History**: Audit trail of what was synced when
- **Idempotency**: Re-running sync doesn't duplicate work

### File Location

`storage/manifest.json` (configurable via `MANIFEST_PATH`)

### File Format

```json
{
  "IF_Automation_Test": {
    "package": "CICDAutomation",
    "name": "IF_Automation_Test",
    "version": "1.0.2",
    "last_synced": "2026-06-27T10:07:41.610821+00:00"
  },
  "IF_Another_Flow": {
    "package": "TestPackage",
    "name": "IF_Another_Flow",
    "version": "1.0.0",
    "last_synced": "2026-06-27T10:08:15.123456+00:00"
  }
}
```

### Sync Rules

When updating manifest, the following rules apply:

1. **New IFlow** (not in manifest)
   - Action: Add entry
   - Status: `NEW_IFLOW`

2. **New Version** (released)
   - Example: Manifest has 1.0.1, SAP has 1.0.2
   - Action: Update version and timestamp
   - Status: `VERSION_CHANGED`

3. **Draft Version** ("Active")
   - Example: SAP has version "Active" (unsaved draft)
   - Action: Ignore (don't sync, don't update manifest)
   - Reason: Drafts may be incomplete

4. **Same Released Version**
   - Example: Manifest and SAP both have 1.0.2
   - Action: Skip sync
   - Status: (not included in pending list)

5. **First Execution** (manifest empty)
   - Action: Sync all flows
   - Status: `INITIAL_SYNC` for all flows

### Example Sync Scenario

**Initial State**:
```json
{}  // Empty manifest
```

**SAP Has**:
```
IF_Automation_Test (v1.0.0)
IF_Automation_Test2 (v1.0.0)
```

**Run 1: First Sync**
- Status: INITIAL_SYNC for both
- Downloaded: 2 flows
- Manifest Updated:
  ```json
  {
    "IF_Automation_Test": {"version": "1.0.0", "last_synced": "..."},
    "IF_Automation_Test2": {"version": "1.0.0", "last_synced": "..."}
  }
  ```

**SAP Now Has** (after developer updates IF_Automation_Test to v1.0.1):
```
IF_Automation_Test (v1.0.1)
IF_Automation_Test (Active)  // Draft
IF_Automation_Test2 (v1.0.0)
```

**Run 2: Second Sync**
- IF_Automation_Test: VERSION_CHANGED (1.0.0 → 1.0.1) ✓ Sync
- IF_Automation_Test: Active draft → Ignored
- IF_Automation_Test2: No change → Skipped
- Downloaded: 1 flow
- Manifest Updated: IF_Automation_Test.version = 1.0.1

---

## GitHub Actions Integration

### Purpose

Automate daily synchronization without manual intervention.

### Workflow File

`.github/workflows/sync-integration-flows.yml`

### Trigger Configuration

```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
  workflow_dispatch:     # Manual trigger available
    inputs:
      package_id:
        description: 'Optional specific package to sync'
        type: string
```

### Workflow Steps

1. **Checkout**: Clone repository with full history
2. **Setup Python**: Install Python 3.11
3. **Install Dependencies**: `pip install -r requirements.txt`
4. **Configure Git**: Set committer identity
5. **Validate Secrets**: Verify all required environment variables set
6. **Run Sync**: Execute `python cli.py sync`
7. **Upload Artifacts**: Save downloaded ZIPs and manifest as workflow artifacts
8. **Error Notification**: Post error comment to workflow

### Environment Variables (GitHub Secrets)

Add these as **GitHub Repository Secrets** (not in .env):

| Secret Name | Value |
|---|---|
| `BTP_BASE_URL` | SAP BTP instance URL |
| `BTP_TOKEN_URL` | Token endpoint |
| `BTP_CLIENT_ID` | Service account ID |
| `BTP_CLIENT_SECRET` | Service account secret |
| `GIT_REPOSITORY_URL` | GitHub repo URL |
| `GIT_GITHUB_TOKEN` | GitHub PAT token |

### Manual Trigger

```bash
# Trigger workflow with optional package parameter
curl -X POST \
  -H "Authorization: token {GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/{owner}/{repo}/actions/workflows/sync-integration-flows.yml/dispatches \
  -d '{"ref":"main","inputs":{"package_id":"CICDAutomation"}}'
```

### Viewing Workflow Runs

1. Go to: **Actions** tab in GitHub
2. Select: **Sync Integration Flows** workflow
3. View: Run history with status (success/failure)
4. Download: Artifacts (ZIPs, manifest, logs)

---

## API Reference

### CLI Commands

#### `cli.py sync`

Synchronize integration flows from SAP to GitHub.

**Signature**:
```
python cli.py sync [--config {json,csv}] [--package PACKAGE_ID]
```

**Arguments**:
- `--config {json,csv}` (optional)
  - Specify configuration format
  - Default: Interactive menu if not specified
  - `json`: Load from `config/packages.json`
  - `csv`: Load from `config/packages.csv`

- `--package PACKAGE_ID` (optional)
  - Sync specific package only
  - Default: Sync all packages if not specified
  - Example: `--package CICDAutomation`

**Examples**:
```bash
python cli.py sync
python cli.py sync --config json
python cli.py sync --config csv --package TestPackage
```

**Exit Codes**:
- `0`: Success
- `1`: Error occurred
- `KeyboardInterrupt`: User cancelled (Ctrl+C)

---

### Python API (For Custom Scripts)

#### `commands.sync.run(config_format, package_id)`

Main synchronization function.

```python
from commands.sync import run

# Sync all packages (JSON format)
run(config_format="json")

# Sync single package (CSV format)
run(config_format="csv", package_id="CICDAutomation")
```

**Parameters**:
- `config_format` (str): "json" or "csv"
- `package_id` (str, optional): Specific package to sync

**Returns**: None

**Raises**:
- `FileNotFoundError`: Config file not found
- `ValueError`: Validation failed
- `Exception`: Sync error (already logged with banner)

---

#### `git_ops.manifest.Manifest`

Version tracking class.

```python
from git_ops.manifest import Manifest

manifest = Manifest("storage/manifest.json")

# Load previous state
previous_state = manifest.load()

# Get flows needing sync
pending_flows = manifest.get_iflows_to_sync(current_iflows)

# Update manifest
manifest.save(synced_iflows)
```

**Methods**:
- `load() -> dict`: Load manifest from disk
- `save(iflows) -> None`: Persist synchronized flows
- `get_iflows_to_sync(current_iflows) -> list[dict]`: Determine pending syncs

---

#### `sap.iflow_service.IFlowService`

Fetch integration flows from SAP.

```python
from sap.iflow_service import IFlowService

service = IFlowService()
flows = service.list_iflows("CICDAutomation")

for flow in flows:
    print(f"{flow['id']} v{flow['version']}")
```

**Methods**:
- `list_iflows(package_id: str) -> list[dict]`: Get flows for package

**Returns**: List of dicts with fields: `id`, `name`, `package`, `version`, `modified_at`, `download_url`

---

#### `sap.artifact_service.ArtifactService`

Download IFlow artifacts.

```python
from sap.artifact_service import ArtifactService

service = ArtifactService()
zip_path = service.download({"id": "IF_Test", "version": "1.0.0"})
print(f"Downloaded to: {zip_path}")

# Batch download
zips = service.download_all(iflows_list)
```

**Methods**:
- `download(iflow: dict) -> Path`: Download single flow
- `download_all(iflows: list) -> list[Path]`: Batch download

---

#### `git_ops.repository.GitRepository`

Git operations.

```python
from git_ops.repository import GitRepository

repo = GitRepository()

# Initialize (clone or pull)
repo.init_or_update()

# Add artifacts
repo.add_artifacts([Path("IF_1.zip"), Path("IF_2.zip")], "CICDAutomation")

# Push to GitHub
success = repo.commit_and_push(pending_iflows)
```

**Methods**:
- `init_or_update() -> None`: Clone or pull repository
- `add_artifacts(zip_files, package_id) -> None`: Stage artifacts
- `commit_and_push(iflows) -> bool`: Commit and push

---

## Development Guide

### Adding a New Command

1. Create new file: `commands/your_command.py`
   ```python
   def run(arg1: str, arg2: str = None):
       """Your command implementation."""
       from ui.logger import Logger
       Logger.progress_section("🔄 YOUR COMMAND")
       # Implementation
       Logger.success_banner("✨ Success", "Command completed")
   ```

2. Update `cli.py`:
   ```python
   from commands.your_command import run as your_run
   
   # In create_parser():
   your_parser = subparsers.add_parser(
       "your-command",
       help="Your command description"
   )
   your_parser.add_argument(...)
   
   # In main():
   if args.command == "your-command":
       your_run(args.arg1, args.arg2)
   ```

### Adding a New SAP Service

1. Create new file: `sap/your_service.py`
   ```python
   from sap.client import SAPClient
   
   class YourService:
       def __init__(self):
           self.client = SAPClient()
       
       def your_method(self, param: str) -> dict:
           endpoint = f"/api/v1/YourEndpoint/{param}"
           response = self.client.get(endpoint)
           return response.json()
   ```

2. Update `commands/sync.py`:
   ```python
   from sap.your_service import YourService
   
   your_service = YourService()
   result = your_service.your_method("value")
   ```

### Adding Configuration Variables

1. Add to `.env`:
   ```env
   YOUR_VARIABLE=value
   ```

2. Add to `config/settings.py`:
   ```python
   YOUR_VARIABLE: str = os.getenv("YOUR_VARIABLE", "default_value")
   ```

3. Access in code:
   ```python
   from config.settings import Settings
   value = Settings.YOUR_VARIABLE
   ```

### Testing

Create `tests/` directory with test files:

```python
# tests/test_manifest.py
import unittest
from git_ops.manifest import Manifest

class TestManifest(unittest.TestCase):
    def test_sync_rules(self):
        manifest = Manifest(":memory:")  # In-memory for testing
        # Test sync rule logic

if __name__ == "__main__":
    unittest.main()
```

Run tests:
```bash
python -m pytest tests/ -v
```

---

## Future Roadmap

### Phase 2: Enhanced Features (Q3 2026)

#### 2.1 Extract & Parse ZIPs
- [ ] Decompose artifact ZIPs into versioned directory structure
- [ ] Generate project metadata files (CHANGELOG, MANIFEST)
- [ ] Support for integration documentation extraction

#### 2.2 Dependency Analysis
- [ ] Extract iflow dependencies from artifacts
- [ ] Generate dependency graphs
- [ ] Alert on circular dependencies

#### 2.3 Conflict Detection
- [ ] Detect simultaneous SAP and GitHub modifications
- [ ] Implement merge conflict resolution strategies
- [ ] Webhook support for real-time SAP updates

### Phase 3: Enterprise Features (Q4 2026)

#### 3.1 Multi-Repository Support
- [ ] Route packages to different GitHub repos
- [ ] Support for multiple Git platforms (Azure DevOps, GitLab)
- [ ] Repository group management

#### 3.2 Branch Strategy
- [ ] Auto-create feature branches for PRs
- [ ] Automatic PR creation after sync
- [ ] Branch cleanup policies

#### 3.3 Database Logging
- [ ] Persist sync history to database
- [ ] Track metrics (sync duration, success rates)
- [ ] Query API for historical data

### Phase 4: Operational Excellence (2027)

#### 4.1 Web Dashboard
- [ ] Visual monitoring of sync status
- [ ] Real-time statistics and trends
- [ ] Alert configuration and management

#### 4.2 Notifications
- [ ] Slack notifications on sync events
- [ ] Email reports and digests
- [ ] Custom webhook support

#### 4.3 Rollback Capability
- [ ] Revert to previous manifest versions
- [ ] Point-in-time recovery
- [ ] Backup scheduling

#### 4.4 API Server
- [ ] REST endpoints for programmatic control
- [ ] Webhook receivers for SAP events
- [ ] Authentication and rate limiting

### Phase 5: Advanced Features (2027-2028)

#### 5.1 Plugin System
- [ ] Custom handlers for post-sync actions
- [ ] Extensible metadata processors
- [ ] Community plugin registry

#### 5.2 Multi-Tenant Support
- [ ] Handle multiple SAP systems
- [ ] Per-tenant configuration isolation
- [ ] Tenant-level metrics and auditing

#### 5.3 SAP Release Management
- [ ] Integration with SAP transport system
- [ ] Automatic promotion workflows
- [ ] Release scheduling and coordination

#### 5.4 Advanced Filtering
- [ ] Sync by flow name patterns
- [ ] Date range based filtering
- [ ] Custom predicates for sync decisions

#### 5.5 Performance Optimization
- [ ] Parallel downloads for large batches
- [ ] Incremental ZIP extraction
- [ ] Caching strategies for manifest

---

## Troubleshooting

### Common Issues

#### Issue: "Bad git executable" Error

**Symptom**:
```
ImportError: Bad git executable.
The git executable must be specified in one of the following ways:
```

**Solution**:
1. Install Git for Windows from https://git-scm.com/download/win
2. Restart your terminal
3. Verify: `git --version`

#### Issue: "Missing environment variables" Error

**Symptom**:
```
ValueError: Missing environment variables: BTP_BASE_URL, BTP_CLIENT_ID, GITHUB_TOKEN
```

**Solution**:
1. Verify `.env` file exists in project root
2. Check file contains all required variables (see Configuration section)
3. Verify values are correct and not commented out
4. Try: `echo $BTP_BASE_URL` to verify env var is loaded

#### Issue: "Package not found in config" Error

**Symptom**:
```
Logger.error('Package not found in config: TestPackage')
```

**Solution**:
1. Check package ID in `config/packages.json` or `config/packages.csv`
2. Verify spelling matches exactly (case-sensitive)
3. If using CSV, ensure no extra whitespace around ID

#### Issue: "Authentication failed" (401 Error)

**Symptom**:
```
sap.auth.AuthenticationError: Unauthorized
Response: 401 Client Authentication failed
```

**Solutions**:
1. Verify BTP_CLIENT_ID and BTP_CLIENT_SECRET are correct
2. Check credentials haven't expired (in SAP BTP cockpit)
3. Verify BTP_TOKEN_URL is correct for your landscape
4. Test with curl: 
   ```bash
   curl -X POST -u "{client_id}:{client_secret}" -d "grant_type=client_credentials" {BTP_TOKEN_URL}
   ```

#### Issue: "Repository cloning failed" (404 Error)

**Symptom**:
```
RuntimeError: Failed to initialize repository: fatal: repository not found
```

**Solutions**:
1. Verify GIT_REPOSITORY_URL is correct
2. Verify GITHUB_TOKEN has `repo` scope
3. Test with git directly: 
   ```bash
   git clone https://x-access-token:{token}@github.com/org/repo.git
   ```
4. Check repository exists and is not private (or token has access)

#### Issue: "Connection timeout"

**Symptom**:
```
requests.exceptions.ConnectTimeout: Connection timeout
```

**Solutions**:
1. Check network connectivity
2. Verify SAP BTP_BASE_URL is accessible
3. Increase timeout values in config (if supported)
4. Check firewall/proxy settings
5. Try from different network to isolate issue

#### Issue: "Manifest corruption" (Invalid JSON)

**Symptom**:
```
json.JSONDecodeError: Expecting value: line 1 column 1
```

**Solutions**:
1. Backup current manifest: `cp storage/manifest.json storage/manifest.backup.json`
2. Validate JSON: Use online JSON validator or `python -m json.tool storage/manifest.json`
3. If corrupted, restore from backup or delete to start fresh
4. Ensure no concurrent sync operations

### Debug Mode

Enable verbose output (in development):

```python
# In commands/sync.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Checking Logs

Artifacts are saved after each run:

```bash
# In GitHub Actions
- View workflow runs at: https://github.com/org/repo/actions
- Download artifacts from workflow summary

# Locally
- Check workspace/downloads/ for ZIP files
- Check storage/manifest.json for version state
```

---

## Contributing

### Contribution Guidelines

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature`
3. **Implement** changes with tests
4. **Follow** code style: Python PEP 8
5. **Update** README.md if needed
6. **Commit** with descriptive messages
7. **Push** to your fork
8. **Create** Pull Request with description

### Code Style

- **Python**: PEP 8 (autopep8 friendly)
- **Naming**: `snake_case` for functions, `CamelCase` for classes
- **Docstrings**: Google style
- **Type Hints**: Use `from __future__ import annotations` and type all function signatures

### Testing Requirements

- Unit tests for new services
- Integration tests for workflows
- Test coverage: Minimum 80%

### Documentation

- Update README.md for new features
- Add docstrings to all public methods
- Include examples for new CLI commands
- Document new environment variables

---

## License

[Add your license here - e.g., MIT, Apache 2.0]

---

## Contact & Support

- **Issues**: https://github.com/jeevan-incture/sap-integration-devops/issues
- **Discussions**: https://github.com/jeevan-incture/sap-integration-devops/discussions
- **Email**: [your-email@example.com]

---

## Version History

### v1.0.0 (2026-06-27)
- Initial release
- Core sync functionality
- JSON/CSV configuration support
- GitHub Actions integration
- Rich terminal UI

---

**Last Updated**: June 27, 2026  
**Maintained By**: SAP DevOps Team  
**Status**: Active Development
