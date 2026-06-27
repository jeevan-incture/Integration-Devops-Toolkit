# 🚀 GitHub Actions POC - SAP Integration Flow Sync

## Overview

This POC (Proof of Concept) workflow demonstrates automated synchronization of SAP Integration Flows to GitHub with persistent manifest tracking.

**Workflow File**: `.github/workflows/sync-poc.yml`

---

## Key Features

✅ **Manual Trigger**: Run on-demand with optional package parameter  
✅ **Scheduled Execution**: Daily at 2 AM UTC  
✅ **Package Support**: Default to CICDAutomation, customizable  
✅ **Manifest Persistence**: Stores at `.sap-devops/storage/manifest.json`  
✅ **Git Automation**: Auto-commits and pushes manifest changes  
✅ **Artifact Storage**: Saves ZIPs and manifest for 7 days  
✅ **Error Handling**: Validates secrets, handles push failures gracefully  
✅ **Visibility**: Detailed logging and workflow summary  

---

## Setup Instructions

### 1. Add GitHub Repository Secrets

Go to **Settings → Secrets and variables → Actions** and add these secrets:

| Secret Name | Value | Example |
|---|---|---|
| `BTP_BASE_URL` | SAP BTP instance URL | `https://inccpidev.it-cpi001.cfapps.eu10.hana.ondemand.com` |
| `BTP_TOKEN_URL` | OAuth token endpoint | `https://inccpidev.authentication.eu10.hana.ondemand.com/oauth/token` |
| `BTP_CLIENT_ID` | Service account ID | `sb-28bf8e67-9030-456e-9152-b1cb433c2b4f!b63626\|it!b16077` |
| `BTP_CLIENT_SECRET` | Service account secret | `21d76727-efd4-499c-ab84-7cdf088e93b2$IgvdYL0OkQmv0...` |
| `GIT_REPOSITORY_URL` | GitHub repo HTTPS URL | `https://github.com/org/repo.git` |
| `GIT_GITHUB_TOKEN` | GitHub Personal Access Token | `ghp_xxxxxxxxxxxx` |

**⚠️ Important**: GitHub automatically provides `GITHUB_TOKEN` for the action; don't add it as a secret.

### 2. Ensure Package Configuration Exists

Make sure `config/packages.json` includes CICDAutomation:

```json
[
  {
    "id": "CICDAutomation",
    "name": "CICD Automation Package",
    "description": "Integration flows for CICD automation"
  }
]
```

### 3. Commit Workflow File

```bash
git add .github/workflows/sync-poc.yml
git commit -m "chore: Add GitHub Actions POC workflow"
git push origin main
```

### 4. Verify Workflow

1. Go to **Actions** tab in GitHub
2. Select **SAP Integration Flow Sync (POC)**
3. Confirm workflow appears

---

## Triggers

### Manual Trigger (Recommended for Testing)

1. Go to **Actions → SAP Integration Flow Sync (POC)**
2. Click **Run workflow**
3. (Optional) Enter custom package ID
4. Click **Run workflow** button

```bash
# Or use GitHub CLI:
gh workflow run sync-poc.yml -f package_id=CICDAutomation
```

### Scheduled Trigger

Runs automatically every day at **2 AM UTC**:

```yaml
schedule:
  - cron: '0 2 * * *'
```

To change time, edit `.github/workflows/sync-poc.yml`:
```yaml
schedule:
  - cron: '0 6 * * *'  # 6 AM UTC instead
```

---

## Workflow Steps

### Step 1: Checkout Repository
- Clones your repository with full history
- Allows workflow to read/write files

### Step 2-4: Setup Environment
- Installs Python 3.11
- Verifies Git is available
- Installs Python dependencies from `requirements.txt`

### Step 5: Configure Git User
- Sets committer identity for automatic commits
- Uses `github-actions[bot]` as author

### Step 6: Setup Storage Directory
- Creates `.sap-devops/storage/` directory
- Creates `workspace/downloads/` for artifacts
- Ensures proper file structure exists

### Step 7: Validate Secrets
- Checks all required environment variables are set
- Fails early if secrets are missing
- Prevents runtime errors

### Step 8: Create Environment File
- Generates `.env` from GitHub Secrets
- Sets manifest path to `.sap-devops/storage/manifest.json`
- Keeps credentials out of version control

### Step 9: Run Sync Command
- Executes Python sync with CICDAutomation package
- Uses JSON configuration format
- Handles errors with proper logging

### Step 10: Verify Manifest
- Checks if manifest was created/updated
- Displays manifest content in logs
- Validates manifest structure

### Step 11: Commit Manifest Changes
- Stages `.sap-devops/storage/manifest.json`
- Commits with descriptive message
- Includes workflow URL and timestamp

### Step 12: Push to Repository
- Pushes manifest commit to main branch
- Gracefully handles no-change scenarios

### Step 13: Upload Artifacts
- Saves downloaded ZIPs to GitHub Artifacts
- Saves manifest.json for inspection
- Retains for 7 days

### Step 14: Display Summary
- Shows success message
- Lists key information
- Displays manifest state

### Step 15: Error Notification
- Shows error if workflow fails
- Provides error context for debugging

---

## Manifest Persistence

### Directory Structure

```
your-repo/
├── .sap-devops/                    # New POC-specific directory
│   └── storage/
│       └── manifest.json           # Persisted version tracking
├── .github/
│   └── workflows/
│       └── sync-poc.yml            # This workflow
└── repository/                     # Local GitHub repo clone
    └── packages/
        └── CICDAutomation/
            ├── IF_Automation_Test.zip
            └── IF_Automation_Test2.zip
```

### Manifest Tracking

**File**: `.sap-devops/storage/manifest.json`

**Format**:
```json
{
  "IF_Automation_Test": {
    "package": "CICDAutomation",
    "name": "IF_Automation_Test",
    "version": "1.0.2",
    "last_synced": "2026-06-27T02:00:00.000000+00:00"
  }
}
```

**Benefits**:
- Tracked in Git (version control)
- Survives workflow runs (persisted across executions)
- Enables differential syncs (only changed flows sync)
- Audit trail (see all sync history in Git commits)

---

## Commit Messages

Auto-generated commit messages follow pattern:

```
🔄 sync(manifest): Update integration flows manifest

Package: CICDAutomation
Timestamp: 2026-06-27T02:00:00Z
Workflow: https://github.com/org/repo/actions/runs/123456789
```

### Viewing Commit History

```bash
# See all sync commits
git log --oneline --grep="sync(manifest)"

# See manifest changes
git log -p .sap-devops/storage/manifest.json
```

---

## Artifacts

After each workflow run, artifacts are saved:

**Location**: **Actions** tab → Run → **Artifacts** section

**Included**:
- `sync-artifacts-{RUN_NUMBER}/workspace/downloads/` - Downloaded ZIP files
- `sync-artifacts-{RUN_NUMBER}/.sap-devops/storage/manifest.json` - Manifest snapshot
- `sync-artifacts-{RUN_NUMBER}/.env` - Environment config (sanitized secrets)

**Retention**: 7 days

**Download**:
```bash
gh run download {RUN_ID} -n sync-artifacts-{NUMBER}
```

---

## Monitoring & Debugging

### View Workflow Runs

1. Go to **Actions** tab
2. Select **SAP Integration Flow Sync (POC)**
3. Click on run to see details

### View Logs

In workflow run details:
- **Setup Python**: Python version and cache info
- **Install Dependencies**: Package versions
- **Create Environment**: Confirms .env created
- **Run Sync**: Full sync output with progress
- **Verify Manifest**: Manifest JSON content
- **Commit/Push**: Git operations status

### Common Issues

#### Issue: "Secrets not configured"

**Error**: `BTP_BASE_URL not set`

**Solution**: 
1. Go to Settings → Secrets and variables → Actions
2. Add all 6 required secrets
3. Re-run workflow

#### Issue: "Push failed"

**Error**: `fatal: could not read Username`

**Solution**:
1. Verify `GIT_GITHUB_TOKEN` has `repo` scope
2. Check token hasn't expired
3. Ensure repo is not archived/readonly

#### Issue: "Manifest not created"

**Error**: `Manifest file not found`

**Solution**:
1. Check sync step completed successfully
2. Verify `config/packages.json` has CICDAutomation
3. Check SAP credentials in secrets are valid

---

## Testing the POC

### Test 1: Manual Trigger with Default Package

1. Go to **Actions → SAP Integration Flow Sync (POC)**
2. Click **Run workflow**
3. Leave package_id empty
4. Click **Run workflow**
5. Wait for completion
6. Check manifest at `.sap-devops/storage/manifest.json`

**Expected**: 
- Manifest created/updated
- Commit pushed to main
- Artifacts saved

### Test 2: Custom Package

1. Go to **Actions → SAP Integration Flow Sync (POC)**
2. Click **Run workflow**
3. Enter custom package (if it exists in config)
4. Click **Run workflow**

**Expected**:
- Syncs only that package
- Manifest persists
- Commit message includes package name

### Test 3: Scheduled Execution

1. Wait until 2 AM UTC
2. Check **Actions** tab
3. Confirm **SAP Integration Flow Sync (POC)** ran automatically

**Expected**:
- Workflow triggered at scheduled time
- Manifest updated if changes exist
- No manual intervention needed

### Test 4: No Changes (Idempotency)

1. Run workflow twice without SAP changes
2. Second run should show "No changes to commit"
3. Manifest should not be updated

**Expected**:
- First run: Manifest committed
- Second run: "ℹ️ No changes to commit" message
- No unnecessary commits

---

## Environment Variables in Workflow

The workflow creates `.env` with these values:

```env
# SAP BTP Configuration
BTP_BASE_URL=<from secret>
BTP_TOKEN_URL=<from secret>
BTP_CLIENT_ID=<from secret>
BTP_CLIENT_SECRET=<from secret>

# GitHub Configuration
GIT_REPOSITORY_URL=<from secret>
GITHUB_TOKEN=<from secret>
GIT_BRANCH=main

# Manifest Persistence (KEY FOR POC)
MANIFEST_PATH=.sap-devops/storage/manifest.json
PACKAGES_CONFIG_JSON=config/packages.json
PACKAGES_CONFIG_CSV=config/packages.csv
REPOSITORY_PATH=repository
WORKSPACE_PATH=workspace
```

**Key Setting**:
```env
MANIFEST_PATH=.sap-devops/storage/manifest.json
```
This ensures manifest persists in repository directory.

---

## Security Considerations

### Secrets Handling

✅ **Good Practices**:
- Secrets are never logged (GitHub masks them)
- Secrets only used in environment variables
- `.env` file created but NOT committed
- Workflow files don't contain credentials

⚠️ **Important**:
- Add `.env` to `.gitignore`
- Never print secrets in logs
- Rotate tokens periodically
- Review secret access in settings

### Permissions

Current permissions:
```yaml
permissions:
  contents: write      # Can read/write repository files
  actions: read        # Can read workflow info
```

This allows:
- Reading repository files
- Creating commits
- Pushing to main branch
- Accessing workflow artifacts

---

## Next Steps / Extensions

### Phase 2 Enhancements

- [ ] **Notification**: Slack/email on success/failure
- [ ] **Status Badge**: Add workflow status badge to README
- [ ] **Approval Gate**: Require approval before pushing manifest
- [ ] **Multiple Packages**: Sync all packages in parallel
- [ ] **Branch Strategy**: Create PR instead of direct push
- [ ] **Conflict Detection**: Alert if Git and SAP modified same flow
- [ ] **Database Logging**: Store metrics in external database
- [ ] **Dashboard**: Visualize sync history and statistics

### Example: Slack Notification

```yaml
- name: 📢 Notify Slack
  if: always()
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "SAP Sync ${{ job.status }}: CICDAutomation",
        "blocks": [...]
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

---

## Troubleshooting Commands

### Check Workflow Status

```bash
# List recent runs
gh run list -w sync-poc.yml --limit 10

# Show latest run details
gh run view --log -w sync-poc.yml
```

### View Manifest in Repository

```bash
# Check manifest exists
git ls-tree -r main -- .sap-devops/

# See manifest history
git log --oneline .sap-devops/storage/manifest.json

# Show manifest at specific commit
git show COMMIT:.sap-devops/storage/manifest.json
```

### Manual Sync (Local Testing)

```bash
# Setup
export BTP_BASE_URL="..."
export BTP_TOKEN_URL="..."
export BTP_CLIENT_ID="..."
export BTP_CLIENT_SECRET="..."
export GIT_REPOSITORY_URL="..."
export GITHUB_TOKEN="..."
export MANIFEST_PATH=".sap-devops/storage/manifest.json"

# Run
python -c "from commands.sync import run; run('json', 'CICDAutomation')"
```

---

## FAQ

**Q: Why use `.sap-devops/` directory?**  
A: Isolates POC-specific data, allows coexistence with other solutions.

**Q: Will manifest changes break existing repos?**  
A: No. Existing manifest at `storage/manifest.json` still works. POC creates new one at `.sap-devops/`.

**Q: Can I sync multiple packages?**  
A: Current POC syncs one package. Future: parallel jobs for each package.

**Q: What if workflow fails mid-sync?**  
A: Manifest is only updated on success, so no partial state is recorded.

**Q: Can I disable scheduled trigger?**  
A: Yes, comment out or remove the `schedule:` section in workflow.

**Q: How do I see previous manifests?**  
A: Use Git history: `git log -p .sap-devops/storage/manifest.json`

---

## Support

For issues:
1. Check **Actions** logs for error messages
2. Verify all secrets are configured
3. Check SAP BTP credentials are valid
4. Ensure `config/packages.json` has correct packages
5. Review workflow file for syntax errors
6. Check `.gitignore` includes `.env`

---

**Created**: June 27, 2026  
**Status**: Proof of Concept (Testing Phase)  
**Tested With**: Python 3.11, Ubuntu Latest
