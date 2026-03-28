# ml-automation-gcp

Google Cloud ML platform extension for [ml-automation](https://github.com/Maxilylm/ml-automation-core).

## Prerequisites

- [ml-automation](https://github.com/Maxilylm/ml-automation-core) core plugin (>= v1.8.0)
- Claude Code CLI
- Google Cloud SDK (`gcloud` CLI) installed and configured
- GCP project with billing enabled

## Installation

```bash
claude plugin add /path/to/ml-automation-gcp
```

## What's Included

### Agents

| Agent | Purpose | Hooks Into |
|---|---|---|
| `gcp-ml-engineer` | Vertex AI training, AutoML, custom jobs, model registry, pipelines | `before-deploy` |
| `gcp-data-engineer` | BigQuery, Cloud Storage, Dataflow, BigQuery ML | `after-init` |
| `gcp-deployer` | Deploy to Vertex AI endpoints, Cloud Run, Cloud Functions | *(direct invocation)* |
| `gcp-reviewer` | GCP cost optimization, IAM security, best practices review | `after-evaluation` |

### Commands

| Command | Purpose |
|---|---|
| `/gcp-connect` | Configure GCP credentials and validate project access |
| `/gcp-coldstart` | Full GCP ML workflow (BigQuery -> Vertex AI -> deploy) |
| `/gcp-train` | Train on Vertex AI (AutoML, custom training, hyperparameter tuning) |
| `/gcp-deploy` | Deploy to Vertex AI endpoint, Cloud Run, or Cloud Functions |
| `/gcp-bigquery` | Generate and execute BigQuery SQL / BigQuery ML |
| `/gcp-data` | Manage Cloud Storage data (upload, download, catalog) |
| `/gcp-status` | Check GCP resources (endpoints, training jobs, datasets, costs) |

## Getting Started

```bash
# Configure GCP credentials
/gcp-connect --project my-ml-project --region us-central1

# Full end-to-end workflow
/gcp-coldstart my_project.my_dataset.training_table --target label --deploy

# Train on Vertex AI
/gcp-train gs://my-bucket/data/train.csv --method automl --task classification --budget 2

# Deploy a model
/gcp-deploy --model projects/123/locations/us-central1/models/456 --target vertex

# Run BigQuery ML
/gcp-bigquery "predict churn for customers" --dataset my_dataset --mode bqml

# Manage Cloud Storage data
/gcp-data upload --local ./data/train.csv --bucket my-ml-bucket --path data/train.csv

# Check resource status
/gcp-status --resource all
```

## How It Integrates

When installed alongside the core plugin:

1. **Automatic routing** -- Tasks mentioning Vertex AI, BigQuery, Cloud Storage, or GCP deployment are routed to GCP agents
2. **Core workflow hooks** -- When running `/team-coldstart`:
   - `gcp-data-engineer` fires at `after-init` to detect and catalog BigQuery/GCS data sources
   - `gcp-ml-engineer` fires at `before-deploy` to configure Vertex AI training
   - `gcp-reviewer` fires at `after-evaluation` to review cost and security
3. **Core agent reuse** -- Commands use eda-analyst, developer, ml-theory-advisor from core

## License

MIT
