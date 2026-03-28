---
name: gcp-bigquery
description: "Generate and execute BigQuery SQL and BigQuery ML queries from natural language descriptions."
aliases: [bq query, bigquery sql, bqml, bigquery ml, bq ml]
extends: ml-automation
user_invocable: true
---

# GCP BigQuery

Generate and execute BigQuery queries from natural language. Supports standard SQL (analytics, transformations, aggregations) and BigQuery ML (CREATE MODEL, ML.EVALUATE, ML.PREDICT). Estimates query cost before execution, optimizes for partitioning and clustering, and reports results with metrics.

## Full Specification

See `commands/gcp-bigquery.md` for the complete workflow.
