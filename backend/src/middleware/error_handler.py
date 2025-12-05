"""
Global error handling middleware for the application.
Provides consistent error responses and logging.
"""
from typing import Dict, Any, Tuple
from quart import Quart, jsonify
from werkzeug.exceptions import HTTPException
from pydantic import ValidationError
from src.logging_config import get_logger

logger = get_logger(__name__)


class APIError(Exception):
    """Custom exception for API errors."""

    def __init__(
        self,
        message: str,
        status_code: int = 400,
        error_code: str = "API_ERROR",
        details: Dict[str, Any] = None
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}


def register_error_handlers(app: Quart) -> None:
    """
    Register error handlers for the application.

    Args:
        app: Quart application instance
    """

    @app.errorhandler(APIError)
    async def handle_api_error(error: APIError) -> Tuple[Dict[str, Any], int]:
        """Handle custom API errors."""
        logger.warning(
            "API error occurred",
            error_code=error.error_code,
            message=error.message,
            status_code=error.status_code,
            details=error.details,
        )

        return jsonify({
            "error": {
                "code": error.error_code,
                "message": error.message,
                "details": error.details,
            }
        }), error.status_code

    @app.errorhandler(ValidationError)
    async def handle_validation_error(error: ValidationError) -> Tuple[Dict[str, Any], int]:
        """Handle Pydantic validation errors."""
        logger.warning(
            "Validation error",
            errors=error.errors(),
        )

        return jsonify({
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": {
                    "validation_errors": error.errors()
                }
            }
        }), 422

    @app.errorhandler(HTTPException)
    async def handle_http_exception(error: HTTPException) -> Tuple[Dict[str, Any], int]:
        """Handle Werkzeug HTTP exceptions."""
        logger.warning(
            "HTTP exception",
            status_code=error.code,
            message=error.description,
        )

        return jsonify({
            "error": {
                "code": error.name.upper().replace(" ", "_"),
                "message": error.description,
            }
        }), error.code

    @app.errorhandler(Exception)
    async def handle_unexpected_error(error: Exception) -> Tuple[Dict[str, Any], int]:
        """Handle unexpected errors."""
        logger.exception(
            "Unexpected error occurred",
            error_type=type(error).__name__,
            error_message=str(error),
        )

        # Don't expose internal error details in production
        if app.config.get("DEBUG"):
            message = str(error)
        else:
            message = "An unexpected error occurred. Please try again later."

        return jsonify({
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": message,
            }
        }), 500

    logger.info("Error handlers registered")
