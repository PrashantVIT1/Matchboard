"""API routes for analytics endpoints."""

import io
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse


from app.services.matcher import MatcherService

router = APIRouter(prefix="/matcher", tags=["matcher"])

@router.get("/data", response_model=MatcherService)
def get_match(n, job_description):
    try:
        service = MatcherService(n, job_description)
        return service.get_n_suitable_candidates(n, job_description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/data", response_model=MatcherService)


