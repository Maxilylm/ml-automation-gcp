"""
GCP utilities for the ml-automation-gcp extension plugin.

Requires ml_utils.py from the ml-automation core plugin to be present
in the same directory (copied via Stage 0 of GCP commands).
"""

import os
import json
import subprocess
import re
from pathlib import Path


# --- Relevance Detection ---

GCP_INDICATORS = {
    "google.cloud.aiplatform",
    "google.cloud.bigquery",
    "google.cloud.storage",
    "google.cloud.run_v2",
    "google.cloud.functions_v1",
    "vertexai",
    "google.auth",
    "google.oauth2",
}

GCP_MODEL_PATTERNS = [
    r"gs://",
    r"aiplatform\.googleapis\.com",
    r"bigquery\.googleapis\.com",
    r"projects/[^/]+/locations/[^/]+/",
]


def detect_gcp_relevance(project_path="."):
    """Check if project has GCP/Google Cloud indicators for relevance gating.

    Checks: GCP library imports, GCS URIs, service account files,
    BigQuery references, Vertex AI configurations.

    Args:
        project_path: root directory of the project

    Returns:
        dict with 'is_gcp': bool, 'indicators': list of found indicators
    """
    indicators = []
    project = Path(project_path)

    # Check for service account JSON files
    for sa_file in project.glob("**/service-account*.json"):
        try:
            content = json.loads(sa_file.read_text())
            if "type" in content and content["type"] == "service_account":
                indicators.append(f"Service account: {sa_file.name}")
        except (json.JSONDecodeError, PermissionError):
            continue

    # Check GOOGLE_APPLICATION_CREDENTIALS env var
    gac = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if gac and Path(gac).exists():
        indicators.append(f"GOOGLE_APPLICATION_CREDENTIALS set: {Path(gac).name}")

    # Check requirements for GCP packages
    for req_file in ["requirements.txt", "pyproject.toml", "setup.py", "Pipfile"]:
        req_path = project / req_file
        if req_path.exists():
            content = req_path.read_text().lower()
            for pkg in ["google-cloud-aiplatform", "google-cloud-bigquery",
                        "google-cloud-storage", "vertexai"]:
                if pkg in content:
                    indicators.append(f"{pkg} in {req_file}")

    # Check Python files for GCP imports
    py_files = list(project.glob("**/*.py"))[:50]  # limit scan
    for py_file in py_files:
        try:
            content = py_file.read_text()
            for pkg in GCP_INDICATORS:
                if f"import {pkg}" in content or f"from {pkg}" in content:
                    indicators.append(f"{pkg} import in {py_file.name}")
                    break
        except (UnicodeDecodeError, PermissionError):
            continue

    # Check for GCS URIs in any text file
    text_files = list(project.glob("**/*.py")) + list(project.glob("**/*.yaml")) + \
                 list(project.glob("**/*.yml")) + list(project.glob("**/*.json"))
    for tf in text_files[:30]:
        try:
            content = tf.read_text()
            if re.search(r"gs://[a-z0-9]", content):
                indicators.append(f"GCS URI reference in {tf.name}")
                break
        except (UnicodeDecodeError, PermissionError):
            continue

    # Check for BigQuery SQL files
    sql_files = list(project.glob("**/*.sql"))
    for sql_file in sql_files[:10]:
        try:
            content = sql_file.read_text()
            if "#standardSQL" in content or re.search(r"`[^`]+\.[^`]+\.[^`]+`", content):
                indicators.append(f"BigQuery SQL: {sql_file.name}")
        except (UnicodeDecodeError, PermissionError):
            continue

    # Check for Terraform GCP resources
    tf_files = list(project.glob("**/*.tf"))
    for tf_file in tf_files[:10]:
        try:
            content = tf_file.read_text()
            if "google_" in content or 'provider "google"' in content:
                indicators.append(f"Terraform GCP resource in {tf_file.name}")
        except (UnicodeDecodeError, PermissionError):
            continue

    return {
        "is_gcp": len(indicators) > 0,
        "indicators": indicators,
    }


# --- GCP Credentials ---

def get_gcp_credentials():
    """Get current GCP credentials and project information.

    Returns:
        dict with 'authenticated': bool, 'account': str, 'project': str,
        'credential_type': str, 'region': str
    """
    result = {
        "authenticated": False,
        "account": None,
        "project": None,
        "credential_type": None,
        "region": None,
    }

    # Check for service account via env var
    gac = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if gac and Path(gac).exists():
        try:
            sa_data = json.loads(Path(gac).read_text())
            result["authenticated"] = True
            result["account"] = sa_data.get("client_email", "unknown")
            result["project"] = sa_data.get("project_id")
            result["credential_type"] = "service_account"
        except (json.JSONDecodeError, PermissionError):
            pass

    # Fall back to gcloud CLI
    if not result["authenticated"]:
        try:
            account = subprocess.run(
                ["gcloud", "config", "get-value", "account"],
                capture_output=True, text=True, timeout=10
            )
            if account.returncode == 0 and account.stdout.strip():
                result["authenticated"] = True
                result["account"] = account.stdout.strip()
                result["credential_type"] = "gcloud_cli"
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

    # Get project
    if not result["project"]:
        for env_var in ["GOOGLE_CLOUD_PROJECT", "GCLOUD_PROJECT", "GCP_PROJECT"]:
            val = os.environ.get(env_var)
            if val:
                result["project"] = val
                break

    if not result["project"]:
        try:
            proj = subprocess.run(
                ["gcloud", "config", "get-value", "project"],
                capture_output=True, text=True, timeout=10
            )
            if proj.returncode == 0 and proj.stdout.strip():
                result["project"] = proj.stdout.strip()
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

    # Get region
    result["region"] = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")
    try:
        region = subprocess.run(
            ["gcloud", "config", "get-value", "compute/region"],
            capture_output=True, text=True, timeout=10
        )
        if region.returncode == 0 and region.stdout.strip():
            result["region"] = region.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    return result


# --- Cloud Storage ---

def upload_to_gcs(local_path, bucket, gcs_path=None, project=None):
    """Upload a file or directory to Google Cloud Storage.

    Args:
        local_path: local file or directory path
        bucket: GCS bucket name (without gs:// prefix)
        gcs_path: destination path in bucket (default: filename)
        project: GCP project ID (default: from gcloud config)

    Returns:
        dict with 'success': bool, 'gcs_uri': str, 'size_bytes': int, 'message': str
    """
    local = Path(local_path)
    if not local.exists():
        return {"success": False, "gcs_uri": None, "size_bytes": 0,
                "message": f"Local path not found: {local_path}"}

    if gcs_path is None:
        gcs_path = local.name

    gcs_uri = f"gs://{bucket}/{gcs_path}"

    cmd = ["gsutil"]
    if project:
        cmd.extend(["-o", f"GSUtil:default_project_id={project}"])

    if local.is_dir():
        cmd.extend(["-m", "cp", "-r", str(local), gcs_uri])
    else:
        cmd.extend(["cp", str(local), gcs_uri])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            size = local.stat().st_size if local.is_file() else sum(
                f.stat().st_size for f in local.rglob("*") if f.is_file()
            )
            return {"success": True, "gcs_uri": gcs_uri, "size_bytes": size,
                    "message": "Upload completed"}
        else:
            return {"success": False, "gcs_uri": gcs_uri, "size_bytes": 0,
                    "message": f"Upload failed: {result.stderr.strip()}"}
    except subprocess.TimeoutExpired:
        return {"success": False, "gcs_uri": gcs_uri, "size_bytes": 0,
                "message": "Upload timed out after 300 seconds"}
    except FileNotFoundError:
        return {"success": False, "gcs_uri": gcs_uri, "size_bytes": 0,
                "message": "gsutil not found. Install Google Cloud SDK."}


def download_from_gcs(gcs_uri, local_path, project=None):
    """Download a file or prefix from Google Cloud Storage.

    Args:
        gcs_uri: GCS URI (gs://bucket/path)
        local_path: local destination path
        project: GCP project ID (default: from gcloud config)

    Returns:
        dict with 'success': bool, 'local_path': str, 'size_bytes': int, 'message': str
    """
    local = Path(local_path)
    local.parent.mkdir(parents=True, exist_ok=True)

    cmd = ["gsutil"]
    if project:
        cmd.extend(["-o", f"GSUtil:default_project_id={project}"])
    cmd.extend(["-m", "cp", "-r", gcs_uri, str(local)])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            size = local.stat().st_size if local.is_file() else sum(
                f.stat().st_size for f in local.rglob("*") if f.is_file()
            )
            return {"success": True, "local_path": str(local), "size_bytes": size,
                    "message": "Download completed"}
        else:
            return {"success": False, "local_path": str(local), "size_bytes": 0,
                    "message": f"Download failed: {result.stderr.strip()}"}
    except subprocess.TimeoutExpired:
        return {"success": False, "local_path": str(local), "size_bytes": 0,
                "message": "Download timed out after 300 seconds"}
    except FileNotFoundError:
        return {"success": False, "local_path": str(local), "size_bytes": 0,
                "message": "gsutil not found. Install Google Cloud SDK."}


# --- Vertex AI Training ---

def create_vertex_training_job(display_name, script_uri, container_uri,
                                machine_type="n1-standard-4",
                                accelerator_type=None, accelerator_count=0,
                                args=None, project=None, region="us-central1"):
    """Create and submit a Vertex AI custom training job.

    Args:
        display_name: human-readable job name
        script_uri: GCS URI to training script or package
        container_uri: pre-built or custom container image URI
        machine_type: Compute Engine machine type
        accelerator_type: GPU type (e.g., 'NVIDIA_TESLA_T4') or None
        accelerator_count: number of GPUs (0 for CPU-only)
        args: list of command-line arguments for the training script
        project: GCP project ID
        region: GCP region

    Returns:
        dict with 'success': bool, 'job_id': str, 'state': str, 'message': str
    """
    try:
        from google.cloud import aiplatform

        aiplatform.init(project=project, location=region)

        job = aiplatform.CustomJob.from_local_script(
            display_name=display_name,
            script_path=script_uri,
            container_uri=container_uri,
            machine_type=machine_type,
            accelerator_type=accelerator_type,
            accelerator_count=accelerator_count,
            args=args or [],
        )

        job.run(sync=False)

        return {
            "success": True,
            "job_id": job.resource_name,
            "state": str(job.state),
            "message": f"Training job submitted: {display_name}",
        }
    except ImportError:
        return {
            "success": False,
            "job_id": None,
            "state": None,
            "message": "google-cloud-aiplatform not installed. "
                       "Install with: pip install google-cloud-aiplatform",
        }
    except Exception as e:
        return {
            "success": False,
            "job_id": None,
            "state": None,
            "message": f"Training job failed: {str(e)}",
        }


# --- Vertex AI Deployment ---

def deploy_vertex_endpoint(model_id, endpoint_display_name=None,
                           machine_type="n1-standard-4",
                           min_replica_count=1, max_replica_count=3,
                           traffic_percentage=100,
                           project=None, region="us-central1"):
    """Deploy a model to a Vertex AI endpoint.

    Args:
        model_id: Vertex AI model resource name or ID
        endpoint_display_name: display name for new endpoint (None to create auto-named)
        machine_type: serving machine type
        min_replica_count: minimum number of replicas
        max_replica_count: maximum number of replicas
        traffic_percentage: percentage of traffic to route to this model (0-100)
        project: GCP project ID
        region: GCP region

    Returns:
        dict with 'success': bool, 'endpoint_id': str, 'endpoint_url': str,
        'deployed_model_id': str, 'message': str
    """
    try:
        from google.cloud import aiplatform

        aiplatform.init(project=project, location=region)

        # Get model
        model = aiplatform.Model(model_id)

        # Create endpoint
        if endpoint_display_name:
            endpoint = aiplatform.Endpoint.create(
                display_name=endpoint_display_name
            )
        else:
            endpoint = aiplatform.Endpoint.create(
                display_name=f"endpoint-{model.display_name}"
            )

        # Deploy model
        model.deploy(
            endpoint=endpoint,
            machine_type=machine_type,
            min_replica_count=min_replica_count,
            max_replica_count=max_replica_count,
            traffic_percentage=traffic_percentage,
        )

        return {
            "success": True,
            "endpoint_id": endpoint.resource_name,
            "endpoint_url": f"https://{region}-aiplatform.googleapis.com/v1/{endpoint.resource_name}",
            "deployed_model_id": model.resource_name,
            "message": f"Model deployed to endpoint: {endpoint.display_name}",
        }
    except ImportError:
        return {
            "success": False,
            "endpoint_id": None,
            "endpoint_url": None,
            "deployed_model_id": None,
            "message": "google-cloud-aiplatform not installed. "
                       "Install with: pip install google-cloud-aiplatform",
        }
    except Exception as e:
        return {
            "success": False,
            "endpoint_id": None,
            "endpoint_url": None,
            "deployed_model_id": None,
            "message": f"Deployment failed: {str(e)}",
        }


# --- BigQuery ---

def run_bigquery(query, project=None, dry_run=False):
    """Execute a BigQuery SQL query.

    Args:
        query: BigQuery Standard SQL query string
        project: GCP project ID (default: from credentials)
        dry_run: if True, only estimate bytes processed without executing

    Returns:
        dict with 'success': bool, 'rows': list (of dicts), 'total_rows': int,
        'bytes_processed': int, 'cost_usd': float, 'message': str
    """
    try:
        from google.cloud import bigquery

        client = bigquery.Client(project=project)

        if dry_run:
            job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
            query_job = client.query(query, job_config=job_config)
            bytes_processed = query_job.total_bytes_processed
            # BigQuery on-demand pricing: $6.25 per TB
            cost = (bytes_processed / (1024 ** 4)) * 6.25
            return {
                "success": True,
                "rows": [],
                "total_rows": 0,
                "bytes_processed": bytes_processed,
                "cost_usd": round(cost, 4),
                "message": f"Dry run: {bytes_processed:,} bytes would be processed "
                           f"(estimated cost: ${cost:.4f})",
            }

        query_job = client.query(query)
        results = query_job.result()

        rows = [dict(row) for row in results]
        bytes_processed = query_job.total_bytes_processed or 0
        cost = (bytes_processed / (1024 ** 4)) * 6.25

        return {
            "success": True,
            "rows": rows,
            "total_rows": len(rows),
            "bytes_processed": bytes_processed,
            "cost_usd": round(cost, 4),
            "message": f"Query completed: {len(rows)} rows, "
                       f"{bytes_processed:,} bytes processed",
        }
    except ImportError:
        return {
            "success": False,
            "rows": [],
            "total_rows": 0,
            "bytes_processed": 0,
            "cost_usd": 0.0,
            "message": "google-cloud-bigquery not installed. "
                       "Install with: pip install google-cloud-bigquery",
        }
    except Exception as e:
        return {
            "success": False,
            "rows": [],
            "total_rows": 0,
            "bytes_processed": 0,
            "cost_usd": 0.0,
            "message": f"BigQuery query failed: {str(e)}",
        }
