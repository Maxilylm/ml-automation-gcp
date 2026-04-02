---
name: gcp-coldstart
description: "Full GCP ML workflow from BigQuery data through Vertex AI training to endpoint deployment with evaluation."
aliases: [gcp workflow, gcp end to end, vertex workflow, gcp ml pipeline]
extends: ml-automation
user_invocable: true
---

# GCP Coldstart

End-to-end GCP ML workflow. Profiles data in BigQuery or Cloud Storage, engineers features, selects the best training approach (BigQuery ML, AutoML, or custom Vertex AI training), trains and evaluates the model, and optionally deploys to a Vertex AI endpoint -- all from a single command.

## When to Use

- You have a dataset in GCS or BigQuery and want a trained, evaluated model on Vertex AI with minimal setup.
- You need an end-to-end pipeline that handles data profiling, feature engineering, training, and deployment in one run.
- You want to compare AutoML vs. custom training approaches and pick the best performer automatically.
- You need a production-ready Vertex AI endpoint with traffic configuration and test predictions.

## Workflow

1. **Env Check** -- Validate GCP credentials, project configuration, and required API enablement (Vertex AI, BigQuery, Cloud Storage).
2. **Data Profiling** -- Detect schema, distributions, missing values, class balance, and target-column suitability via BigQuery or local pandas analysis.
3. **Vertex AI Training** -- Select training strategy (BigQuery ML for tabular quick-wins, AutoML for zero-code, or custom Vertex AI training jobs), configure compute resources, and launch the training run.
4. **Evaluation** -- Retrieve model metrics (accuracy, AUC, RMSE, etc.), compare against baseline thresholds, and generate an evaluation summary.
5. **Deploy** -- (when `--deploy` is passed) Create or reuse a Vertex AI endpoint, deploy the winning model with autoscaling and traffic splitting, and validate with a test prediction.

## Report Bus Integration

Writes `gcp-coldstart_report.json` containing stage outcomes, model metrics, endpoint URI, and cost summary. Agents `gcp-data-engineer`, `gcp-ml-engineer`, and `gcp-deployer` each publish their own reports consumed by downstream stages.

## Full Specification

Usage: `/gcp-coldstart <dataset> [--target <col>] [--task classification|regression|forecasting] [--deploy]`

See `commands/gcp-coldstart.md` for the complete workflow.
