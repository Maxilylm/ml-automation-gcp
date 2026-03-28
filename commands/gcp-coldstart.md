# /gcp-coldstart

Full GCP ML workflow from data in BigQuery through Vertex AI training to deployment.

## Usage

```
/gcp-coldstart <dataset> [--target <column>] [--task classification|regression|forecasting] [--deploy] [--budget <hours>]
```

- `dataset`: BigQuery table (`project.dataset.table`) or GCS path (`gs://bucket/path`)
- `--target`: target column name for supervised learning
- `--task`: ML task type (default: auto-detect)
- `--deploy`: deploy best model to Vertex AI endpoint after training
- `--budget`: AutoML training budget in node-hours (default: 1)

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` -- if missing, copy from core plugin
2. Check if `gcp_utils.py` exists in `src/` -- if missing, copy from this plugin's `templates/gcp_utils.py`
3. Run `/gcp-connect` checks to verify credentials and project access
4. Verify dataset accessibility (BigQuery table exists or GCS path readable)

### Stage 1: Data Profiling

1. If BigQuery source:
   - Run `SELECT * FROM <table> LIMIT 0` to get schema
   - Compute row count, column stats via `APPROX_COUNT_DISTINCT`, `MIN`, `MAX`, `AVG`
   - Sample 1000 rows for profiling
2. If GCS source:
   - Download sample to local, detect format (CSV, Parquet, JSON)
   - Load into pandas for profiling
3. Profile: data types, nulls, cardinality, distributions, target class balance
4. Report: schema, row count, column stats, data quality issues

### Stage 2: Feature Engineering

1. Identify feature types (numeric, categorical, text, datetime)
2. Generate BigQuery SQL for feature transformations:
   - Numeric: standardization, log transforms, binning
   - Categorical: encoding (label, one-hot via CASE WHEN)
   - Datetime: extract components (year, month, day, hour, day_of_week)
   - Text: token count, length features
3. Create feature table in BigQuery: `CREATE TABLE <dataset>.features AS SELECT ...`
4. Report: feature list, transformation SQL, feature table location

### Stage 3: Training Strategy Selection

1. Based on data profile and task type, select training approach:
   - **BigQuery ML** -- for tabular data < 100GB, simple models (linear, boosted trees)
   - **AutoML Tabular** -- for tabular data, when explainability matters
   - **Custom Training** -- for complex architectures or custom frameworks
2. Configure training parameters for selected approach
3. Report: selected approach with rationale, configuration summary

### Stage 4: Model Training

1. If BigQuery ML:
   - Generate and execute `CREATE MODEL` statement
   - Monitor training via `ML.TRAINING_INFO`
   - Evaluate via `ML.EVALUATE`
2. If AutoML:
   - Create Vertex AI TabularDataset from BigQuery or GCS
   - Launch AutoML training job with budget
   - Poll for completion
3. If Custom Training:
   - Generate training script
   - Configure Vertex AI CustomTrainingJob
   - Launch and monitor training
4. Report: training metrics, training time, cost

### Stage 5: Model Evaluation

1. Compute task-appropriate metrics:
   - Classification: accuracy, precision, recall, F1, AUC-ROC, confusion matrix
   - Regression: RMSE, MAE, R-squared, residual analysis
   - Forecasting: MAPE, RMSE, forecast vs actuals plot
2. Feature importance analysis
3. Compare against baseline (majority class, mean prediction)
4. Report: all metrics, feature importance, comparison to baseline

### Stage 6: Deployment (if --deploy)

1. Upload model to Vertex AI Model Registry
2. Create or update Vertex AI endpoint
3. Deploy model to endpoint with default configuration:
   - Machine type: `n1-standard-4`
   - Min replicas: 1, max replicas: 3
   - Traffic: 100% to new model
4. Test endpoint with sample prediction
5. Report: endpoint URL, deployment configuration, sample prediction result

### Stage 7: Final Report

```python
from ml_utils import save_agent_report
save_agent_report("gcp-coldstart", {
    "status": "completed",
    "data_source": dataset,
    "task_type": task_type,
    "training_approach": approach,
    "row_count": row_count,
    "feature_count": feature_count,
    "metrics": metrics,
    "model_id": model_id,
    "endpoint_url": endpoint_url,
    "cost_estimate": cost_estimate,
    "recommendations": recommendations
})
```

Print end-to-end summary with data profile, training results, and deployment status.
