# Matchboard Backend

AI-powered candidate screening and matching application.

## Installation

This project uses `uv` for dependency management.

### Install Dependencies

```powershell
uv sync --extra dev
```

## Running the Backend

### Start the Development Server

```powershell
uv run uvicorn app.main:app --reload
```

The server will start at `http://127.0.0.1:8000`

## API Documentation

Once the server is running, access the interactive API documentation:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json

## Testing

### Run All Tests

```powershell
uv run pytest
```

### Run Tests with Verbose Output

```powershell
uv run pytest -v
```

## Health Check

Verify the API is running:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

## Configuration

Environment variables are loaded from `.env` file. The `.env` file is git-ignored for security.

Required environment variables:
- `GROQ_API_KEY`: API key for Groq LLM service
- `model`: Model name to use (e.g., `openai/gpt-oss-20b`)
- `FRONTEND_URL`: Frontend URL for CORS (default: `http://localhost:5174`)

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   └── health.py    # Health check endpoint
│   │   └── matching.py      # Matching endpoints (existing)
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py        # LLM and configuration logic
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   └── resumes/             # Resume storage
├── tests/
│   ├── __init__.py
│   └── test_health.py       # Health endpoint tests
├── pyproject.toml           # Project dependencies
└── uv.lock                  # Locked dependencies
```
