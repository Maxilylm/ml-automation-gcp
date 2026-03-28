---
name: gcp-deploy
description: "Deploy ML models to Vertex AI endpoints, Cloud Run services, or Cloud Functions with traffic splitting and monitoring."
aliases: [vertex deploy, cloud run deploy, gcp serve, gcp endpoint, vertex endpoint]
extends: ml-automation
user_invocable: true
---

# GCP Deploy

Deploy ML models to GCP serving infrastructure. Supports Vertex AI endpoints (with autoscaling and traffic splitting), Cloud Run (containerized serving), and Cloud Functions (lightweight HTTP inference). Validates deployment with test predictions and configures monitoring.

## Full Specification

See `commands/gcp-deploy.md` for the complete workflow.
