"""
Unit tests for GROQ provider.
"""
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from groq import BadRequestError, RateLimitError, AuthenticationError

from src.services.llm import (
    GroqProvider,
    LLMRequest,
    Message,
    InvalidRequestError,
    RateLimitError as CustomRateLimitError,
    AuthenticationError as CustomAuthenticationError,
)
from src.config import settings
from src.utils.logger import get_logger


@pytest.fixture
def logger():
    """Create a mock logger."""
    return get_logger("test_groq_provider")


@pytest.fixture
def groq_provider(logger):
    """Create a GROQ provider instance."""
    return GroqProvider(
        api_key=settings.groq_api_key,
        logger=logger,
        model=settings.groq_model,
        max_retries=3,
        timeout=30,
    )


@pytest.mark.asyncio
async def test_provider_initialization(groq_provider):
    """Test GROQ provider initialization."""
    assert groq_provider.model == settings.groq_model
    assert groq_provider.max_retries == 3
    assert groq_provider.timeout == 30
    assert groq_provider.client is not None


@pytest.mark.asyncio
async def test_calculate_cost(groq_provider):
    """Test cost calculation."""
    # Test with default model
    cost = groq_provider.calculate_cost(1000, 500)

    # llama-3.3-70b-versatile: $0.59 prompt, $0.79 completion per 1M tokens
    expected = (1000 / 1_000_000) * 0.59 + (500 / 1_000_000) * 0.79
    assert abs(cost - expected) < 0.000001


@pytest.mark.asyncio
async def test_get_rate_limits(groq_provider):
    """Test rate limits retrieval."""
    limits = groq_provider.get_rate_limits()

    assert "requests_per_minute" in limits
    assert "requests_per_day" in limits
    assert limits["requests_per_minute"] == 30
    assert limits["requests_per_day"] == 14400


@pytest.mark.asyncio
async def test_count_tokens(groq_provider):
    """Test token counting estimation."""
    text = "This is a test message with some words."
    tokens = await groq_provider.count_tokens(text)

    # Rough estimate: ~4 characters per token
    expected_tokens = len(text) // 4
    assert tokens == expected_tokens


@pytest.mark.asyncio
@pytest.mark.integration
async def test_basic_completion(groq_provider):
    """Test basic completion generation."""
    request = LLMRequest(
        messages=[
            Message(role="user", content="Say 'test' and nothing else."),
        ],
        max_tokens=10,
    )

    response = await groq_provider.generate_completion(request)

    assert response is not None
    assert response.content is not None
    assert len(response.content) > 0
    assert response.provider == "groq"
    assert response.model == settings.groq_model
    assert response.tokens_used > 0
    assert response.cost_usd > 0
    assert response.response_time_ms > 0


@pytest.mark.asyncio
@pytest.mark.integration
async def test_completion_with_system_prompt(groq_provider):
    """Test completion with system prompt."""
    request = LLMRequest(
        messages=[
            Message(role="user", content="What is 5+5?"),
        ],
        system_prompt="You are a math tutor. Be very concise.",
        max_tokens=50,
    )

    response = await groq_provider.generate_completion(request)

    assert response is not None
    assert "10" in response.content


@pytest.mark.asyncio
@pytest.mark.integration
async def test_completion_with_temperature(groq_provider):
    """Test completion with different temperature."""
    request = LLMRequest(
        messages=[
            Message(role="user", content="Say hello"),
        ],
        temperature=0.1,  # Low temperature for more deterministic output
        max_tokens=20,
    )

    response = await groq_provider.generate_completion(request)

    assert response is not None
    assert len(response.content) > 0


@pytest.mark.asyncio
@pytest.mark.integration
async def test_multi_turn_conversation(groq_provider):
    """Test multi-turn conversation."""
    request = LLMRequest(
        messages=[
            Message(role="user", content="My name is Alice."),
            Message(role="assistant", content="Nice to meet you, Alice!"),
            Message(role="user", content="What's my name?"),
        ],
        max_tokens=50,
    )

    response = await groq_provider.generate_completion(request)

    assert response is not None
    assert "alice" in response.content.lower()


@pytest.mark.asyncio
async def test_retry_on_rate_limit():
    """Test retry logic on rate limit error."""
    logger = get_logger("test_retry")
    provider = GroqProvider(
        api_key="test_key",
        logger=logger,
        max_retries=2,
    )

    # Mock the client to raise RateLimitError then succeed
    mock_response = Mock()
    mock_response.choices = [Mock(message=Mock(content="Success"), finish_reason="stop")]
    mock_response.usage = Mock(prompt_tokens=10, completion_tokens=20, total_tokens=30)

    call_count = 0

    async def mock_create(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise RateLimitError("Rate limit exceeded", response=Mock(status_code=429), body=None)
        return mock_response

    provider.client.chat.completions.create = mock_create

    request = LLMRequest(
        messages=[Message(role="user", content="test")],
    )

    response = await provider.generate_completion(request)

    assert call_count == 2  # Should have retried once
    assert response.content == "Success"


@pytest.mark.asyncio
async def test_authentication_error():
    """Test authentication error handling."""
    logger = get_logger("test_auth_error")
    provider = GroqProvider(
        api_key="invalid_key",
        logger=logger,
    )

    # Mock the client to raise AuthenticationError
    async def mock_create(*args, **kwargs):
        raise AuthenticationError("Invalid API key", response=Mock(status_code=401), body=None)

    provider.client.chat.completions.create = mock_create

    request = LLMRequest(
        messages=[Message(role="user", content="test")],
    )

    with pytest.raises(CustomAuthenticationError):
        await provider.generate_completion(request)


@pytest.mark.asyncio
async def test_invalid_request_error():
    """Test invalid request error handling."""
    logger = get_logger("test_invalid_request")
    provider = GroqProvider(
        api_key="test_key",
        logger=logger,
    )

    # Mock the client to raise BadRequestError
    async def mock_create(*args, **kwargs):
        raise BadRequestError("Invalid model", response=Mock(status_code=400), body=None)

    provider.client.chat.completions.create = mock_create

    request = LLMRequest(
        messages=[Message(role="user", content="test")],
    )

    with pytest.raises(InvalidRequestError):
        await provider.generate_completion(request)


@pytest.mark.asyncio
async def test_exponential_backoff():
    """Test exponential backoff timing."""
    logger = get_logger("test_backoff")
    provider = GroqProvider(
        api_key="test_key",
        logger=logger,
        max_retries=3,
    )

    call_times = []

    async def mock_create(*args, **kwargs):
        call_times.append(asyncio.get_event_loop().time())
        raise RateLimitError("Rate limit", response=Mock(status_code=429), body=None)

    provider.client.chat.completions.create = mock_create

    request = LLMRequest(
        messages=[Message(role="user", content="test")],
    )

    with pytest.raises(CustomRateLimitError):
        await provider.generate_completion(request)

    # Should have 3 attempts
    assert len(call_times) == 3

    # Check backoff times (approximately 2^0=1s, 2^1=2s)
    if len(call_times) >= 2:
        time_diff_1 = call_times[1] - call_times[0]
        assert 0.9 < time_diff_1 < 1.5  # ~1 second with some tolerance

    if len(call_times) >= 3:
        time_diff_2 = call_times[2] - call_times[1]
        assert 1.9 < time_diff_2 < 2.5  # ~2 seconds with some tolerance
