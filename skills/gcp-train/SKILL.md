---
name: gcp-train
description: "Train ML models on Vertex AI with AutoML, custom training jobs, or hyperparameter tuning via Vizier."
aliases: [vertex train, automl train, gcp training, vertex ai training, hpt]
extends: ml-automation
user_invocable: true
---

# GCP Train

Train ML models on Vertex AI. Supports AutoML (tabular, image, text), custom training with pre-built or custom containers, and hyperparameter tuning via Vertex AI Vizier. Monitors training progress, evaluates results, and reports metrics with cost breakdown.

## When to Use

- You have data ready in GCS or BigQuery and want to train a model on Vertex AI without managing infrastructure.
- You want to compare AutoML against a custom training script to find the best approach for your task.
- You need hyperparameter tuning (HPT) with Vizier to optimize model performance automatically.
- You want a training job that tracks metrics, logs artifacts to GCS, and registers the resulting model in the Vertex AI Model Registry.

## Workflow

1. **Env Check** -- Validate GCP credentials, confirm Vertex AI API is enabled, and verify the data source is accessible.
2. **Data Prep** -- Resolve the data source (GCS URI, BigQuery table, or local path to upload). Validate schema compatibility with the chosen training method and task type.
3. **Training** -- Launch the training job based on the selected method:
   - **AutoML** -- Submit an AutoML training job for the specified task type (classification, regression, forecasting) with budget and optimization objective.
   - **Custom** -- Create a custom training job with the specified container, machine type, and optional GPU accelerators. Stream logs during training.
   - **HPT** -- Configure a hyperparameter tuning job via Vizier with search space, metric, and trial budget. Run parallel trials and select the best configuration.

## Report Bus Integration

Writes `gcp-train_report.json` with job ID, training method, model metrics, artifact URI, training duration, and cost estimate. The `gcp-ml-engineer` agent manages the full training lifecycle.

## Full Specification

Usage: `/gcp-train <data_source> [--method automl|custom|hpt] [--task classification|regression|forecasting]`

See `commands/gcp-train.md` for the complete workflow.
