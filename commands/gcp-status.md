# /gcp-status

Check GCP ML resource status: Vertex AI endpoints, training jobs, BigQuery datasets, and costs.

## Usage

```
/gcp-status [--resource all|vertex|bigquery|storage|costs] [--project <project_id>] [--region <region>]
```

- `--resource`: resource type to check (default: `all`)
- `--project`: GCP project ID (default: current project)
- `--region`: region filter (default: all regions)

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` -- if missing, copy from core plugin
2. Check if `gcp_utils.py` exists in `src/` -- if missing, copy from this plugin's `templates/gcp_utils.py`
3. Verify GCP credentials and project access

### Stage 1: Vertex AI Status

1. **Endpoints**:
   - List all endpoints with deployed models
   - For each: endpoint ID, display name, model count, traffic split
   - Machine type, replica count, last prediction time
2. **Training Jobs**:
   - List recent training jobs (last 30 days)
   - For each: job ID, state, create time, duration, machine type
   - Active jobs: progress percentage, estimated completion
3. **Models**:
   - List models in Model Registry
   - For each: model ID, display name, version count, last update
4. **Pipelines**:
   - List recent pipeline runs
   - For each: pipeline ID, state, create time, duration

### Stage 2: BigQuery Status

1. **Datasets**:
   - List datasets with table counts
   - For each dataset: table count, total size, last modified
2. **Recent Jobs**:
   - List recent query jobs (last 7 days)
   - Total bytes processed, estimated cost
3. **BQML Models**:
   - List BigQuery ML models
   - For each: model type, training state, last trained
4. **Reservations** (if applicable):
   - Slot usage and capacity

### Stage 3: Cloud Storage Status

1. **Buckets**:
   - List buckets with storage class and region
   - For each: object count, total size, lifecycle rules
2. **ML Data Assets**:
   - Identify ML-related data (training data, model artifacts, predictions)
   - Summarize by category

### Stage 4: Cost Summary

1. Query billing data (if accessible):
   - Current month spend by service (Vertex AI, BigQuery, Cloud Storage)
   - Daily cost trend
   - Top cost drivers
2. Estimate monthly projected cost
3. Identify cost optimization opportunities:
   - Unused endpoints (no recent predictions)
   - Oversized machine types
   - Unoptimized BigQuery queries (full table scans)
   - Storage lifecycle improvements

### Stage 5: Status Report

```python
from ml_utils import save_agent_report
save_agent_report("gcp-status", {
    "status": "completed",
    "project_id": project_id,
    "vertex_ai": {
        "endpoints": endpoints_summary,
        "training_jobs": jobs_summary,
        "models": models_summary,
        "pipelines": pipelines_summary
    },
    "bigquery": {
        "datasets": datasets_summary,
        "recent_cost": bq_cost,
        "bqml_models": bqml_summary
    },
    "storage": {
        "buckets": buckets_summary,
        "total_size": total_storage_size
    },
    "costs": {
        "current_month": current_month_cost,
        "projected": projected_cost,
        "optimizations": cost_optimizations
    }
})
```

Print status dashboard with resource tables and cost summary.
