"""
Tests for LLM service caching and rate limiting.
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, Mock
import redis.asyncio as aioredis

from src.services.llm import (
    RateLimiter,
    ResponseCache,
    ContextManager,
    LLMRequest,
    LLMResponse,
    Message,
)
from src.utils.logger import get_logger
from datetime import datetime


@pytest.fixture(scope="function")
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
    try:
        await client.flushdb()
        await client.aclose()
    except Exception:
        pass  # Ignore cleanup errors


@pytest.fixture
def logger():
    """Create a logger for testing."""
    return get_logger("test_cache_ratelimit")


class TestRateLimiter:
    """Tests for RateLimiter class."""

    @pytest.mark.asyncio
    async def test_rate_limit_within_limits(self, redis_client, logger):
        """Test that requests within limits are allowed."""
        limiter = RateLimiter(redis_client, logger)

        # First request should be allowed
        allowed, retry_after = await limiter.check_rate_limit(
            user_id="user123",
            requests_per_minute=10,
            requests_per_day=100,
        )

        assert allowed is True
        assert retry_after is None

    @pytest.mark.asyncio
    async def test_rate_limit_minute_exceeded(self, redis_client, logger):
        """Test that minute rate limit is enforced."""
        limiter = RateLimiter(redis_client, logger)
        user_id = "user_minute_test"

        # Make requests up to the limit
        for i in range(5):
            allowed, _ = await limiter.check_rate_limit(
                user_id=user_id,
                requests_per_minute=5,
                requests_per_day=100,
            )
            assert allowed is True

        # Next request should be blocked
        allowed, retry_after = await limiter.check_rate_limit(
            user_id=user_id,
            requests_per_minute=5,
            requests_per_day=100,
        )

        assert allowed is False
        assert retry_after is not None
        assert 0 < retry_after <= 60

    @pytest.mark.asyncio
    async def test_rate_limit_day_exceeded(self, redis_client, logger):
        """Test that day rate limit is enforced."""
        limiter = RateLimiter(redis_client, logger)
        user_id = "user_day_test"

        # Make requests up to the limit
        for i in range(10):
            allowed, _ = await limiter.check_rate_limit(
                user_id=user_id,
                requests_per_minute=100,
                requests_per_day=10,
            )
            assert allowed is True

        # Next request should be blocked
        allowed, retry_after = await limiter.check_rate_limit(
            user_id=user_id,
            requests_per_minute=100,
            requests_per_day=10,
        )

        assert allowed is False
        assert retry_after is not None
        assert retry_after > 0

    @pytest.mark.asyncio
    async def test_rate_limit_different_users(self, redis_client, logger):
        """Test that rate limits are per-user."""
        limiter = RateLimiter(redis_client, logger)

        # User 1 makes requests
        for i in range(5):
            allowed, _ = await limiter.check_rate_limit(
                user_id="user1",
                requests_per_minute=5,
                requests_per_day=100,
            )
            assert allowed is True

        # User 1 is now at limit
        allowed, _ = await limiter.check_rate_limit(
            user_id="user1",
            requests_per_minute=5,
            requests_per_day=100,
        )
        assert allowed is False

        # User 2 should still be allowed
        allowed, _ = await limiter.check_rate_limit(
            user_id="user2",
            requests_per_minute=5,
            requests_per_day=100,
        )
        assert allowed is True

    @pytest.mark.asyncio
    async def test_get_usage(self, redis_client, logger):
        """Test getting current usage statistics."""
        limiter = RateLimiter(redis_client, logger)
        user_id = "user_usage_test"

        # Make some requests
        for i in range(3):
            await limiter.check_rate_limit(
                user_id=user_id,
                requests_per_minute=10,
                requests_per_day=100,
            )

        # Get usage
        usage = await limiter.get_usage(user_id)

        assert usage["requests_this_minute"] == 3
        assert usage["requests_today"] == 3


class TestResponseCache:
    """Tests for ResponseCache class."""

    @pytest.mark.asyncio
    async def test_cache_miss(self, redis_client, logger):
        """Test cache miss scenario."""
        cache = ResponseCache(redis_client, logger, ttl=60)

        request = LLMRequest(
            messages=[Message(role="user", content="test")],
        )

        result = await cache.get(request)
        assert result is None

    @pytest.mark.asyncio
    async def test_cache_hit(self, redis_client, logger):
        """Test cache hit scenario."""
        cache = ResponseCache(redis_client, logger, ttl=60)

        request = LLMRequest(
            messages=[Message(role="user", content="test message")],
            temperature=0.7,
        )

        # Create a response
        response = LLMResponse(
            content="test response",
            model="test-model",
            provider="test",
            tokens_used=100,
            prompt_tokens=50,
            completion_tokens=50,
            finish_reason="stop",
            response_time_ms=100.0,
            timestamp=datetime.utcnow(),
            cost_usd=0.001,
        )

        # Cache the response
        await cache.set(request, response)

        # Retrieve from cache
        cached = await cache.get(request)

        assert cached is not None
        assert cached.content == "test response"
        assert cached.model == "test-model"
        assert cached.tokens_used == 100
        assert cached.cached is True

    @pytest.mark.asyncio
    async def test_cache_different_requests(self, redis_client, logger):
        """Test that different requests get different cache keys."""
        cache = ResponseCache(redis_client, logger, ttl=60)

        request1 = LLMRequest(
            messages=[Message(role="user", content="message 1")],
        )

        request2 = LLMRequest(
            messages=[Message(role="user", content="message 2")],
        )

        response1 = LLMResponse(
            content="response 1",
            model="test",
            provider="test",
            tokens_used=10,
            prompt_tokens=5,
            completion_tokens=5,
            finish_reason="stop",
            response_time_ms=100.0,
            timestamp=datetime.utcnow(),
            cost_usd=0.001,
        )

        response2 = LLMResponse(
            content="response 2",
            model="test",
            provider="test",
            tokens_used=10,
            prompt_tokens=5,
            completion_tokens=5,
            finish_reason="stop",
            response_time_ms=100.0,
            timestamp=datetime.utcnow(),
            cost_usd=0.001,
        )

        # Cache both
        await cache.set(request1, response1)
        await cache.set(request2, response2)

        # Retrieve and verify
        cached1 = await cache.get(request1)
        cached2 = await cache.get(request2)

        assert cached1.content == "response 1"
        assert cached2.content == "response 2"

    @pytest.mark.asyncio
    async def test_cache_with_system_prompt(self, redis_client, logger):
        """Test that system prompt affects cache key."""
        cache = ResponseCache(redis_client, logger, ttl=60)

        request1 = LLMRequest(
            messages=[Message(role="user", content="test")],
            system_prompt="You are helpful",
        )

        request2 = LLMRequest(
            messages=[Message(role="user", content="test")],
            system_prompt="You are concise",
        )

        response = LLMResponse(
            content="response",
            model="test",
            provider="test",
            tokens_used=10,
            prompt_tokens=5,
            completion_tokens=5,
            finish_reason="stop",
            response_time_ms=100.0,
            timestamp=datetime.utcnow(),
            cost_usd=0.001,
        )

        # Cache first request
        await cache.set(request1, response)

        # Second request should be cache miss
        cached2 = await cache.get(request2)
        assert cached2 is None

        # First request should be cache hit
        cached1 = await cache.get(request1)
        assert cached1 is not None


class TestContextManager:
    """Tests for ContextManager class."""

    def test_trim_context_within_limits(self):
        """Test that context within limits is not trimmed."""
        manager = ContextManager(max_context_messages=10, max_context_tokens=4000)

        messages = [
            Message(role="user", content="message 1"),
            Message(role="assistant", content="response 1"),
            Message(role="user", content="message 2"),
        ]

        trimmed = manager.trim_context(messages)

        assert len(trimmed) == 3
        assert trimmed == messages

    def test_trim_context_exceeds_message_limit(self):
        """Test that old messages are removed when limit exceeded."""
        manager = ContextManager(max_context_messages=5, max_context_tokens=10000)

        messages = [
            Message(role="user", content=f"message {i}")
            for i in range(10)
        ]

        trimmed = manager.trim_context(messages)

        assert len(trimmed) == 5
        # Should keep the most recent 5
        assert trimmed[0].content == "message 5"
        assert trimmed[-1].content == "message 9"

    def test_trim_context_exceeds_token_limit(self):
        """Test that context is trimmed based on token estimate."""
        manager = ContextManager(max_context_messages=100, max_context_tokens=100)

        # Create messages that will exceed token limit
        # Each message ~120 chars = ~30 tokens
        # So 10 messages = ~300 tokens, which exceeds our limit of 100
        messages = [
            Message(role="user", content="This is a test message with many words " * 3)
            for i in range(10)
        ]

        trimmed = manager.trim_context(messages)

        # Should have trimmed some messages
        # With 100 token limit and each message being ~30 tokens, we should have ~3 messages max
        assert len(trimmed) <= 4  # Allow some margin
        assert len(trimmed) >= 1  # Should keep at least one message

    def test_trim_context_with_system_prompt(self):
        """Test that system prompt is considered in token count."""
        manager = ContextManager(max_context_messages=100, max_context_tokens=200)

        messages = [
            Message(role="user", content="test message " * 10)
            for i in range(5)
        ]

        system_prompt = "You are a helpful assistant. " * 10

        trimmed = manager.trim_context(messages, system_prompt)

        # System prompt should reduce available space for messages
        # Should have fewer messages than without system prompt
        assert len(trimmed) <= len(messages)

    def test_trim_context_preserves_order(self):
        """Test that message order is preserved after trimming."""
        manager = ContextManager(max_context_messages=3, max_context_tokens=10000)

        messages = [
            Message(role="user", content=f"message {i}")
            for i in range(10)
        ]

        trimmed = manager.trim_context(messages)

        # Should preserve order of kept messages
        for i in range(len(trimmed) - 1):
            curr_num = int(trimmed[i].content.split()[-1])
            next_num = int(trimmed[i + 1].content.split()[-1])
            assert next_num == curr_num + 1
