from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from gateway.oauth2.router import router as auth_router

from gateway.errors.exceptions import FundboxAPIException
from gateway.errors.handlers import (
    fundbox_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from gateway.middleware.db.db_session import db_session_middleware
from gateway.oauth2.token_router import router as token_router


app = FastAPI(title="API Gateway (FastAPI)")
app.middleware("http")(db_session_middleware)
app.include_router(token_router)
app.add_exception_handler(FundboxAPIException, fundbox_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.include_router(auth_router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/boom")
def boom():
    raise RuntimeError("boom")
