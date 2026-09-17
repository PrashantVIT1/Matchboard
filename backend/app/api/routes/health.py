"""Health check endpoint."""

from fastapi import APIRouter
from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health check response schema."""
    status: str


router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """
    Health check endpoint.
    
    Returns a simple status to verify the API is running.
    Does not depend on external services (database, LLM, etc.).
    """
    return HealthResponse(status="ok")
