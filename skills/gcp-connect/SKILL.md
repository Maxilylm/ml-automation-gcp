---
name: gcp-connect
description: "Configure GCP credentials, project settings, and validate API access for Google Cloud ML workflows."
aliases: [gcp auth, gcp credentials, gcp project, gcp setup, google cloud connect]
extends: ml-automation
user_invocable: true
---

# GCP Connect

Configure GCP authentication and project settings. Detects existing credentials (service account, application default, gcloud CLI), validates project access, checks enabled APIs (Vertex AI, BigQuery, Cloud Storage, Cloud Run), and reports IAM permissions.

## Full Specification

See `commands/gcp-connect.md` for the complete workflow.
