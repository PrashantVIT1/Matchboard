import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.api.routes.resumes import router as resumes_router
from app.api.routes.jobs import router as jobs_router
from app.api.routes.matching import router as matching_router
from app.api.routes.analysis import router as analysis_router

# Load environment variables
load_dotenv()
FRONTEND_URL = os.getenv("FRONTEND_URL")

app = FastAPI(
    title="Matchboard API",
    description="AI-powered candidate screening and matching application",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS Configuration - Allow localhost and 127.0.0.1 for local development
# The browser preview proxy uses dynamic ports, so we use a regex to match any port
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL,
    ],
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router)
app.include_router(resumes_router)
app.include_router(jobs_router)
app.include_router(matching_router)
app.include_router(analysis_router)


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Matchboard API is running"}
