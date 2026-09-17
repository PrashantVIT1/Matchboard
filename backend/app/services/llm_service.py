"""LLM service for Groq API interactions."""

import json
import logging
import os
from groq import Groq
from dotenv import load_dotenv

from app.schemas.jobd import JobD
from app.schemas.resume import Resume
from app.schemas.matchResult import MatchResult

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("model")

# Log configuration (without secrets)
logger.info(f"[CONFIG] GROQ_API_KEY loaded: {bool(GROQ_API_KEY)}")
logger.info(f"[CONFIG] MODEL: {MODEL}")

_client = None


def get_llm_client():
    """Get or create LLM client."""
    global _client
    if _client is None:
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set")
        _client = Groq(api_key=GROQ_API_KEY)
    return _client


def parse_job_description(job_description: str) -> JobD:
    """
    Parse job description into structured JobD using LLM.

    Args:
        job_description: Raw job description text

    Returns:
        Structured JobD object
    """
    logger.info("[LLM] Starting JD parsing")
    client = get_llm_client()
    jobd_schema = JobD.model_json_schema()

    system_prompt = f"""
    You are an expert HR assistant.

    Your job is to analyze job descriptions and extract
    structured information from them.

    Return ONLY valid JSON matching this schema:

    {jobd_schema}
    IMPORTANT:
    Do NOT return the schema itself.
    Do NOT return fields like "properties", "title" or "type".
    Fill the schema with actual information extracted from the job description.

    If minimum experience is not mentioned, return null.
    If information for a list is missing, return an empty list.
    Do not invent information.
    """

    user_prompt = f"""
    Analyze the following job description:

    {job_description}
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            response_format={"type": "json_object"}
        )
        logger.info(f"[LLM] JD parsing succeeded - Model: {MODEL}")
        raw_json = response.choices[0].message.content
        job_data = json.loads(raw_json)
        return JobD(**job_data)
    except Exception as e:
        logger.error(f"[LLM] JD parsing failed - Error: {type(e).__name__}: {str(e)}")
        raise


def parse_resume(resume_text: str) -> Resume:
    """
    Parse resume text into structured Resume using LLM.

    Args:
        resume_text: Raw resume text

    Returns:
        Structured Resume object
    """
    logger.info("[LLM] Starting resume parsing")
    client = get_llm_client()

    system_prompt = """
    You are an expert resume parser. Extract information from resumes into structured JSON.

    CRITICAL OUTPUT RULES:
    1. Return ONLY valid JSON. No Markdown, no ```json fences, no explanations.
    2. Use EXACTLY these fields with these exact types:
       - name: string or null
       - email: string or null
       - phone: string or null
       - total_experience_years: number or null
       - skills: array of strings (empty array if none)
       - experiences: array of objects (empty array if none)
       - education: array of strings (empty array if none)
       - projects: array of strings (empty array if none)
       - certifications: array of strings (empty array if none)
    3. Each experience object must have:
       - company: string or null
       - role: string or null
       - duration: string or null
       - description: string or null
       - skills_used: array of strings (empty array if none)
    4. Do NOT invent information. Use null for missing values.
    5. Arrays must always be arrays, never null.
    6. Numeric fields must be numbers, never strings.
    7. Do NOT add extra fields beyond those specified.
    8. Do NOT change field names.

    Extract information based on meaning, not exact section headings.
    Different resumes may use headings like: Experience, Professional Experience, Work History, Employment, Internships.
    Skills may appear in skills section, work experience, internships, or projects.
    """

    user_prompt = f"""
    Parse the following resume into JSON:

    {resume_text}
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.3  # Lower temperature for more deterministic output
        )
        logger.info(f"[LLM] Resume parsing succeeded - Model: {MODEL}")
        raw_output = response.choices[0].message.content
        logger.debug(f"[LLM] Raw output length: {len(raw_output)} characters")
        
        # Parse JSON
        data = json.loads(raw_output)
        
        # Validate against Pydantic model
        resume = Resume(**data)
        logger.info(f"[LLM] Resume validated successfully - Name: {resume.name}, Skills: {len(resume.skills)}")
        return resume
        
    except json.JSONDecodeError as e:
        logger.error(f"[LLM] JSON parsing failed - Error: {str(e)}")
        logger.error(f"[LLM] Raw output (first 500 chars): {raw_output[:500] if 'raw_output' in locals() else 'N/A'}")
        raise ValueError(f"Invalid JSON output from LLM: {str(e)}")
    except Exception as e:
        logger.error(f"[LLM] Resume parsing failed - Error: {type(e).__name__}: {str(e)}")
        if hasattr(e, 'response'):
            logger.error(f"[LLM] Groq API error: {e.response}")
        raise


def match_candidate(job: JobD, resume: Resume) -> MatchResult:
    """
    Match candidate resume against job description using LLM.

    Args:
        job: Structured JobD object
        resume: Structured Resume object

    Returns:
        MatchResult with score and details
    """
    logger.info("[LLM] Starting candidate matching")
    client = get_llm_client()
    match_schema = MatchResult.model_json_schema()

    prompt = f"""
    You are an HR recruiter.

    Compare the candidate's resume with the job description.

    JOB DESCRIPTION:
    {job.model_dump_json(indent=2)}

    CANDIDATE RESUME:
    {resume.model_dump_json(indent=2)}
    Return JSON matching this schema:

    {match_schema}

    Give me:

    1. Candidate name
    2. Matching skills
    3. Missing important skills
    4. Whether experience requirement is met
    5. Overall match percentage from 0 to 100
    6. A short final verdict

    Keep the response concise and easy to read.
    """

    messages = [{"role": "user", "content": prompt}]

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.5
        )
        logger.info(f"[LLM] Candidate matching succeeded - Model: {MODEL}")
        data = json.loads(response.choices[0].message.content)
        return MatchResult(**data)
    except Exception as e:
        logger.error(f"[LLM] Candidate matching failed - Error: {type(e).__name__}: {str(e)}")
        raise
