"""Job description parsing endpoint."""

from fastapi import APIRouter, HTTPException, Body

from app.services.llm_service import parse_job_description
from app.schemas.jobd import JobD


router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/parse", response_model=JobD)
async def parse_job(job_description: str = Body(..., embed=True)) -> JobD:
    """
    Parse job description into structured format.
    
    Args:
        job_description: Raw job description text
    
    Returns:
        Structured JobD object
    """
    if not job_description or not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is required")
    
    try:
        parsed_job = parse_job_description(job_description)
        return parsed_job
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"LLM configuration error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse job description: {str(e)}")
