"""Tests for matching endpoint."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.jobd import JobD
from app.schemas.resume import Resume


client = TestClient(app)


def test_match_endpoint_exists():
    """Test that the match endpoint exists."""
    job = JobD(
        role="Software Engineer",
        required_skills=["Python", "Java"],
        preferred_skills=["SQL"],
        minimum_experience=2.0,
        education_requirements=["Bachelor's in CS"],
        responsibilities=["Develop software"]
    )
    
    resume = Resume(
        name="John Doe",
        email="john@example.com",
        phone="123-456-7890",
        total_experience_years=3.0,
        skills=["Python", "Java", "SQL"],
        experiences=[],
        education=["Bachelor's in CS"],
        projects=[],
        certifications=[]
    )
    
    response = client.post(
        "/matching/match",
        json={
            "job": job.model_dump(),
            "resume": resume.model_dump()
        }
    )
    
    # May fail if GROQ_API_KEY is not set, but endpoint should exist
    assert response.status_code in [200, 500]
