"""
CORS (Cross-Origin Resource Sharing) configuration.
"""
from quart import Quart
from quart_cors import cors
from src.config import settings
from src.logging_config import get_logger

logger = get_logger(__name__)


def setup_cors(app: Quart) -> Quart:
    """
    Configure CORS for the application.

    Args:
        app: Quart application instance

    Returns:
        Quart application with CORS configured
    """
    # Apply CORS to the entire application
    app = cors(
        app,
        allow_origin=settings.cors_origins,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=[
            "Content-Type",
            "Authorization",
            "X-Request-ID",
            "Accept",
        ],
        allow_credentials=True,
        max_age=3600,
    )

    logger.info(
        "CORS configured",
        allowed_origins=settings.cors_origins,
    )

    return app
