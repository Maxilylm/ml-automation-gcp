# /gcp-bigquery

Generate and execute BigQuery SQL and BigQuery ML queries.

## Usage

```
/gcp-bigquery <task_description> [--dataset <dataset>] [--table <table>] [--mode sql|bqml] [--dry-run]
```

- `task_description`: natural language description of the query or model
- `--dataset`: BigQuery dataset name
- `--table`: BigQuery table name
- `--mode`: `sql` for standard queries, `bqml` for BigQuery ML (default: auto-detect)
- `--dry-run`: generate SQL without executing (estimate cost only)

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` -- if missing, copy from core plugin
2. Check if `gcp_utils.py` exists in `src/` -- if missing, copy from this plugin's `templates/gcp_utils.py`
3. Verify GCP credentials and BigQuery API enabled
4. Verify dataset/table access permissions

### Stage 1: Schema Discovery

1. List available datasets and tables (if not specified)
2. Retrieve table schema: column names, types, descriptions
3. Sample data preview (first 10 rows)
4. Compute table stats: row count, size, last modified, partitioning, clustering
5. Report: schema summary, sample data, table metadata

### Stage 2: Query Generation

1. **SQL Mode** (`--mode sql`):
   - Translate natural language task to BigQuery Standard SQL
   - Apply best practices: avoid `SELECT *`, use partitioning filters, limit scanned data
   - Include cost estimation comment (`-- Estimated bytes: X GB`)
   - Handle complex operations: window functions, CTEs, UNNESTs, JOINs

2. **BigQuery ML Mode** (`--mode bqml`):
   - Select appropriate model type based on task:
     - Classification: `LOGISTIC_REG`, `BOOSTED_TREE_CLASSIFIER`, `DNN_CLASSIFIER`
     - Regression: `LINEAR_REG`, `BOOSTED_TREE_REGRESSOR`, `DNN_REGRESSOR`
     - Clustering: `KMEANS`
     - Forecasting: `ARIMA_PLUS`
     - Recommendation: `MATRIX_FACTORIZATION`
   - Generate `CREATE MODEL` statement with `TRANSFORM` clause
   - Configure model options (max_iterations, learn_rate, l1_reg, l2_reg)
   - Generate evaluation query (`ML.EVALUATE`)
   - Generate prediction query (`ML.PREDICT`)

3. Report: generated SQL, estimated cost, execution plan

### Stage 3: Execution (unless --dry-run)

1. Execute query via BigQuery API
2. Monitor job progress (bytes processed, slot usage)
3. Capture results:
   - SQL: result table or rows
   - BQML: training info, evaluation metrics
4. Report: execution time, bytes processed, actual cost, results preview

### Stage 4: Results Report

```python
from ml_utils import save_agent_report
save_agent_report("gcp-bigquery", {
    "status": "completed",
    "mode": mode,
    "sql": generated_sql,
    "bytes_processed": bytes_processed,
    "execution_time_seconds": exec_time,
    "cost_usd": cost,
    "row_count": result_rows,
    "bqml_metrics": bqml_metrics,
    "recommendations": recommendations
})
```

Print query, cost, and results summary. For BQML: print model metrics table.
