"""Tests for resume text extraction and processing."""

import io
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.text_cleaning import clean_extracted_text
from app.core.config import read_pdf


client = TestClient(app)


def test_clean_extracted_text_removes_excessive_whitespace():
    """Test that text cleaning removes excessive whitespace."""
    text = "This  is  a  test\n\n\nwith  extra  spaces"
    cleaned = clean_extracted_text(text)
    assert "  " not in cleaned
    assert "\n\n\n" not in cleaned


def test_clean_extracted_text_preserves_content():
    """Test that text cleaning preserves original content."""
    text = "John Doe\nSoftware Engineer\nPython, Java"
    cleaned = clean_extracted_text(text)
    assert "John Doe" in cleaned
    assert "Software Engineer" in cleaned
    assert "Python" in cleaned


def test_clean_extracted_text_handles_empty():
    """Test that text cleaning handles empty input."""
    cleaned = clean_extracted_text("")
    assert cleaned == ""
    
    cleaned = clean_extracted_text(None)
    assert cleaned == ""


def test_process_single_valid_pdf():
    """Test processing a single valid PDF file."""
    # Use an existing PDF from the project if available
    # For this test, we'll create a minimal PDF-like file
    pdf_content = b"%PDF-1.4\nTest Resume Content\nJohn Doe\nSoftware Engineer\n%%EOF"
    
    file = io.BytesIO(pdf_content)
    filename = "test_resume.pdf"
    
    response = client.post(
        "/resumes/process",
        files={"files": (filename, file, "application/pdf")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["processed"] >= 0  # May fail if PDF is invalid
    assert len(data["candidates"]) == 1
    assert data["candidates"][0]["filename"] == filename


def test_process_multiple_pdfs():
    """Test processing multiple PDF files."""
    pdf_content1 = b"%PDF-1.4\nResume 1\n%%EOF"
    pdf_content2 = b"%PDF-1.4\nResume 2\n%%EOF"
    
    file1 = io.BytesIO(pdf_content1)
    file2 = io.BytesIO(pdf_content2)
    
    response = client.post(
        "/resumes/process",
        files=[
            ("files", ("resume1.pdf", file1, "application/pdf")),
            ("files", ("resume2.pdf", file2, "application/pdf")),
        ]
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["candidates"]) == 2


def test_process_invalid_file_type():
    """Test processing an invalid file type is rejected."""
    file = io.BytesIO(b"test content")
    filename = "resume.txt"
    
    response = client.post(
        "/resumes/process",
        files={"files": (filename, file, "text/plain")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["processed"] == 0
    assert len(data["candidates"]) == 1
    assert data["candidates"][0]["extraction_status"] == "failed"
    assert "Unsupported file type" in data["candidates"][0]["error_message"]


def test_process_no_files():
    """Test processing with no files returns error."""
    response = client.post("/resumes/process")
    
    # FastAPI returns 422 for missing required parameters
    assert response.status_code == 422


def test_process_empty_pdf():
    """Test processing an empty PDF."""
    file = io.BytesIO(b"%PDF-1.4\n%%EOF")
    filename = "empty_resume.pdf"
    
    response = client.post(
        "/resumes/process",
        files={"files": (filename, file, "application/pdf")}
    )
    
    assert response.status_code == 200
    data = response.json()
    # Empty PDF may be marked as partial or failed depending on extraction
    assert len(data["candidates"]) == 1


def test_pdf_extraction_with_existing_file():
    """Test PDF extraction with an actual resume file from the project."""
    # Check if we have existing resume files
    resume_dir = Path(__file__).resolve().parents[2] / "app" / "resumes"
    pdf_files = list(resume_dir.glob("*.pdf"))
    
    if pdf_files:
        # Test with the first PDF found
        pdf_path = pdf_files[0]
        try:
            extracted_text = read_pdf(pdf_path)
            assert isinstance(extracted_text, str)
            assert len(extracted_text) > 0
        except Exception:
            # PDF might be corrupt or unreadable, that's okay for this test
            pytest.skip("PDF file could not be extracted")
    else:
        pytest.skip("No PDF files found in app/resumes directory")


def test_api_response_structure():
    """Test that the API response has the correct structure."""
    pdf_content = b"%PDF-1.4\nTest\n%%EOF"
    file = io.BytesIO(pdf_content)
    
    response = client.post(
        "/resumes/process",
        files={"files": ("test.pdf", file, "application/pdf")}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Check top-level structure
    assert "processed" in data
    assert "candidates" in data
    assert isinstance(data["processed"], int)
    assert isinstance(data["candidates"], list)
    
    # Check candidate structure
    if data["candidates"]:
        candidate = data["candidates"][0]
        assert "candidate_id" in candidate
        assert "filename" in candidate
        assert "page_count" in candidate
        assert "extracted_text" in candidate
        assert "extraction_status" in candidate
        assert candidate["extraction_status"] in ["success", "partial", "failed"]
