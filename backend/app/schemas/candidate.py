"""Pydantic schemas for candidate extraction."""

from pydantic import BaseModel
from typing import Literal


class CandidateExtraction(BaseModel):
    """Schema for extracted candidate information from resume."""
    candidate_id: str
    filename: str
    page_count: int
    extracted_text: str
    extraction_status: Literal["success", "partial", "failed"]
    error_message: str | None = None


class ProcessResumesResponse(BaseModel):
    """Response for resume processing endpoint."""
    processed: int
    candidates: list[CandidateExtraction]
