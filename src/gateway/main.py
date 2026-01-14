"""
Gateway API application.

FastAPI-based OAuth2 Gateway service.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from gateway.errors.exceptions import FundboxAPIException
from gateway.errors.handlers import (
    fundbox_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from gateway.middleware.db.db_session import db_session_middleware
from gateway.oauth2.router import router as oauth2_router
from gateway.oauth2.token_router import router as token_router
from gateway.routers.debug import router as debug_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler for startup/shutdown events."""
    # Startup
    yield
    # Shutdown


app = FastAPI(
    title="API Gateway",
    description="OAuth2 Gateway API using FastAPI",
    version="0.1.0",
    lifespan=lifespan,
)

# Middleware
app.middleware("http")(db_session_middleware)

# Exception handlers
app.add_exception_handler(FundboxAPIException, fundbox_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Routers
app.include_router(debug_router)
app.include_router(oauth2_router)
app.include_router(token_router)


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/")
def root():
    """Root endpoint with API info."""
    return {
        "name": "API Gateway",
        "version": "0.1.0",
        "docs": "/docs",
    }
