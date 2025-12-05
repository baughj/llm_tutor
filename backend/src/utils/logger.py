"""
Centralized logging module for CodeMentor backend.
Provides structured logging with JSON formatting and context management.
"""
import logging
import sys
from typing import Any, Dict, Optional
from pythonjsonlogger import jsonlogger
import structlog
from structlog.types import EventDict


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter for log records."""

    def add_fields(
        self,
        log_record: Dict[str, Any],
        record: logging.LogRecord,
        message_dict: Dict[str, Any],
    ) -> None:
        """Add custom fields to log record."""
        super().add_fields(log_record, record, message_dict)
        log_record["timestamp"] = record.created
        log_record["level"] = record.levelname
        log_record["logger"] = record.name
        log_record["module"] = record.module
        log_record["function"] = record.funcName
        log_record["line"] = record.lineno


def setup_logging(
    log_level: str = "INFO",
    log_format: str = "json",
    app_name: str = "CodeMentor",
) -> logging.Logger:
    """
    Set up centralized logging configuration.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Output format ('json' or 'text')
        app_name: Application name for logging context

    Returns:
        Configured root logger
    """
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))

    # Set formatter based on format preference
    if log_format == "json":
        formatter = CustomJsonFormatter(
            "%(timestamp)s %(level)s %(logger)s %(module)s %(function)s %(line)s %(message)s"
        )
    else:
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Create application logger
    app_logger = logging.getLogger(app_name)
    app_logger.info(
        "Logging initialized",
        extra={"log_level": log_level, "log_format": log_format},
    )

    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.

    Args:
        name: Logger name (typically __name__ of the module)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


class LoggerMixin:
    """Mixin class to provide logging capability to any class."""

    @property
    def logger(self) -> logging.Logger:
        """Get logger instance for this class."""
        if not hasattr(self, "_logger"):
            self._logger = get_logger(self.__class__.__name__)
        return self._logger


def log_request(request: Any, response: Optional[Any] = None) -> None:
    """
    Log HTTP request and optional response details.

    Args:
        request: Quart request object
        response: Optional Quart response object
    """
    logger = get_logger("http")

    log_data = {
        "method": request.method,
        "path": request.path,
        "remote_addr": request.remote_addr,
        "user_agent": request.headers.get("User-Agent", ""),
    }

    if response:
        log_data["status_code"] = response.status_code
        logger.info("HTTP request completed", extra=log_data)
    else:
        logger.info("HTTP request received", extra=log_data)


def log_exception(exception: Exception, context: Optional[Dict[str, Any]] = None) -> None:
    """
    Log exception with context information.

    Args:
        exception: Exception instance
        context: Optional context dictionary
    """
    logger = get_logger("exception")

    log_data = {
        "exception_type": type(exception).__name__,
        "exception_message": str(exception),
    }

    if context:
        log_data.update(context)

    logger.error("Exception occurred", exc_info=True, extra=log_data)


def log_database_query(query: str, duration_ms: float, success: bool = True) -> None:
    """
    Log database query execution.

    Args:
        query: SQL query string
        duration_ms: Query execution duration in milliseconds
        success: Whether query succeeded
    """
    logger = get_logger("database")

    log_data = {
        "query": query[:200],  # Truncate long queries
        "duration_ms": duration_ms,
        "success": success,
    }

    if success:
        logger.debug("Database query executed", extra=log_data)
    else:
        logger.warning("Database query failed", extra=log_data)


def log_llm_request(
    provider: str,
    model: str,
    prompt_tokens: int,
    completion_tokens: int,
    duration_ms: float,
) -> None:
    """
    Log LLM API request details.

    Args:
        provider: LLM provider name (openai, anthropic, etc.)
        model: Model identifier
        prompt_tokens: Number of tokens in prompt
        completion_tokens: Number of tokens in completion
        duration_ms: Request duration in milliseconds
    """
    logger = get_logger("llm")

    log_data = {
        "provider": provider,
        "model": model,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens,
        "duration_ms": duration_ms,
    }

    logger.info("LLM request completed", extra=log_data)
