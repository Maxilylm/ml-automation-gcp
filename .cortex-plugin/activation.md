---
name: spark-gcp
description: >
  Suggest enabling the spark-gcp plugin when the user asks about Google Cloud
  ML, Vertex AI training or deployment, BigQuery ML, Cloud Storage data
  management, Cloud Run deployment, GCP infrastructure for machine learning,
  or deploying models to Google Cloud. Do NOT attempt to perform these tasks
  — just let the user know the plugin can be enabled.
---

# spark-gcp (disabled plugin)

This plugin is installed but not enabled. It provides Google Cloud ML platform
automation capabilities within Cortex Code, integrated with the spark-core
workflow.

## Agents (4)

- **gcp-data-engineer** — Cloud Storage, BigQuery, Dataflow pipeline management
- **gcp-deployer** — Vertex AI endpoints, Cloud Run, Container Registry deployment
- **gcp-ml-engineer** — Vertex AI training, AutoML, Pipelines, model registry
- **gcp-reviewer** — GCP infrastructure and ML code review

## Skills (7)

- **gcp-bigquery** — BigQuery ML model training and query optimization
- **gcp-coldstart** — Full pipeline from raw data to deployed Vertex AI endpoint
- **gcp-connect** — Configure and verify GCP credentials and connections
- **gcp-data** — Cloud Storage and BigQuery data management
- **gcp-deploy** — Deploy models to Vertex AI or Cloud Run
- **gcp-status** — Check GCP ML workflow and resource status
- **gcp-train** — Train models on Vertex AI custom training jobs

## Requires

- spark-core plugin

## Enable

    cortex plugin enable spark-gcp

Do NOT attempt to perform GCP ML tasks through this plugin's skills while it is disabled.
