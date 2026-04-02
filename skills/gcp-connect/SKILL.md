---
name: gcp-connect
description: "Configure GCP credentials, project settings, and validate API access for Google Cloud ML workflows."
aliases: [gcp auth, gcp credentials, gcp project, gcp setup, google cloud connect]
extends: ml-automation
user_invocable: true
---

# GCP Connect

Configure GCP authentication and project settings. Detects existing credentials (service account, application default, gcloud CLI), validates project access, checks enabled APIs (Vertex AI, BigQuery, Cloud Storage, Cloud Run), and reports IAM permissions.

## When to Use

- You are starting a new GCP ML project and need to verify credentials and API access before running any workload.
- You want to switch to a different GCP project or region for subsequent commands.
- A GCP command failed with an authentication or permissions error and you need to diagnose credential state.
- You need to confirm which APIs are enabled and what IAM roles are available for the active service account.

## Workflow

1. **Env Check** -- Verify that the Google Cloud SDK (`gcloud`) is installed and accessible on PATH.
2. **Credential Detection** -- Probe for credentials in priority order: `GOOGLE_APPLICATION_CREDENTIALS` env var (service account JSON), application default credentials (`gcloud auth application-default`), and active gcloud CLI account. Report credential type, account email, and project ID.
3. **API Validation** -- Query the Service Usage API to confirm that required services (aiplatform, bigquery, storage, cloudfunctions, run) are enabled. List missing APIs with enablement commands. Summarize IAM roles bound to the authenticated principal.

## Report Bus Integration

Writes `gcp-connect_report.json` with credential type, project ID, region, enabled APIs, and IAM role summary. All other GCP commands read this report to skip redundant auth checks.

## Full Specification

Usage: `/gcp-connect [--project <id>] [--region <region>] [--service-account <path>]`

See `commands/gcp-connect.md` for the complete workflow.
