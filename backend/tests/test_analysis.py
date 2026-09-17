"""Tests for batch candidate analysis endpoint."""

import pytest
from unittest.mock import Mock, patch, AsyncMock

from app.services.analysis_service import analyze_candidates
from app.schemas.jobd import JobD
from app.schemas.resume import Resume
from app.schemas.matchResult import MatchResult
from app.schemas.experience import Experience


@pytest.fixture
def mock_jobd():
    """Mock JobD object."""
    return JobD(
        role="Software Engineer",
        required_skills=["Python", "Java"],
        preferred_skills=["SQL"],
        minimum_experience=2.0,
        education_requirements=["Bachelor's in CS"],
        responsibilities=["Develop software"]
    )


@pytest.fixture
def mock_resume():
    """Mock Resume object."""
    return Resume(
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


@pytest.fixture
def mock_match_result():
    """Mock MatchResult object."""
    return MatchResult(
        score=85.0,
        details={"matching_skills": ["Python", "Java"], "missing_skills": []}
    )


def create_mock_upload_file(filename: str, content: bytes = b"test content"):
    """Create a mock UploadFile object."""
    mock_file = Mock()
    mock_file.filename = filename
    mock_file.content_type = "application/pdf" if filename.endswith(".pdf") else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    
    async def mock_read():
        return content
    mock_file.read = mock_read
    
    return mock_file


@patch("app.services.analysis_service.parse_job_description")
@patch("app.services.analysis_service.parse_resume")
@patch("app.services.analysis_service.match_candidate")
@patch("app.services.analysis_service.save_uploaded_file")
@patch("app.services.analysis_service.read_resume")
@pytest.mark.asyncio
async def test_analysis_single_resume(
    mock_read_resume,
    mock_save_uploaded_file,
    mock_match_candidate,
    mock_parse_resume,
    mock_parse_job_description,
    mock_jobd,
    mock_resume,
    mock_match_result
):
    """Test single resume analysis."""
    # Setup mocks
    mock_parse_job_description.return_value = mock_jobd
    mock_save_uploaded_file.return_value = Mock()
    mock_read_resume.return_value = "Resume text content"
    mock_parse_resume.return_value = mock_resume
    mock_match_candidate.return_value = mock_match_result
    
    files = [create_mock_upload_file("resume1.pdf")]
    
    result = await analyze_candidates("Software Engineer requiring Python", files, 1)
    
    assert result.total_candidates == 1
    assert result.successful_candidates == 1
    assert result.failed_candidates == 0
    assert result.top_n == 1
    assert len(result.results) == 1
    assert result.results[0].rank == 1
    assert result.results[0].status == "success"


@patch("app.services.analysis_service.parse_job_description")
@patch("app.services.analysis_service.parse_resume")
@patch("app.services.analysis_service.match_candidate")
@patch("app.services.analysis_service.save_uploaded_file")
@patch("app.services.analysis_service.read_resume")
@pytest.mark.asyncio
async def test_analysis_multiple_resumes(
    mock_read_resume,
    mock_save_uploaded_file,
    mock_match_candidate,
    mock_parse_resume,
    mock_parse_job_description,
    mock_jobd,
    mock_resume
):
    """Test multiple resume analysis with ranking."""
    # Setup mocks
    mock_parse_job_description.return_value = mock_jobd
    mock_save_uploaded_file.return_value = Mock()
    mock_read_resume.return_value = "Resume text content"
    
    # Create different match results for ranking
    def create_match_result(score):
        return MatchResult(
            score=score,
            details={"matching_skills": ["Python"], "missing_skills": []}
        )
    
    mock_parse_resume.return_value = mock_resume
    mock_match_candidate.side_effect = [
        create_match_result(90.0),  # Candidate 1
        create_match_result(75.0),  # Candidate 2
        create_match_result(85.0),  # Candidate 3
    ]
    
    files = [
        create_mock_upload_file("resume1.pdf", b"test1"),
        create_mock_upload_file("resume2.pdf", b"test2"),
        create_mock_upload_file("resume3.pdf", b"test3"),
    ]
    
    result = await analyze_candidates("Software Engineer requiring Python", files, 3)
    
    assert result.total_candidates == 3
    assert result.successful_candidates == 3
    assert result.failed_candidates == 0
    assert len(result.results) == 3
    
    # Check ranking (should be sorted by score descending)
    scores = [r.match.score for r in result.results]
    assert scores == [90.0, 85.0, 75.0]
    
    # Check ranks
    ranks = [r.rank for r in result.results]
    assert ranks == [1, 2, 3]


@patch("app.services.analysis_service.parse_job_description")
@patch("app.services.analysis_service.parse_resume")
@patch("app.services.analysis_service.match_candidate")
@patch("app.services.analysis_service.save_uploaded_file")
@patch("app.services.analysis_service.read_resume")
@pytest.mark.asyncio
async def test_analysis_top_n_filtering(
    mock_read_resume,
    mock_save_uploaded_file,
    mock_match_candidate,
    mock_parse_resume,
    mock_parse_job_description,
    mock_jobd,
    mock_resume
):
    """Test that top_n correctly filters results."""
    # Setup mocks
    mock_parse_job_description.return_value = mock_jobd
    mock_save_uploaded_file.return_value = Mock()
    mock_read_resume.return_value = "Resume text content"
    
    def create_match_result(score):
        return MatchResult(
            score=score,
            details={"matching_skills": ["Python"], "missing_skills": []}
        )
    
    mock_parse_resume.return_value = mock_resume
    mock_match_candidate.side_effect = [
        create_match_result(90.0),
        create_match_result(75.0),
        create_match_result(85.0),
    ]
    
    files = [
        create_mock_upload_file("resume1.pdf", b"test1"),
        create_mock_upload_file("resume2.pdf", b"test2"),
        create_mock_upload_file("resume3.pdf", b"test3"),
    ]
    
    result = await analyze_candidates("Software Engineer requiring Python", files, 2)
    
    assert result.total_candidates == 3
    assert result.successful_candidates == 3
    assert result.top_n == 2
    
    # Should return top 2 candidates
    successful_results = [r for r in result.results if r.status == "success"]
    assert len(successful_results) == 2
    
    # Check they are the top 2
    scores = [r.match.score for r in successful_results]
    assert scores == [90.0, 85.0]


@patch("app.services.analysis_service.parse_job_description")
@pytest.mark.asyncio
async def test_analysis_jd_parsing_failure(mock_parse_job_description):
    """Test that JD parsing failure causes overall analysis failure."""
    mock_parse_job_description.side_effect = Exception("JD parsing failed")
    
    files = [create_mock_upload_file("resume1.pdf")]
    
    with pytest.raises(Exception, match="JD parsing failed"):
        await analyze_candidates("Software Engineer", files, 1)


@patch("app.services.analysis_service.parse_job_description")
@patch("app.services.analysis_service.parse_resume")
@patch("app.services.analysis_service.match_candidate")
@patch("app.services.analysis_service.save_uploaded_file")
@patch("app.services.analysis_service.read_resume")
@pytest.mark.asyncio
async def test_analysis_resume_parsing_failure(
    mock_read_resume,
    mock_save_uploaded_file,
    mock_match_candidate,
    mock_parse_resume,
    mock_parse_job_description,
    mock_jobd,
    mock_resume,
    mock_match_result
):
    """Test that one resume parsing failure doesn't stop other resumes."""
    mock_parse_job_description.return_value = mock_jobd
    mock_save_uploaded_file.return_value = Mock()
    mock_read_resume.return_value = "Resume text content"
    
    # First resume fails parsing, second succeeds
    mock_parse_resume.side_effect = [
        Exception("Resume parsing failed"),
        mock_resume
    ]
    mock_match_candidate.return_value = mock_match_result
    
    files = [
        create_mock_upload_file("resume1.pdf", b"test1"),
        create_mock_upload_file("resume2.pdf", b"test2"),
    ]
    
    result = await analyze_candidates("Software Engineer", files, 2)
    
    assert result.total_candidates == 2
    assert result.successful_candidates == 1
    assert result.failed_candidates == 1
    
    # Check that one failed and one succeeded
    failed_results = [r for r in result.results if r.status == "failed"]
    successful_results = [r for r in result.results if r.status == "success"]
    assert len(failed_results) == 1
    assert len(successful_results) == 1


@patch("app.services.analysis_service.parse_job_description")
@patch("app.services.analysis_service.parse_resume")
@patch("app.services.analysis_service.match_candidate")
@patch("app.services.analysis_service.save_uploaded_file")
@patch("app.services.analysis_service.read_resume")
@pytest.mark.asyncio
async def test_analysis_invalid_file(
    mock_read_resume,
    mock_save_uploaded_file,
    mock_match_candidate,
    mock_parse_resume,
    mock_parse_job_description,
    mock_jobd,
    mock_resume,
    mock_match_result
):
    """Test that invalid file is reported but doesn't stop valid files."""
    mock_parse_job_description.return_value = mock_jobd
    mock_save_uploaded_file.return_value = Mock()
    mock_read_resume.return_value = "Resume text content"
    mock_parse_resume.return_value = mock_resume
    mock_match_candidate.return_value = mock_match_result
    
    # Use an invalid file extension
    files = [
        create_mock_upload_file("resume1.txt"),
        create_mock_upload_file("resume2.pdf"),
    ]
    
    result = await analyze_candidates("Software Engineer", files, 2)
    
    assert result.total_candidates == 2
    assert result.successful_candidates == 1
    assert result.failed_candidates == 1
    
    # Check that invalid file was rejected
    failed_results = [r for r in result.results if r.status == "failed"]
    assert len(failed_results) == 1
    assert "Unsupported file type" in failed_results[0].error


@patch("app.services.analysis_service.parse_job_description")
@pytest.mark.asyncio
async def test_analysis_llm_configuration_error(mock_parse_job_description):
    """Test that LLM configuration error is handled."""
    mock_parse_job_description.side_effect = ValueError("GROQ_API_KEY is not set")
    
    files = [create_mock_upload_file("resume1.pdf")]
    
    with pytest.raises(ValueError, match="GROQ_API_KEY is not set"):
        await analyze_candidates("Software Engineer", files, 1)
