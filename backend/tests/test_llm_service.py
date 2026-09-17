"""Tests for LLM service with mocked Groq client."""

import json
from unittest.mock import Mock, patch

import pytest

from app.schemas.experience import Experience
from app.schemas.resume import Resume
from app.services.llm_service import parse_resume


class TestParseResume:
    """Tests for parse_resume function."""

    def test_parse_resume_valid_output(self):
        """Test parsing resume with valid LLM output."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps({
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "555-1234",
            "total_experience_years": 5.0,
            "skills": ["Python", "Java", "SQL"],
            "experiences": [
                {
                    "company": "Tech Corp",
                    "role": "Software Engineer",
                    "duration": "3 years",
                    "description": "Developed web applications",
                    "skills_used": ["Python", "Django"]
                }
            ],
            "education": ["BS Computer Science"],
            "projects": ["Project A"],
            "certifications": ["AWS"]
        })

        with patch('app.services.llm_service.get_llm_client') as mock_get_client:
            mock_client = Mock()
            mock_client.chat.completions.create.return_value = mock_response
            mock_get_client.return_value = mock_client

            result = parse_resume("Sample resume text")

            assert isinstance(result, Resume)
            assert result.name == "John Doe"
            assert result.email == "john@example.com"
            assert result.total_experience_years == 5.0
            assert len(result.skills) == 3
            assert len(result.experiences) == 1
            assert result.experiences[0].company == "Tech Corp"

    def test_parse_resume_missing_optional_fields(self):
        """Test parsing resume with missing optional fields."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps({
            "name": "Jane Smith",
            "email": None,
            "phone": None,
            "total_experience_years": None,
            "skills": [],
            "experiences": [],
            "education": [],
            "projects": [],
            "certifications": []
        })

        with patch('app.services.llm_service.get_llm_client') as mock_get_client:
            mock_client = Mock()
            mock_client.chat.completions.create.return_value = mock_response
            mock_get_client.return_value = mock_client

            result = parse_resume("Minimal resume")

            assert isinstance(result, Resume)
            assert result.name == "Jane Smith"
            assert result.email is None
            assert result.phone is None
            assert result.total_experience_years is None
            assert result.skills == []
            assert result.experiences == []

    def test_parse_resume_nested_experience_data(self):
        """Test parsing resume with nested experience objects."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps({
            "name": "Alice Johnson",
            "email": "alice@example.com",
            "phone": "555-5678",
            "total_experience_years": 8.5,
            "skills": ["React", "Node.js", "TypeScript"],
            "experiences": [
                {
                    "company": "Startup Inc",
                    "role": "Senior Developer",
                    "duration": "4 years",
                    "description": "Led frontend team",
                    "skills_used": ["React", "TypeScript"]
                },
                {
                    "company": "Enterprise Co",
                    "role": "Developer",
                    "duration": "3 years",
                    "description": "Built APIs",
                    "skills_used": ["Node.js", "Express"]
                }
            ],
            "education": ["MS Computer Science"],
            "projects": [],
            "certifications": []
        })

        with patch('app.services.llm_service.get_llm_client') as mock_get_client:
            mock_client = Mock()
            mock_client.chat.completions.create.return_value = mock_response
            mock_get_client.return_value = mock_client

            result = parse_resume("Resume with multiple experiences")

            assert isinstance(result, Resume)
            assert len(result.experiences) == 2
            assert result.experiences[0].company == "Startup Inc"
            assert result.experiences[0].role == "Senior Developer"
            assert result.experiences[1].company == "Enterprise Co"
            assert result.experiences[1].skills_used == ["Node.js", "Express"]

    def test_parse_resume_malformed_json(self):
        """Test parsing resume with malformed JSON output."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "{ invalid json }"

        with patch('app.services.llm_service.get_llm_client') as mock_get_client:
            mock_client = Mock()
            mock_client.chat.completions.create.return_value = mock_response
            mock_get_client.return_value = mock_client

            with pytest.raises(ValueError) as exc_info:
                parse_resume("Some resume text")

            assert "Invalid JSON output from LLM" in str(exc_info.value)

    def test_parse_resume_json_with_extra_fields(self):
        """Test parsing resume with extra fields (Pydantic should ignore them)."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps({
            "name": "Bob Wilson",
            "email": "bob@example.com",
            "phone": "555-9999",
            "total_experience_years": 3.0,
            "skills": ["Python"],
            "experiences": [],
            "education": [],
            "projects": [],
            "certifications": [],
            "extra_field": "should be ignored",
            "another_extra": 123
        })

        with patch('app.services.llm_service.get_llm_client') as mock_get_client:
            mock_client = Mock()
            mock_client.chat.completions.create.return_value = mock_response
            mock_get_client.return_value = mock_client

            result = parse_resume("Resume with extra fields")

            assert isinstance(result, Resume)
            assert result.name == "Bob Wilson"
            # Extra fields are ignored by Pydantic

    def test_parse_resume_wrong_type_for_numeric_field(self):
        """Test parsing resume with string instead of number for experience years."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps({
            "name": "Test User",
            "email": "test@example.com",
            "phone": "555-0000",
            "total_experience_years": "5",  # String instead of number
            "skills": [],
            "experiences": [],
            "education": [],
            "projects": [],
            "certifications": []
        })

        with patch('app.services.llm_service.get_llm_client') as mock_get_client:
            mock_client = Mock()
            mock_client.chat.completions.create.return_value = mock_response
            mock_get_client.return_value = mock_client

            # Pydantic should coerce string to number if possible
            result = parse_resume("Resume with wrong type")

            assert isinstance(result, Resume)
            # Pydantic v2 may coerce this, but if it fails, it will raise ValidationError

    def test_parse_resume_groq_api_error(self):
        """Test parsing resume when Groq API returns an error."""
        with patch('app.services.llm_service.get_llm_client') as mock_get_client:
            mock_client = Mock()
            mock_client.chat.completions.create.side_effect = Exception("Groq API error")
            mock_get_client.return_value = mock_client

            with pytest.raises(Exception) as exc_info:
                parse_resume("Resume text")

            assert "Groq API error" in str(exc_info.value)

    def test_parse_resume_empty_arrays(self):
        """Test parsing resume with empty arrays (should be valid)."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps({
            "name": "Empty Arrays User",
            "email": None,
            "phone": None,
            "total_experience_years": 0.0,
            "skills": [],
            "experiences": [],
            "education": [],
            "projects": [],
            "certifications": []
        })

        with patch('app.services.llm_service.get_llm_client') as mock_get_client:
            mock_client = Mock()
            mock_client.chat.completions.create.return_value = mock_response
            mock_get_client.return_value = mock_client

            result = parse_resume("Resume with empty arrays")

            assert isinstance(result, Resume)
            assert result.skills == []
            assert result.experiences == []

    def test_parse_resume_null_instead_of_array(self):
        """Test parsing resume with null instead of array (should fail validation)."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps({
            "name": "Null Arrays User",
            "email": None,
            "phone": None,
            "total_experience_years": 0.0,
            "skills": None,  # Should be array, not null
            "experiences": None,
            "education": None,
            "projects": None,
            "certifications": None
        })

        with patch('app.services.llm_service.get_llm_client') as mock_get_client:
            mock_client = Mock()
            mock_client.chat.completions.create.return_value = mock_response
            mock_get_client.return_value = mock_client

            # This should fail Pydantic validation
            with pytest.raises(Exception):  # Pydantic ValidationError
                parse_resume("Resume with null arrays")
