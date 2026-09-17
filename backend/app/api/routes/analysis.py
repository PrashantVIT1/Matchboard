"""Batch candidate analysis endpoint."""

import logging
from fastapi import APIRouter, UploadFile, HTTPException, Form

from app.services.analysis_service import analyze_candidates
from app.schemas.analysis import AnalysisResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("", response_model=AnalysisResponse)
async def analyze(
    job_description: str = Form(...),
    top_n: int = Form(..., ge=1),
    files: list[UploadFile] = []
) -> AnalysisResponse:
    """
    Perform end-to-end batch candidate analysis.

    Accepts a job description, multiple resume files, and top_n parameter.
    Parses the job description, extracts and parses each resume,
    matches candidates against the job, ranks by score, and returns top_n results.

    Args:
        job_description: Raw job description text
        top_n: Number of top candidates to return (must be >= 1)
        files: List of uploaded resume files (PDF/DOCX)

    Returns:
        AnalysisResponse with ranked candidate results
    """
    logger.info(f"[API] /analysis called - Files: {len(files)}, Top N: {top_n}")

    # Validate job description
    if not job_description or not job_description.strip():
        logger.error("[API] Job description is empty")
        raise HTTPException(status_code=400, detail="Job description is required")

    # Validate files
    if not files:
        logger.error("[API] No files provided")
        raise HTTPException(status_code=400, detail="At least one resume file is required")

    # Validate top_n
    if top_n > len(files):
        logger.error(f"[API] Top N ({top_n}) exceeds number of files ({len(files)})")
        raise HTTPException(
            status_code=400,
            detail=f"top_n ({top_n}) cannot exceed number of uploaded files ({len(files)})"
        )

    try:
        logger.info("[API] Calling analysis service")
        result = await analyze_candidates(job_description, files, top_n)
        logger.info(f"[API] Analysis service returned successfully")
        return result
    except ValueError as e:
        logger.error(f"[API] LLM configuration error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"LLM configuration error: {str(e)}")
    except Exception as e:
        logger.error(f"[API] Analysis failed: {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
