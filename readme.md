# Gateway

A modern, async HTTP API gateway built with **FastAPI**, designed to replace the legacy `api` service.

This project is the foundation for the next-generation Fundbox API layer, focusing on:
- Clear domain boundaries
- Consistent error handling
- Strong typing and validation
- Async-first architecture
- Long-term maintainability

---

## Status

🚧 **Bootstrap / Early development**

This repository currently serves as an initial skeleton to:
- Validate project structure
- Establish core conventions
- Align on error handling and request/response patterns

Production traffic, deployment, and migration from the legacy `api` service are **out of scope** for this stage.

---

## Tech Stack

- **Python**: 3.14
- **Framework**: FastAPI
- **ASGI Server**: Uvicorn
- **Dependency management**: `uv`
- **Validation & settings**: Pydantic v2

---

## Project Structure

```text
src/
  gateway/
    ├── main.py          # FastAPI application entrypoint
    ├── routers/         # API routers (per domain / feature)
    ├── deps/            # Shared dependencies
    ├── middleware/      # Custom middleware
    ├── errors/          # Error definitions & exception handling
    └── __init__.py
tests/
```

## Setup
```text
uv venv --python 3.14 .venv
source .venv/bin/activate
uv pip sync requirements.in
```

## Run the server
```text
python -m uvicorn gateway.main:app --reload --port 8001 --app-dir src
```
