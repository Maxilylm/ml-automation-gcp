# /gcp-data

Manage Cloud Storage data for ML workflows: upload, download, catalog, and organize.

## Usage

```
/gcp-data <action> [--bucket <bucket>] [--path <gcs_path>] [--local <local_path>] [--format csv|parquet|json]
```

- `action`: `upload`, `download`, `catalog`, `create-bucket`
- `--bucket`: GCS bucket name
- `--path`: GCS object path (prefix or full path)
- `--local`: local file or directory path
- `--format`: data format filter for catalog (default: all)

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` -- if missing, copy from core plugin
2. Check if `gcp_utils.py` exists in `src/` -- if missing, copy from this plugin's `templates/gcp_utils.py`
3. Verify GCP credentials and Cloud Storage API enabled

### Stage 1: Action Execution

1. **Upload** (`action=upload`):
   - Validate local file/directory exists
   - Detect file format and size
   - Upload with resumable transfer for files > 5MB
   - Set content-type metadata
   - Report: GCS URI, file size, upload duration

2. **Download** (`action=download`):
   - Validate GCS path exists
   - Download to local path (single file or recursive prefix)
   - Verify integrity (size match, optional MD5)
   - Report: local path, file count, total size

3. **Catalog** (`action=catalog`):
   - List objects in bucket/prefix
   - Group by format (CSV, Parquet, JSON, Avro, TFRecord)
   - Compute stats: file count, total size, last modified
   - For tabular files: sample schema (first file of each format)
   - Report: data catalog table with format, count, size

4. **Create Bucket** (`action=create-bucket`):
   - Create bucket with specified region and storage class
   - Apply default lifecycle rules (30-day transition to Nearline)
   - Enable uniform bucket-level access
   - Report: bucket name, region, storage class, lifecycle rules

### Stage 2: Data Validation (for upload/download)

1. Verify file integrity post-transfer
2. For tabular data: validate schema consistency
3. Check for common issues: encoding problems, corrupted files, empty files
4. Report: validation results, warnings

### Stage 3: Data Report

```python
from ml_utils import save_agent_report
save_agent_report("gcp-data", {
    "status": "completed",
    "action": action,
    "bucket": bucket,
    "gcs_uri": gcs_uri,
    "local_path": local_path,
    "file_count": file_count,
    "total_size_bytes": total_size,
    "format": file_format,
    "validation": validation_results,
    "catalog": catalog_summary
})
```

Print action summary with file details and GCS URIs.
