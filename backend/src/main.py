from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from .config import settings
from .api.router import api_router
from .utils.logging import logger
from .utils.errors import (
    http_exception_handler,
    sqlalchemy_exception_handler,
    finpilot_exception_handler,
    general_exception_handler,
    FinPilotException,
)
from .database import engine

app = FastAPI(
    title="FinPilot API",
    description="Financial planning API for Vietnamese users",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Add exception handlers
app.add_exception_handler(500, general_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(FinPilotException, finpilot_exception_handler)


@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info("Starting FinPilot API")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info("Shutting down FinPilot API")
    await engine.dispose()


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "finpilot-api"}
