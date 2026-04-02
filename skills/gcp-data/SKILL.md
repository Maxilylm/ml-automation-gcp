---
name: gcp-data
description: "Manage Cloud Storage data for ML workflows: upload, download, catalog datasets, and create buckets."
aliases: [gcs data, cloud storage, gcs upload, gcs download, gcs catalog]
extends: ml-automation
user_invocable: true
---

# GCP Data

Manage Cloud Storage data for ML pipelines. Upload and download files with resumable transfers, catalog datasets by format and size, create buckets with lifecycle rules, and validate data integrity post-transfer.

## When to Use

- You need to upload local training data to a GCS bucket before launching a Vertex AI training job.
- You want to download model artifacts or prediction results from Cloud Storage to your local machine.
- You need to catalog all ML datasets in a bucket (listing formats, sizes, and last-modified dates).
- You want to create a new bucket with region and lifecycle configuration for a new ML project.

## Workflow

1. **Env Check** -- Validate GCP credentials and confirm Cloud Storage API access for the target project.
2. **Action Execution** -- Execute the requested data operation:
   - **upload** -- Transfer local files or directories to the specified GCS path with resumable upload and integrity verification.
   - **download** -- Pull objects or prefixes from GCS to a local destination with parallel transfer.
   - **catalog** -- List objects under a bucket or prefix, summarize by file type, total size, and freshness.
   - **create-bucket** -- Create a new bucket with specified region, storage class, and lifecycle rules.

## Report Bus Integration

Writes `gcp-data_report.json` with action performed, GCS URIs, transfer sizes, and integrity status. The `gcp-data-engineer` agent executes all data operations.

## Full Specification

Usage: `/gcp-data <action> [--bucket <bucket>] [--path <gcs_path>]`

See `commands/gcp-data.md` for the complete workflow.
