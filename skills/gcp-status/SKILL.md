---
name: gcp-status
description: "Check GCP ML resource status: Vertex AI endpoints, training jobs, BigQuery datasets, storage, and cost summary."
aliases: [gcp resources, vertex status, gcp cost, gcp check, gcp dashboard]
extends: spark
user_invocable: true
---

# GCP Status

Check the status of all GCP ML resources. Lists Vertex AI endpoints, training jobs, models, and pipelines. Summarizes BigQuery datasets, recent query costs, and BQML models. Reports Cloud Storage buckets and ML data assets. Provides cost summary with optimization recommendations.

## When to Use

- You want a quick overview of all ML resources currently active in your GCP project.
- You need to check whether a training job or endpoint deployment has completed or failed.
- You want to review recent BigQuery query costs and identify optimization opportunities.
- You need a cost summary across Vertex AI, BigQuery, and Cloud Storage to manage your ML budget.

## Workflow

1. **Env Check** -- Validate GCP credentials and project configuration.
2. **Vertex AI** -- List endpoints (with deployed models, traffic splits, and replica counts), active and recent training jobs (with status and duration), registered models, and pipeline runs.
3. **BigQuery** -- List datasets and tables with row counts and sizes, summarize recent query jobs with bytes processed and cost, and list any BQML models with their evaluation metrics.
4. **Storage** -- List Cloud Storage buckets with region and storage class, summarize ML-related objects (datasets, artifacts, checkpoints) by size and freshness.
5. **Cost Summary** -- Aggregate costs across Vertex AI (training compute, endpoint serving, prediction), BigQuery (query, storage), and Cloud Storage (storage, network). Flag top cost drivers and recommend optimizations.

## Report Bus Integration

Writes `gcp-status_report.json` with per-service resource inventories, cost breakdowns, and optimization recommendations. The `gcp-reviewer` agent compiles the full status report.

## Full Specification

Usage: `/gcp-status [--resource all|vertex|bigquery|storage|costs]`

See `commands/gcp-status.md` for the complete workflow.
