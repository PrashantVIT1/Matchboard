"""Resume upload and processing endpoints."""

import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, HTTPException

from app.core.file_storage import save_uploaded_file
from app.core.file_validation import validate_file_upload
from app.core.config import read_pdf, read_docx
from app.core.text_cleaning import clean_extracted_text
from app.services.llm_service import parse_resume
from app.schemas.upload import FileUploadResult, UploadResponse
from app.schemas.candidate import CandidateExtraction, ProcessResumesResponse
from app.schemas.resume import Resume


router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.post("/upload", response_model=UploadResponse)
async def upload_resumes(files: list[UploadFile]) -> UploadResponse:
    """
    Upload multiple resume files.
    
    Accepts multiple PDF files for resume processing.
    Validates file type, size, and content before accepting.
    
    Args:
        files: List of uploaded files
    
    Returns:
        UploadResponse with upload results for each file
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    results = []
    uploaded_count = 0
    
    for file in files:
        # Read file content
        file_content = await file.read()
        
        # Validate file
        is_valid, error_message = validate_file_upload(
            filename=file.filename,
            content_type=file.content_type,
            file_size=len(file_content),
        )
        
        if is_valid:
            # Save file
            try:
                await save_uploaded_file(file_content, file.filename)
                results.append(FileUploadResult(
                    filename=file.filename,
                    status="accepted"
                ))
                uploaded_count += 1
            except Exception as e:
                results.append(FileUploadResult(
                    filename=file.filename,
                    status="rejected",
                    message=f"Failed to save file: {str(e)}"
                ))
        else:
            results.append(FileUploadResult(
                filename=file.filename,
                status="rejected",
                message=error_message
            ))
    
    return UploadResponse(
        uploaded=uploaded_count,
        files=results
    )


@router.post("/process", response_model=ProcessResumesResponse)
async def process_resumes(files: list[UploadFile]) -> ProcessResumesResponse:
    """
    Upload and process multiple resume files.
    
    Accepts multiple PDF/DOCX files, validates them, extracts text,
    parses with LLM, and returns structured candidate information.
    
    Args:
        files: List of uploaded files
    
    Returns:
        ProcessResumesResponse with extracted candidate information
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    candidates = []
    processed_count = 0
    
    for file in files:
        # Read file content
        file_content = await file.read()
        
        # Validate file
        is_valid, error_message = validate_file_upload(
            filename=file.filename,
            content_type=file.content_type,
            file_size=len(file_content),
        )
        
        if not is_valid:
            candidates.append(CandidateExtraction(
                candidate_id=str(uuid.uuid4()),
                filename=file.filename,
                page_count=0,
                extracted_text="",
                extraction_status="failed",
                error_message=error_message
            ))
            continue
        
        # Save file
        try:
            file_path = await save_uploaded_file(file_content, file.filename)
        except Exception as e:
            candidates.append(CandidateExtraction(
                candidate_id=str(uuid.uuid4()),
                filename=file.filename,
                page_count=0,
                extracted_text="",
                extraction_status="failed",
                error_message=f"Failed to save file: {str(e)}"
            ))
            continue
        
        # Extract text based on file type
        try:
            file_ext = Path(file.filename).suffix.lower()
            if file_ext == ".pdf":
                extracted_text = read_pdf(file_path)
            elif file_ext == ".docx":
                extracted_text = read_docx(file_path)
            else:
                candidates.append(CandidateExtraction(
                    candidate_id=str(uuid.uuid4()),
                    filename=file.filename,
                    page_count=0,
                    extracted_text="",
                    extraction_status="failed",
                    error_message=f"Unsupported file type: {file_ext}"
                ))
                continue
            
            if not extracted_text:
                candidates.append(CandidateExtraction(
                    candidate_id=str(uuid.uuid4()),
                    filename=file.filename,
                    page_count=0,
                    extracted_text="",
                    extraction_status="partial",
                    error_message="No extractable text found"
                ))
                continue
            
            # Clean extracted text
            cleaned_text = clean_extracted_text(extracted_text)
            
            candidates.append(CandidateExtraction(
                candidate_id=str(uuid.uuid4()),
                filename=file.filename,
                page_count=0,
                extracted_text=cleaned_text,
                extraction_status="success"
            ))
            processed_count += 1
            
        except Exception as e:
            candidates.append(CandidateExtraction(
                candidate_id=str(uuid.uuid4()),
                filename=file.filename,
                page_count=0,
                extracted_text="",
                extraction_status="failed",
                error_message=f"Error during extraction: {str(e)}"
            ))
    
    return ProcessResumesResponse(
        processed=processed_count,
        candidates=candidates
    )


@router.post("/parse", response_model=Resume)
async def parse_resume_endpoint(files: list[UploadFile]) -> Resume:
    """
    Upload and parse resume files using LLM.
    
    Accepts multiple PDF/DOCX files, extracts text, and parses
    into structured Resume format using LLM.
    
    Args:
        files: List of uploaded files (only first file is processed)
    
    Returns:
        Structured Resume object
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    file = files[0]
    file_content = await file.read()
    
    # Validate file
    is_valid, error_message = validate_file_upload(
        filename=file.filename,
        content_type=file.content_type,
        file_size=len(file_content),
    )
    
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)
    
    # Save file
    try:
        file_path = await save_uploaded_file(file_content, file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # Extract text
    try:
        file_ext = Path(file.filename).suffix.lower()
        if file_ext == ".pdf":
            extracted_text = read_pdf(file_path)
        elif file_ext == ".docx":
            extracted_text = read_docx(file_path)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_ext}")
        
        if not extracted_text:
            raise HTTPException(status_code=400, detail="No extractable text found")
        
        # Clean extracted text
        cleaned_text = clean_extracted_text(extracted_text)
        
        # Parse with LLM
        parsed_resume = parse_resume(cleaned_text)
        return parsed_resume
        
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"LLM configuration error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse resume: {str(e)}")
