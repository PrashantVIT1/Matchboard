"""Analysis service for batch candidate matching."""

import logging
from pathlib import Path

from app.core.config import read_resume
from app.core.file_validation import validate_file_upload
from app.core.file_storage import save_uploaded_file
from app.core.text_cleaning import clean_extracted_text
from app.services.llm_service import parse_job_description, parse_resume, match_candidate
from app.schemas.jobd import JobD
from app.schemas.resume import Resume
from app.schemas.matchResult import MatchResult
from app.schemas.analysis import CandidateMatchResult, AnalysisResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def analyze_candidates(
    job_description: str,
    files: list,
    top_n: int
) -> AnalysisResponse:
    """
    Perform end-to-end batch candidate analysis.

    Args:
        job_description: Raw job description text
        files: List of UploadFile objects
        top_n: Number of top candidates to return

    Returns:
        AnalysisResponse with ranked candidate results
    """
    logger.info(f"[ANALYSIS] Starting analysis - Files: {len(files)}, Top N: {top_n}")

    # Parse job description once
    try:
        logger.info("[ANALYSIS] Parsing job description")
        job = parse_job_description(job_description)
        logger.info("[ANALYSIS] Job description parsed successfully")
    except Exception as e:
        logger.error(f"[ANALYSIS] Job description parsing failed: {type(e).__name__}: {str(e)}")
        raise ValueError(f"Failed to parse job description: {str(e)}")

    # Process each resume
    all_results = []
    successful_count = 0
    failed_count = 0

    for file in files:
        # Read file content
        file_content = await file.read()
        filename = file.filename
        content_type = file.content_type

        logger.info(f"[ANALYSIS] Processing file: {filename}")

        # Validate file
        is_valid, error_message = validate_file_upload(
            filename=filename,
            content_type=content_type,
            file_size=len(file_content),
        )

        if not is_valid:
            logger.error(f"[ANALYSIS] File validation failed: {filename} - {error_message}")
            all_results.append(CandidateMatchResult(
                rank=0,
                filename=filename,
                candidate=Resume(),
                match=MatchResult(score=0.0, details={}),
                status="failed",
                error=error_message
            ))
            failed_count += 1
            continue

        # Save file
        try:
            file_path = await save_uploaded_file(file_content, filename)
            logger.info(f"[ANALYSIS] File saved: {file_path}")
        except Exception as e:
            logger.error(f"[ANALYSIS] File save failed: {filename} - {str(e)}")
            all_results.append(CandidateMatchResult(
                rank=0,
                filename=filename,
                candidate=Resume(),
                match=MatchResult(score=0.0, details={}),
                status="failed",
                error=f"Failed to save file: {str(e)}"
            ))
            failed_count += 1
            continue

        # Extract text
        try:
            extracted_text = read_resume(file_path)

            if not extracted_text:
                logger.error(f"[ANALYSIS] No extractable text: {filename}")
                all_results.append(CandidateMatchResult(
                    rank=0,
                    filename=filename,
                    candidate=Resume(),
                    match=MatchResult(score=0.0, details={}),
                    status="failed",
                    error="No extractable text found"
                ))
                failed_count += 1
                continue

            # Clean extracted text
            cleaned_text = clean_extracted_text(extracted_text)
            logger.info(f"[ANALYSIS] Text extracted and cleaned: {filename}")

            # Parse resume
            try:
                logger.info(f"[ANALYSIS] Parsing resume: {filename}")
                parsed_resume = parse_resume(cleaned_text)
                logger.info(f"[ANALYSIS] Resume parsed successfully: {filename}")
            except Exception as e:
                logger.error(f"[ANALYSIS] Resume parsing failed: {filename} - {type(e).__name__}: {str(e)}")
                all_results.append(CandidateMatchResult(
                    rank=0,
                    filename=filename,
                    candidate=Resume(),
                    match=MatchResult(score=0.0, details={}),
                    status="failed",
                    error=f"Resume parsing failed: {str(e)}"
                ))
                failed_count += 1
                continue

            # Match candidate
            try:
                logger.info(f"[ANALYSIS] Matching candidate: {filename}")
                match_result = match_candidate(job, parsed_resume)
                logger.info(f"[ANALYSIS] Candidate matched successfully: {filename} - Score: {match_result.score}")
            except Exception as e:
                logger.error(f"[ANALYSIS] Candidate matching failed: {filename} - {type(e).__name__}: {str(e)}")
                all_results.append(CandidateMatchResult(
                    rank=0,
                    filename=filename,
                    candidate=parsed_resume,
                    match=MatchResult(score=0.0, details={}),
                    status="failed",
                    error=f"Candidate matching failed: {str(e)}"
                ))
                failed_count += 1
                continue

            all_results.append(CandidateMatchResult(
                rank=0,  # Will be assigned after sorting
                filename=filename,
                candidate=parsed_resume,
                match=match_result,
                status="success",
                error=None
            ))
            successful_count += 1

        except Exception as e:
            logger.error(f"[ANALYSIS] Processing error: {filename} - {type(e).__name__}: {str(e)}")
            all_results.append(CandidateMatchResult(
                rank=0,
                filename=filename,
                candidate=Resume(),
                match=MatchResult(score=0.0, details={}),
                status="failed",
                error=f"Processing error: {str(e)}"
            ))
            failed_count += 1

    # Sort successful candidates by score descending
    successful_results = [r for r in all_results if r.status == "success"]
    successful_results.sort(key=lambda x: x.match.score, reverse=True)

    # Assign ranks
    for idx, result in enumerate(successful_results, start=1):
        result.rank = idx

    # Apply top_n filter
    if top_n < len(successful_results):
        # Keep failed results and top_n successful results
        final_results = [r for r in all_results if r.status == "failed"]
        final_results.extend(successful_results[:top_n])
    else:
        final_results = all_results

    # Sort final results by rank (successful first, then failed)
    final_results.sort(key=lambda x: (x.rank if x.status == "success" else 999999))

    logger.info(f"[ANALYSIS] Analysis complete - Total: {len(files)}, Successful: {successful_count}, Failed: {failed_count}")

    return AnalysisResponse(
        total_candidates=len(files),
        successful_candidates=successful_count,
        failed_candidates=failed_count,
        top_n=top_n,
        results=final_results
    )
