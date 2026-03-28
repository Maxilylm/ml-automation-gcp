# /gcp-connect

Configure GCP credentials and project settings for ML workflows.

## Usage

```
/gcp-connect [--project <project_id>] [--region <region>] [--service-account <path>]
```

- `--project`: GCP project ID (default: detect from `gcloud config`)
- `--region`: default compute region (default: `us-central1`)
- `--service-account`: path to service account JSON key file

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` -- if missing, copy from core plugin (`~/.claude/plugins/*/templates/ml_utils.py`)
2. Check if `gcp_utils.py` exists in `src/` -- if missing, copy from this plugin's `templates/gcp_utils.py`
3. Verify `gcloud` CLI is installed and accessible

### Stage 1: Credential Detection

1. Check for existing credentials in priority order:
   - `--service-account` flag (explicit path)
   - `GOOGLE_APPLICATION_CREDENTIALS` environment variable
   - Application Default Credentials (`gcloud auth application-default print-access-token`)
   - Active `gcloud` config (`gcloud config get-value account`)
2. If no credentials found: guide user through authentication:
   - For interactive: `gcloud auth application-default login`
   - For service account: `gcloud auth activate-service-account --key-file=<path>`
3. Report: credential type, account email, expiry

### Stage 2: Project Configuration

1. Detect or set GCP project:
   - From `--project` flag
   - From `gcloud config get-value project`
   - From `GOOGLE_CLOUD_PROJECT` or `GCLOUD_PROJECT` env vars
2. Verify project access: `gcloud projects describe <project_id>`
3. Set default region: `gcloud config set compute/region <region>`
4. Report: project ID, project name, region, billing status

### Stage 3: Service Validation

1. Check enabled APIs:
   - `aiplatform.googleapis.com` (Vertex AI)
   - `bigquery.googleapis.com` (BigQuery)
   - `storage.googleapis.com` (Cloud Storage)
   - `run.googleapis.com` (Cloud Run)
   - `cloudfunctions.googleapis.com` (Cloud Functions)
2. For disabled APIs: list enable commands but do NOT auto-enable
3. Check IAM permissions for current account on key services
4. Report: enabled APIs, missing APIs with enable commands, IAM summary

### Stage 4: Connection Report

```python
from ml_utils import save_agent_report
save_agent_report("gcp-connect", {
    "status": "completed",
    "credential_type": credential_type,
    "account": account_email,
    "project_id": project_id,
    "project_name": project_name,
    "region": region,
    "enabled_apis": enabled_apis,
    "missing_apis": missing_apis,
    "iam_summary": iam_summary
})
```

Print connection summary table with project, region, credential type, and API status.
