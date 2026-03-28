---
name: gcp-coldstart
description: "Full GCP ML workflow from BigQuery data through Vertex AI training to endpoint deployment with evaluation."
aliases: [gcp workflow, gcp end to end, vertex workflow, gcp ml pipeline]
extends: ml-automation
user_invocable: true
---

# GCP Coldstart

End-to-end GCP ML workflow. Profiles data in BigQuery or Cloud Storage, engineers features, selects training approach (BigQuery ML, AutoML, or custom Vertex AI training), trains and evaluates the model, and optionally deploys to a Vertex AI endpoint.

## Full Specification

See `commands/gcp-coldstart.md` for the complete workflow.
