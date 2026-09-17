"""Pydantic schemas for batch candidate analysis."""

from pydantic import BaseModel
from typing import Literal

from app.schemas.resume import Resume
from app.schemas.matchResult import MatchResult


class CandidateMatchResult(BaseModel):
    """Schema for a single candidate match result."""
    rank: int
    filename: str
    candidate: Resume
    match: MatchResult
    status: Literal["success", "failed"]
    error: str | None = None


class AnalysisResponse(BaseModel):
    """Response schema for batch candidate analysis endpoint."""
    total_candidates: int
    successful_candidates: int
    failed_candidates: int
    top_n: int
    results: list[CandidateMatchResult]
