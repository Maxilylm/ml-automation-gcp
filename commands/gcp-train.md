# /gcp-train

Train ML models on Vertex AI with AutoML, custom training, or hyperparameter tuning.

## Usage

```
/gcp-train <data_source> [--method automl|custom|hpt] [--target <column>] [--task classification|regression|forecasting] [--budget <hours>] [--machine-type <type>] [--accelerator <gpu_type>]
```

- `data_source`: BigQuery table or GCS path to training data
- `--method`: training method (default: `automl`)
- `--target`: target column name
- `--task`: ML task type (default: auto-detect)
- `--budget`: AutoML training budget in node-hours (default: 1)
- `--machine-type`: Vertex AI machine type for custom training (default: `n1-standard-4`)
- `--accelerator`: GPU type for custom training (e.g., `NVIDIA_TESLA_T4`)

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` -- if missing, copy from core plugin
2. Check if `gcp_utils.py` exists in `src/` -- if missing, copy from this plugin's `templates/gcp_utils.py`
3. Verify GCP credentials and Vertex AI API enabled
4. Verify data source accessibility

### Stage 1: Data Preparation

1. Load and validate training data schema
2. Check for data quality issues (nulls, class imbalance, data types)
3. If BigQuery source: create Vertex AI managed dataset
4. If GCS source: validate file format, create managed dataset
5. Configure train/validation/test split (default: 80/10/10)
6. Report: dataset stats, split sizes, quality warnings

### Stage 2: Training Configuration

1. **AutoML** (`--method automl`):
   - Configure AutoML Tabular/Image/Text based on data type
   - Set training budget (node-hours)
   - Configure optimization objective (minimize RMSE, maximize AUC, etc.)
   - Enable feature importance explanations

2. **Custom Training** (`--method custom`):
   - Generate training script (`trainer/task.py`)
   - Select pre-built container or configure custom container
   - Configure machine type and accelerator
   - Set up distributed training if needed (worker count, strategy)
   - Configure output directory (`gs://bucket/models/`)

3. **Hyperparameter Tuning** (`--method hpt`):
   - Define search space from training script hyperparameters
   - Configure Vizier study (algorithm, metric, goal)
   - Set max trial count and parallel trial count
   - Configure early stopping

4. Report: training configuration, estimated cost, estimated duration

### Stage 3: Launch Training

1. Submit training job to Vertex AI
2. Monitor job status with polling:
   - Log training metrics as they arrive
   - Report progress percentage
   - Alert on warnings or errors
3. On completion: download training metrics and artifacts
4. Report: final metrics, training duration, actual cost

### Stage 4: Model Evaluation

1. Evaluate trained model on test split
2. Compute task-appropriate metrics
3. Generate evaluation visualizations (confusion matrix, ROC curve, residuals)
4. Compare against baseline
5. Report: evaluation metrics, visualizations, baseline comparison

### Stage 5: Training Report

```python
from ml_utils import save_agent_report
save_agent_report("gcp-train", {
    "status": "completed",
    "method": method,
    "data_source": data_source,
    "task_type": task_type,
    "training_job_id": job_id,
    "training_duration": duration,
    "metrics": metrics,
    "model_uri": model_uri,
    "cost": cost,
    "hyperparameters": best_hyperparameters,
    "recommendations": recommendations
})
```

Print training summary with metrics table and next steps (deploy, tune further, retrain).
