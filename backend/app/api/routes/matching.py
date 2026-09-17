"""Matching endpoint for candidate-job matching."""

from fastapi import APIRouter, HTTPException

from app.schemas.jobd import JobD
from app.schemas.resume import Resume
from app.schemas.matchResult import MatchResult
from app.services.llm_service import match_candidate


router = APIRouter(prefix="/matching", tags=["matching"])


@router.post("/match", response_model=MatchResult)
async def match_candidate_endpoint(job: JobD, resume: Resume) -> MatchResult:
    """
    Match a candidate resume against a job description.
    
    Args:
        job: Structured JobD object
        resume: Structured Resume object
    
    Returns:
        MatchResult with score and details
    """
    try:
        match_result = match_candidate(job, resume)
        return match_result
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"LLM configuration error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to match candidate: {str(e)}")
