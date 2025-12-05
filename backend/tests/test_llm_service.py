"""
Integration tests for LLM service.
"""
import pytest
import redis.asyncio as aioredis

from src.services.llm import (
    Message,
    LLMRequest,
    GroqProvider,
    LLMService,
    create_llm_service,
    PromptTemplateManager,
    PromptType,
    RateLimitError,
)
from src.config import settings
from src.utils.logger import get_logger


@pytest.fixture
async def redis_client():
    """Create a Redis client for testing."""
    client = await aioredis.from_url(
        "redis://localhost:6379/15",  # Use test database
        encoding="utf-8",
        decode_responses=True,
    )
    # Clean up before tests
    await client.flushdb()
    yield client
    # Clean up after tests
    await client.flushdb()
    await client.close()


@pytest.mark.asyncio
@pytest.mark.integration
async def test_groq_provider_basic():
    """Test basic GROQ provider functionality."""
    logger = get_logger("test_groq")

    provider = GroqProvider(
        api_key=settings.groq_api_key,
        logger=logger,
        model=settings.groq_model,
    )

    request = LLMRequest(
        messages=[
            Message(role="user", content="Say 'Hello, World!' and nothing else."),
        ],
        max_tokens=50,
    )

    response = await provider.generate_completion(request)

    assert response is not None
    assert response.content is not None
    assert len(response.content) > 0
    assert response.provider == "groq"
    assert response.tokens_used > 0
    assert response.cost_usd >= 0


@pytest.mark.asyncio
@pytest.mark.integration
async def test_groq_provider_with_system_prompt():
    """Test GROQ provider with system prompt."""
    logger = get_logger("test_groq")

    provider = GroqProvider(
        api_key=settings.groq_api_key,
        logger=logger,
        model=settings.groq_model,
    )

    request = LLMRequest(
        messages=[
            Message(role="user", content="What is 2+2?"),
        ],
        system_prompt="You are a helpful math tutor. Be concise.",
        max_tokens=100,
    )

    response = await provider.generate_completion(request)

    assert response is not None
    assert "4" in response.content


@pytest.mark.asyncio
async def test_prompt_template_system():
    """Test prompt template system."""
    system_prompt, user_prompt = PromptTemplateManager.create_tutor_message(
        student_name="Alice",
        language="Python",
        skill_level="Beginner",
        career_goal="Web Developer",
    )

    assert "Alice" in user_prompt
    assert "Python" in user_prompt
    assert "Beginner" in user_prompt
    assert "Web Developer" in user_prompt
    assert len(system_prompt) > 0


@pytest.mark.asyncio
async def test_prompt_template_exercise():
    """Test exercise generation prompt template."""
    system_prompt, user_prompt = PromptTemplateManager.create_exercise_prompt(
        language="JavaScript",
        skill_level="Intermediate",
        interests="Frontend Development",
        difficulty="medium",
    )

    assert "JavaScript" in user_prompt
    assert "Intermediate" in user_prompt
    assert "Frontend Development" in user_prompt
    assert len(system_prompt) > 0


@pytest.mark.asyncio
async def test_llm_service_creation():
    """Test LLM service factory."""
    service = await create_llm_service(
        enable_caching=False,
        enable_rate_limiting=False,
    )

    assert service is not None
    assert service.primary_provider is not None


@pytest.mark.asyncio
@pytest.mark.integration
async def test_llm_service_completion():
    """Test LLM service completion generation."""
    service = await create_llm_service(
        enable_caching=False,
        enable_rate_limiting=False,
    )

    messages = [
        Message(role="user", content="Say 'test passed' and nothing else."),
    ]

    response = await service.generate_completion(
        messages=messages,
        max_tokens=50,
    )

    assert response is not None
    assert response.content is not None
    assert len(response.content) > 0
    assert not response.cached


@pytest.mark.asyncio
@pytest.mark.integration
async def test_llm_service_with_caching(redis_client):
    """Test LLM service with caching enabled."""
    logger = get_logger("test_cache")

    provider = GroqProvider(
        api_key=settings.groq_api_key,
        logger=logger,
        model=settings.groq_model,
    )

    service = LLMService(
        groq_provider=provider,
        redis_client=redis_client,
        logger=logger,
        enable_caching=True,
        enable_rate_limiting=False,
    )

    messages = [
        Message(role="user", content="Say 'cached test' and nothing else."),
    ]

    # First request - should not be cached
    response1 = await service.generate_completion(
        messages=messages,
        max_tokens=50,
    )

    assert response1 is not None
    assert not response1.cached

    # Second request - should be cached
    response2 = await service.generate_completion(
        messages=messages,
        max_tokens=50,
    )

    assert response2 is not None
    assert response2.cached
    assert response2.content == response1.content


@pytest.mark.asyncio
@pytest.mark.integration
async def test_llm_service_with_rate_limiting(redis_client):
    """Test LLM service with rate limiting."""
    logger = get_logger("test_ratelimit")

    provider = GroqProvider(
        api_key=settings.groq_api_key,
        logger=logger,
        model=settings.groq_model,
        rate_limit_rpm=2,  # Very low limit for testing
        rate_limit_rpd=100,
    )

    service = LLMService(
        groq_provider=provider,
        redis_client=redis_client,
        logger=logger,
        enable_caching=False,
        enable_rate_limiting=True,
    )

    messages = [Message(role="user", content="test")]

    # First two requests should succeed
    await service.generate_completion(messages=messages, user_id="test_user", max_tokens=10)
    await service.generate_completion(messages=messages, user_id="test_user", max_tokens=10)

    # Third request should be rate limited
    with pytest.raises(RateLimitError):
        await service.generate_completion(messages=messages, user_id="test_user", max_tokens=10)


@pytest.mark.asyncio
async def test_llm_service_get_user_usage(redis_client):
    """Test getting user usage statistics."""
    logger = get_logger("test_usage")

    provider = GroqProvider(
        api_key=settings.groq_api_key,
        logger=logger,
        model=settings.groq_model,
    )

    service = LLMService(
        groq_provider=provider,
        redis_client=redis_client,
        logger=logger,
        enable_caching=False,
        enable_rate_limiting=True,
    )

    # Get usage for a user who hasn't made requests
    usage = await service.get_user_usage("new_user")

    assert "requests_this_minute" in usage
    assert "requests_today" in usage
    assert "limits" in usage
    assert usage["requests_this_minute"] == 0
    assert usage["requests_today"] == 0


@pytest.mark.asyncio
@pytest.mark.integration
async def test_llm_service_context_trimming():
    """Test context trimming with long conversations."""
    service = await create_llm_service(
        enable_caching=False,
        enable_rate_limiting=False,
    )

    # Create a long conversation
    messages = []
    for i in range(15):
        messages.append(Message(role="user", content=f"Message {i}"))
        messages.append(Message(role="assistant", content=f"Response {i}"))

    messages.append(Message(role="user", content="What is the last number you saw?"))

    # Should trim to last 10 messages and still work
    response = await service.generate_completion(
        messages=messages,
        max_tokens=50,
        trim_context=True,
    )

    assert response is not None
    assert len(response.content) > 0
