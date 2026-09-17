"""Tests for job description parsing endpoint."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_parse_job_empty_description():
    """Test parsing empty job description returns error."""
    response = client.post(
        "/jobs/parse",
        data=""
    )
    
    assert response.status_code == 422  # FastAPI validation error


def test_parse_job_endpoint_exists():
    """Test that the job parse endpoint exists."""
    response = client.post(
        "/jobs/parse",
        json={"job_description": "Software Engineer position requiring Python and Java skills."}
    )
    
    # May fail if GROQ_API_KEY is not set, but endpoint should exist
    assert response.status_code in [200, 500]
