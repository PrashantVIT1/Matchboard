"""File storage utilities for resume uploads."""

import os
from pathlib import Path
from typing import Optional


def get_upload_dir() -> Path:
    """
    Get the upload directory path.
    
    Returns:
        Path to the upload directory
    """
    # Default to uploads directory in app folder
    upload_dir = Path(__file__).resolve().parents[1] / "uploads"
    
    # Allow override via environment variable
    env_upload_dir = os.getenv("UPLOAD_DIR")
    if env_upload_dir:
        upload_dir = Path(env_upload_dir)
    
    return upload_dir


def ensure_upload_dir() -> Path:
    """
    Ensure the upload directory exists.
    
    Returns:
        Path to the upload directory
    """
    upload_dir = get_upload_dir()
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir


async def save_uploaded_file(
    file_content: bytes,
    filename: str,
    upload_dir: Optional[Path] = None,
) -> Path:
    """
    Save an uploaded file to the upload directory.
    
    Args:
        file_content: The file's content as bytes
        filename: The filename to save
        upload_dir: Optional custom upload directory
    
    Returns:
        Path to the saved file
    """
    if upload_dir is None:
        upload_dir = ensure_upload_dir()
    
    # Sanitize filename to prevent path traversal
    safe_filename = Path(filename).name
    file_path = upload_dir / safe_filename
    
    # Write file
    with open(file_path, "wb") as f:
        f.write(file_content)
    
    return file_path
