"""
Factory for creating LLM service instances.
"""
from typing import Optional
import redis.asyncio as aioredis

from src.config import settings
from src.utils.logger import get_logger
from .groq_provider import GroqProvider
from .llm_service import LLMService


async def create_llm_service(
    redis_client: Optional[aioredis.Redis] = None,
    enable_caching: bool = True,
    enable_rate_limiting: bool = True,
) -> LLMService:
    """
    Create and configure an LLM service instance.

    Args:
        redis_client: Redis client (will create one if not provided)
        enable_caching: Whether to enable response caching
        enable_rate_limiting: Whether to enable rate limiting

    Returns:
        Configured LLMService instance

    Raises:
        ValueError: If GROQ API key is not configured
    """
    logger = get_logger("llm_service")

    # Validate configuration
    if not settings.groq_api_key:
        raise ValueError("GROQ_API_KEY is not configured")

    # Create Redis client if not provided
    if redis_client is None and (enable_caching or enable_rate_limiting):
        redis_client = await aioredis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
        )
        logger.info("Redis client created", extra={"url": settings.redis_url})

    # Create GROQ provider
    groq_provider = GroqProvider(
        api_key=settings.groq_api_key,
        logger=logger,
        model=settings.groq_model,
        max_retries=settings.groq_max_retries,
        timeout=settings.groq_timeout,
        rate_limit_rpm=settings.groq_rate_limit_rpm,
        rate_limit_rpd=settings.groq_rate_limit_rpd,
    )

    # Create LLM service
    llm_service = LLMService(
        groq_provider=groq_provider,
        redis_client=redis_client,
        logger=logger,
        enable_caching=enable_caching,
        enable_rate_limiting=enable_rate_limiting,
    )

    logger.info(
        "LLM service created",
        extra={
            "provider": "groq",
            "model": settings.groq_model,
            "caching": enable_caching,
            "rate_limiting": enable_rate_limiting,
        },
    )

    return llm_service
