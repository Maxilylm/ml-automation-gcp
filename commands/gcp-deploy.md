# /gcp-deploy

Deploy ML models to Vertex AI endpoints, Cloud Run, or Cloud Functions.

## Usage

```
/gcp-deploy [--model <model_id_or_path>] [--target vertex|cloudrun|functions] [--endpoint <endpoint_id>] [--traffic <percent>] [--machine-type <type>]
```

- `--model`: Vertex AI model ID, GCS model path, or local model directory
- `--target`: deployment target (default: `vertex`)
- `--endpoint`: existing endpoint ID for traffic splitting (creates new if omitted)
- `--traffic`: traffic percentage for this model version (default: 100)
- `--machine-type`: serving machine type (default: `n1-standard-4`)

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` -- if missing, copy from core plugin
2. Check if `gcp_utils.py` exists in `src/` -- if missing, copy from this plugin's `templates/gcp_utils.py`
3. Verify GCP credentials and required APIs enabled
4. Verify model exists and is accessible

### Stage 1: Model Preparation

1. Locate model artifacts:
   - If Vertex AI model ID: verify in Model Registry
   - If GCS path: verify model files exist
   - If local path: upload to GCS staging bucket
2. Determine serving container:
   - Auto-detect framework (TensorFlow, PyTorch, Scikit-learn, XGBoost)
   - Select pre-built serving container
   - Or use custom container if Dockerfile present
3. Report: model location, framework, container image

### Stage 2: Deployment

1. **Vertex AI Endpoint** (`--target vertex`):
   - Create endpoint (or use existing via `--endpoint`)
   - Deploy model with traffic split
   - Configure autoscaling (min: 1, max: 5, target CPU: 60%)
   - Enable request logging
   - Report: endpoint ID, deployed model ID, endpoint URL

2. **Cloud Run** (`--target cloudrun`):
   - Build serving container (FastAPI/Flask wrapper)
   - Push to Artifact Registry
   - Deploy Cloud Run service
   - Configure concurrency, memory, CPU
   - Set up IAM for access control
   - Report: service URL, container image, resource config

3. **Cloud Functions** (`--target functions`):
   - Generate function code with model loading
   - Deploy HTTP-triggered function
   - Configure memory and timeout
   - Report: function URL, trigger type, resource config

### Stage 3: Validation

1. Send test prediction request to deployed endpoint
2. Verify response format and latency
3. Check health endpoint (Cloud Run) or model health (Vertex)
4. Report: test prediction result, latency, health status

### Stage 4: Monitoring Setup

1. Configure Vertex AI Model Monitoring (if Vertex endpoint):
   - Prediction drift detection
   - Feature skew detection
   - Alert thresholds
2. Create Cloud Monitoring dashboard (optional)
3. Report: monitoring configuration, alert policies

### Stage 5: Deployment Report

```python
from ml_utils import save_agent_report
save_agent_report("gcp-deployer", {
    "status": "completed",
    "target": target,
    "model_id": model_id,
    "endpoint_url": endpoint_url,
    "traffic_split": traffic_split,
    "machine_type": machine_type,
    "autoscaling": autoscaling_config,
    "test_prediction": test_result,
    "latency_ms": latency,
    "monitoring": monitoring_config,
    "estimated_monthly_cost": cost_estimate
})
```

Print deployment summary with endpoint URL, resource config, and monitoring status.
