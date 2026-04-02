---
name: gcp-bigquery
description: "Generate and execute BigQuery SQL and BigQuery ML queries from natural language descriptions."
aliases: [bq query, bigquery sql, bqml, bigquery ml, bq ml]
extends: ml-automation
user_invocable: true
---

# GCP BigQuery

Generate and execute BigQuery queries from natural language. Supports standard SQL (analytics, transformations, aggregations) and BigQuery ML (CREATE MODEL, ML.EVALUATE, ML.PREDICT). Estimates query cost before execution, optimizes for partitioning and clustering, and reports results with metrics.

## When to Use

- You need to explore, transform, or aggregate data that lives in BigQuery without writing SQL by hand.
- You want to train or evaluate a model using BigQuery ML directly inside the data warehouse.
- You need a cost estimate (dry run) before executing an expensive analytical query.
- You want to discover dataset schemas, table sizes, and column statistics before building a pipeline.

## Workflow

1. **Env Check** -- Validate GCP credentials and confirm the BigQuery API is enabled for the active project.
2. **Schema Discovery** -- List datasets and tables in the target project, retrieve column types, partitioning, clustering, and row counts to inform query generation.
3. **Query Generation** -- Translate the natural language task description into BigQuery Standard SQL or BigQuery ML syntax. Apply cost-optimization hints (partition filters, column pruning, LIMIT guards).
4. **Execution** -- Run the query (or dry-run if `--dry-run` is set). Report row count, bytes processed, estimated cost, and result preview.

## Report Bus Integration

Writes `gcp-bigquery_report.json` with the generated SQL, execution stats (rows, bytes, cost), and result sample. The `gcp-data-engineer` agent handles query generation and execution.

## Full Specification

Usage: `/gcp-bigquery <task_description> [--dataset <dataset>] [--mode sql|bqml] [--dry-run]`

See `commands/gcp-bigquery.md` for the complete workflow.
