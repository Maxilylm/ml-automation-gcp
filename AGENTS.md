# spark-gcp — Cortex Code Extension

Google Cloud ML platform automation. Vertex AI training, BigQuery ML, Cloud Storage, Cloud Run deployment, and GCP ML infrastructure. Requires spark-core installed.

## Available Agents

| Agent | When to use |
|---|---|
| `gcp-data-engineer` | User wants to work with BigQuery, Cloud Storage, Dataflow, or build GCP data pipelines |
| `gcp-ml-engineer` | User wants to train models on Vertex AI, use BigQuery ML, or run AutoML on GCP |
| `gcp-deployer` | User wants to deploy to Vertex AI endpoints, Cloud Run, or Cloud Functions |
| `gcp-reviewer` | User wants cost optimization, security review, or GCP best practices for ML |

## Available Skills

| Skill | Trigger |
|---|---|
| `/gcp-connect` | "connect to GCP", "configure GCP credentials", "set up Vertex AI project" |
| `/gcp-coldstart` | "full GCP ML workflow", "end to end on GCP", "Vertex AI coldstart" |
| `/gcp-data` | "manage Cloud Storage", "BigQuery table", "Dataflow pipeline", "GCS bucket" |
| `/gcp-bigquery` | "BigQuery ML", "BQML model", "BigQuery query", "analyze in BigQuery" |
| `/gcp-train` | "train on Vertex AI", "Vertex AI training job", "AutoML on GCP", "BigQuery ML model" |
| `/gcp-deploy` | "deploy to Vertex AI", "Cloud Run deployment", "Cloud Functions", "GCP endpoint" |
| `/gcp-status` | "GCP resource status", "list Vertex AI jobs", "check Cloud Storage" |

## Routing

- BigQuery, Cloud Storage, Dataflow → `gcp-data-engineer`
- Vertex AI training, BigQuery ML, AutoML → `gcp-ml-engineer`
- Vertex AI endpoints, Cloud Run, Cloud Functions → `gcp-deployer`
- Cost, security, best practices → `gcp-reviewer`
- Fallback → spark-core orchestrator
