"""Tests for resume upload endpoint."""

import io
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def create_test_pdf(content: bytes = b"%PDF-1.4 test pdf content") -> tuple[io.BytesIO, str]:
    """Create a test PDF file."""
    file = io.BytesIO(content)
    file.name = "test_resume.pdf"
    file.content_type = "application/pdf"
    return file, "test_resume.pdf"


def test_upload_single_valid_pdf():
    """Test uploading a single valid PDF file."""
    file, filename = create_test_pdf()
    
    response = client.post(
        "/resumes/upload",
        files={"files": (filename, file, "application/pdf")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["uploaded"] == 1
    assert len(data["files"]) == 1
    assert data["files"][0]["filename"] == filename
    assert data["files"][0]["status"] == "accepted"


def test_upload_multiple_valid_pdfs():
    """Test uploading multiple valid PDF files."""
    file1, filename1 = create_test_pdf(b"%PDF-1.4 test pdf 1")
    file2, filename2 = create_test_pdf(b"%PDF-1.4 test pdf 2")
    file3, filename3 = create_test_pdf(b"%PDF-1.4 test pdf 3")
    
    response = client.post(
        "/resumes/upload",
        files=[
            ("files", (filename1, file1, "application/pdf")),
            ("files", (filename2, file2, "application/pdf")),
            ("files", (filename3, file3, "application/pdf")),
        ]
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["uploaded"] == 3
    assert len(data["files"]) == 3
    for file_result in data["files"]:
        assert file_result["status"] == "accepted"


def test_upload_empty_file():
    """Test uploading an empty file is rejected."""
    file, filename = create_test_pdf(b"")
    
    response = client.post(
        "/resumes/upload",
        files={"files": (filename, file, "application/pdf")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["uploaded"] == 0
    assert len(data["files"]) == 1
    assert data["files"][0]["status"] == "rejected"
    assert "empty" in data["files"][0]["message"].lower()


def test_upload_unsupported_extension():
    """Test uploading a file with unsupported extension is rejected."""
    file = io.BytesIO(b"test content")
    filename = "resume.txt"
    
    response = client.post(
        "/resumes/upload",
        files={"files": (filename, file, "text/plain")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["uploaded"] == 0
    assert len(data["files"]) == 1
    assert data["files"][0]["status"] == "rejected"
    assert "unsupported" in data["files"][0]["message"].lower()


def test_upload_no_files():
    """Test uploading with no files returns validation error."""
    response = client.post("/resumes/upload")
    
    # FastAPI returns 422 for missing required parameters
    assert response.status_code == 422


def test_upload_mixed_valid_and_invalid():
    """Test uploading multiple files where one is invalid."""
    file1, filename1 = create_test_pdf(b"%PDF-1.4 valid pdf")
    file2 = io.BytesIO(b"test content")
    filename2 = "resume.txt"
    
    response = client.post(
        "/resumes/upload",
        files=[
            ("files", (filename1, file1, "application/pdf")),
            ("files", (filename2, file2, "text/plain")),
        ]
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["uploaded"] == 1
    assert len(data["files"]) == 2
    assert data["files"][0]["status"] == "accepted"
    assert data["files"][1]["status"] == "rejected"


def test_upload_file_size_limit():
    """Test uploading a file exceeding size limit is rejected."""
    # Create a file larger than 10MB
    large_content = b"%PDF-1.4 " + b"x" * (11 * 1024 * 1024)
    file = io.BytesIO(large_content)
    filename = "large_resume.pdf"
    
    response = client.post(
        "/resumes/upload",
        files={"files": (filename, file, "application/pdf")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["uploaded"] == 0
    assert len(data["files"]) == 1
    assert data["files"][0]["status"] == "rejected"
    assert "size" in data["files"][0]["message"].lower()


def test_upload_invalid_content_type():
    """Test uploading a PDF with wrong content type is rejected."""
    file, filename = create_test_pdf(b"%PDF-1.4 test pdf")
    
    response = client.post(
        "/resumes/upload",
        files={"files": (filename, file, "text/plain")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["uploaded"] == 0
    assert len(data["files"]) == 1
    assert data["files"][0]["status"] == "rejected"
    assert "content type" in data["files"][0]["message"].lower()
