"""Pydantic schemas for Match Result."""

from pydantic import BaseModel


class MatchResult(BaseModel):
    """Schema for candidate match result."""
    score: float
    details: dict
