---
name: gcp-deploy
description: "Deploy ML models to Vertex AI endpoints, Cloud Run services, or Cloud Functions with traffic splitting and monitoring."
aliases: [vertex deploy, cloud run deploy, gcp serve, gcp endpoint, vertex endpoint]
extends: spark
user_invocable: true
---

# GCP Deploy

Deploy ML models to GCP serving infrastructure. Supports Vertex AI endpoints (with autoscaling and traffic splitting), Cloud Run (containerized serving), and Cloud Functions (lightweight HTTP inference). Validates deployment with test predictions and configures monitoring.

## When to Use

- You have a trained model in the Vertex AI Model Registry or a model artifact in GCS and need a live prediction endpoint.
- You want to deploy a containerized model to Cloud Run for cost-efficient, scale-to-zero serving.
- You need a lightweight Cloud Function endpoint for simple inference workloads.
- You want to perform a canary or blue-green deployment by splitting traffic between model versions on a Vertex AI endpoint.

## Workflow

1. **Env Check** -- Validate GCP credentials and confirm the target deployment service API is enabled (Vertex AI, Cloud Run, or Cloud Functions).
2. **Model Prep** -- Locate the model by ID, resource name, or GCS artifact path. Verify the model is compatible with the target deployment platform and resolve container image if needed.
3. **Deployment** -- Deploy to the selected target:
   - **Vertex AI** -- Create or reuse an endpoint, deploy the model with specified machine type, replica range, and autoscaling policy.
   - **Cloud Run** -- Build or reference a serving container, deploy as a Cloud Run service with concurrency and memory settings.
   - **Cloud Functions** -- Package the inference handler, deploy as an HTTP function with memory and timeout configuration.
4. **Traffic Config** -- Set the traffic percentage for the newly deployed model (relevant for Vertex AI endpoints with multiple deployed models). Validate with a test prediction request.

## Report Bus Integration

Writes `gcp-deploy_report.json` with endpoint URI, deployed model ID, traffic allocation, test prediction result, and serving cost estimate. The `gcp-deployer` agent manages the full deployment lifecycle.

## Full Specification

Usage: `/gcp-deploy [--model <id_or_path>] [--target vertex|cloudrun|functions] [--traffic <percent>]`

See `commands/gcp-deploy.md` for the complete workflow.
