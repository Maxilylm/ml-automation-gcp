"""Shared pytest fixtures for ml-automation-gcp."""
import json
import tempfile
from pathlib import Path
from typing import Any, Generator
import pytest


@pytest.fixture
def mock_llm_response() -> dict[str, Any]:
    """
    Return a mock LLM response for testing without API calls.

    Typical structure:
        {
            "content": "...",
            "model": "claude-3-5-sonnet",
            "stop_reason": "end_turn"
        }
    """
    return {
        "content": "Mock response from Claude for testing",
        "model": "claude-3-5-sonnet",
        "stop_reason": "end_turn",
    }


@pytest.fixture
def sample_dataset() -> dict[str, Any]:
    """
    Return a sample dataset for ML testing.

    Typical structure:
        {
            "features": [...],
            "labels": [...],
            "metadata": {...}
        }
    """
    return {
        "features": [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]],
        "labels": [0, 1, 0],
        "metadata": {
            "source": "test",
            "rows": 3,
            "columns": 2,
        },
    }


@pytest.fixture
def temp_workspace(tmp_path: Path) -> Generator[Path, None, None]:
    """
    Provide a temporary workspace directory for tests.

    Automatically cleans up after test completes.
    """
    workspace = tmp_path / "workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    yield workspace
