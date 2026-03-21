from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from ..utils.logging import logger


class FinPilotException(Exception):
    """Base exception for FinPilot application"""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ValidationError(FinPilotException):
    """Validation error"""

    pass


class NotFoundError(FinPilotException):
    """Resource not found error"""

    def __init__(self, resource: str, resource_id: str = None):
        message = f"{resource} not found"
        if resource_id:
            message += f" with id {resource_id}"
        super().__init__(message, 404)


class AuthenticationError(FinPilotException):
    """Authentication error"""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, 401)


class AuthorizationError(FinPilotException):
    """Authorization error"""

    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, 403)


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    logger.warning(f"HTTP exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "type": "http_exception"},
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle SQLAlchemy exceptions"""
    logger.error(f"Database error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Database error occurred", "type": "database_error"},
    )


async def finpilot_exception_handler(request: Request, exc: FinPilotException):
    """Handle FinPilot custom exceptions"""
    logger.warning(f"FinPilot exception: {exc.status_code} - {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message, "type": "finpilot_exception"},
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": "internal_error"},
    )
