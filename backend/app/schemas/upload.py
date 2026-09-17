"""Pydantic schemas for resume upload."""

from pydantic import BaseModel


class FileUploadResult(BaseModel):
    """Result for a single file upload."""
    filename: str
    status: str  # "accepted" or "rejected"
    message: str | None = None


class UploadResponse(BaseModel):
    """Response for resume upload endpoint."""
    uploaded: int
    files: list[FileUploadResult]
