"""Pytest configuration file."""
import pytest
from fastapi.testclient import TestClient

from jobs_crm_assistant.api.app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)
