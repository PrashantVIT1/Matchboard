"""File validation utilities for resume uploads."""

from pathlib import Path
from typing import Tuple


ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


def validate_file_upload(
    filename: str,
    content_type: str,
    file_size: int,
) -> Tuple[bool, str | None]:
    """
    Validate a file upload.
    
    Args:
        filename: The uploaded file's name
        content_type: The file's content type
        file_size: The file's size in bytes
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check filename exists
    if not filename:
        return False, "Filename is required"
    
    # Check file extension
    file_ext = Path(filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        return False, f"Unsupported file type: {file_ext}. Only PDF files are allowed."
    
    # Check file is not empty
    if file_size == 0:
        return False, "File is empty"
    
    # Check file size limit
    if file_size > MAX_FILE_SIZE_BYTES:
        return False, f"File size exceeds {MAX_FILE_SIZE_MB}MB limit"
    
    # Basic content type check (not foolproof but helps)
    # Be lenient with content types as browsers/systems may send generic types
    if content_type:
        if file_ext == ".pdf" and "pdf" not in content_type.lower():
            return False, f"Invalid content type: {content_type}. Expected PDF."
        # For DOCX, allow application/octet-stream as some systems send this
        if file_ext == ".docx":
            if "word" not in content_type.lower() and "docx" not in content_type.lower() and "octet-stream" not in content_type.lower():
                return False, f"Invalid content type: {content_type}. Expected DOCX."
    
    return True, None
