"""Tests for health check endpoint."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check_returns_200():
    """Test that GET /health returns HTTP 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_check_returns_expected_status():
    """Test that GET /health returns expected status field."""
    response = client.get("/health")
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"


def test_health_check_response_format():
    """Test that GET /health returns correct JSON format."""
    response = client.get("/health")
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 1
    assert "status" in data


def test_root_endpoint():
    """Test that root endpoint returns expected message."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Matchboard API is running"
