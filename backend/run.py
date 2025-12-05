"""
Main entry point for CodeMentor backend application.
Runs the Quart server using Hypercorn.
"""
import asyncio
import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from hypercorn.asyncio import serve
from hypercorn.config import Config as HypercornConfig

from src.app import create_app, shutdown_app
from src.config import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


async def main():
    """Main async function to run the application."""
    # Create application instance
    app = create_app()

    # Configure Hypercorn server
    config = HypercornConfig()
    config.bind = [f"{settings.host}:{settings.port}"]
    config.accesslog = "-"  # Log to stdout
    config.errorlog = "-"  # Log to stdout
    config.worker_class = "asyncio"
    config.workers = 1  # Single worker for development

    logger.info(
        "Starting CodeMentor backend server",
        extra={
            "host": settings.host,
            "port": settings.port,
            "environment": settings.app_env,
            "debug": settings.debug,
        },
    )

    try:
        # Run server
        await serve(app, config)
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
    finally:
        # Cleanup
        await shutdown_app(app)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as exception:
        logger.error(
            "Fatal error running application",
            exc_info=True,
            extra={"exception": str(exception)},
        )
        sys.exit(1)
