"""
Request logging middleware to track and log all incoming requests and responses.
"""
import time
import uuid
from typing import Any
from quart import request, Response
from src.logging_config import get_logger
import structlog

logger = get_logger(__name__)


class RequestLoggingMiddleware:
    """Middleware for logging requests and responses."""

    @staticmethod
    async def log_request() -> None:
        """Log incoming request details."""
        # Generate unique request ID for tracking
        request_id = str(uuid.uuid4())
        structlog.contextvars.bind_contextvars(request_id=request_id)

        # Store request start time
        request.start_time = time.time()

        # Log request details
        logger.info(
            "Incoming request",
            method=request.method,
            path=request.path,
            remote_addr=request.remote_addr,
            user_agent=request.headers.get("User-Agent", ""),
        )

    @staticmethod
    async def log_response(response: Response) -> Response:
        """
        Log response details.

        Args:
            response: Response object to be sent

        Returns:
            Response object with added headers
        """
        # Calculate request duration
        duration = None
        if hasattr(request, "start_time"):
            duration = (time.time() - request.start_time) * 1000  # Convert to milliseconds

        # Get request ID from context
        request_id = structlog.contextvars.get_contextvars().get("request_id", "unknown")

        # Log response details
        logger.info(
            "Outgoing response",
            status_code=response.status_code,
            duration_ms=round(duration, 2) if duration else None,
            method=request.method,
            path=request.path,
        )

        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id

        # Clear context variables
        structlog.contextvars.clear_contextvars()

        return response
