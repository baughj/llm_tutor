"""
CodeMentor Backend - Main Application Entry Point
Quart async web application for LLM Coding Tutor Platform
"""
import asyncio
from typing import Dict, Any
from quart import Quart, jsonify, request
from quart_cors import cors
from hypercorn.config import Config as HypercornConfig
from hypercorn.asyncio import serve

from src.config import settings
from src.logging_config import configure_logging, get_logger
from src.middleware.error_handler import register_error_handlers
from src.middleware.request_logging import RequestLoggingMiddleware
from src.middleware.cors_handler import setup_cors
from src.api import register_blueprints
from src.openapi import setup_openapi_routes

# Configure logging
configure_logging()
logger = get_logger(__name__)


def create_app() -> Quart:
    """
    Application factory to create and configure the Quart app.

    Returns:
        Configured Quart application instance
    """
    app = Quart(__name__)

    # Load configuration
    app.config.from_mapping(
        SECRET_KEY=settings.secret_key,
        DEBUG=settings.debug,
        TESTING=False,
    )

    logger.info(
        "Creating application",
        app_name=settings.app_name,
        environment=settings.app_env,
    )

    # Set up CORS
    setup_cors(app)

    # Register middleware
    register_middleware(app)

    # Register error handlers
    register_error_handlers(app)

    # Register API blueprints
    register_blueprints(app)

    # Register health check and root routes
    register_core_routes(app)

    # Register OpenAPI documentation routes
    setup_openapi_routes(app)

    logger.info("Application created successfully")

    return app


def register_middleware(app: Quart) -> None:
    """
    Register application middleware.

    Args:
        app: Quart application instance
    """
    # Request logging middleware
    app.before_request(RequestLoggingMiddleware.log_request)
    app.after_request(RequestLoggingMiddleware.log_response)

    logger.info("Middleware registered")


def register_core_routes(app: Quart) -> None:
    """
    Register core application routes (health check, root).

    Args:
        app: Quart application instance
    """

    @app.route("/")
    async def root() -> Dict[str, Any]:
        """Root endpoint with API information."""
        return jsonify({
            "name": settings.app_name,
            "version": "0.1.0",
            "environment": settings.app_env,
            "status": "running",
            "docs": "/docs",
            "openapi": "/openapi.json"
        })

    @app.route("/health")
    async def health_check() -> Dict[str, str]:
        """Health check endpoint for monitoring."""
        # TODO: Add database and Redis health checks
        return jsonify({
            "status": "healthy",
            "service": settings.app_name
        })

    @app.route("/ready")
    async def readiness_check() -> Dict[str, str]:
        """Readiness check endpoint for load balancers."""
        # TODO: Verify all dependencies are ready
        return jsonify({
            "status": "ready",
            "service": settings.app_name
        })

    logger.info("Core routes registered")


async def run_server() -> None:
    """Run the application server using Hypercorn."""
    app = create_app()

    # Configure Hypercorn
    config = HypercornConfig()
    config.bind = [f"{settings.host}:{settings.port}"]
    config.use_reloader = settings.debug
    config.accesslog = "-" if settings.debug else None
    config.errorlog = "-"

    logger.info(
        "Starting server",
        host=settings.host,
        port=settings.port,
        debug=settings.debug,
    )

    await serve(app, config)


def main() -> None:
    """Main entry point."""
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as error:
        logger.exception("Server error", error=str(error))
        raise


if __name__ == "__main__":
    main()
