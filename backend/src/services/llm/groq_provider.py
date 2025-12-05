"""
GROQ LLM provider implementation for CodeMentor.
Implements the BaseLLMProvider interface for GROQ API.
"""
import asyncio
import time
from typing import Dict, Optional
from datetime import datetime
from groq import AsyncGroq
import groq

from .base_provider import (
    BaseLLMProvider,
    LLMRequest,
    LLMResponse,
    Message,
    LLMProviderError,
    RateLimitError,
    AuthenticationError,
    InvalidRequestError,
    TimeoutError,
)


class GroqProvider(BaseLLMProvider):
    """GROQ LLM provider implementation."""

    # GROQ pricing per 1M tokens (as of December 2025)
    PRICING = {
        "llama-3.3-70b-versatile": {
            "prompt": 0.59,  # per 1M tokens
            "completion": 0.79,  # per 1M tokens
        },
        "llama-3.1-70b-versatile": {
            "prompt": 0.59,
            "completion": 0.79,
        },
        "llama-3.1-8b-instant": {
            "prompt": 0.05,
            "completion": 0.08,
        },
        "mixtral-8x7b-32768": {  # Deprecated
            "prompt": 0.27,
            "completion": 0.27,
        },
    }

    def __init__(
        self,
        api_key: str,
        logger,
        model: str = "llama-3.3-70b-versatile",
        max_retries: int = 3,
        timeout: int = 30,
        rate_limit_rpm: int = 30,
        rate_limit_rpd: int = 14400,
    ):
        """
        Initialize GROQ provider.

        Args:
            api_key: GROQ API key
            logger: Logger instance
            model: Default model to use
            max_retries: Maximum number of retries for failed requests
            timeout: Request timeout in seconds
            rate_limit_rpm: Rate limit requests per minute
            rate_limit_rpd: Rate limit requests per day
        """
        super().__init__(api_key, logger)
        self.model = model
        self.max_retries = max_retries
        self.timeout = timeout
        self.rate_limit_rpm = rate_limit_rpm
        self.rate_limit_rpd = rate_limit_rpd

        # Initialize GROQ client
        self.client = AsyncGroq(api_key=api_key, timeout=timeout)

        self.logger.info(
            "GROQ provider initialized",
            extra={
                "model": model,
                "max_retries": max_retries,
                "timeout": timeout,
                "rate_limit_rpm": rate_limit_rpm,
            },
        )

    async def generate_completion(self, request: LLMRequest) -> LLMResponse:
        """
        Generate a completion from GROQ.

        Args:
            request: The LLM request containing messages and parameters

        Returns:
            LLMResponse object containing the response and metadata

        Raises:
            LLMProviderError: If the request fails after retries
        """
        start_time = time.time()
        model = request.model or self.model
        temperature = request.temperature if request.temperature is not None else 0.7
        max_tokens = request.max_tokens or 2000

        # Convert messages to GROQ format
        messages = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})

        for msg in request.messages:
            messages.append({"role": msg.role, "content": msg.content})

        # Retry logic with exponential backoff
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                self.logger.debug(
                    "GROQ request attempt",
                    extra={
                        "attempt": attempt + 1,
                        "model": model,
                        "messages_count": len(messages),
                    },
                )

                # Make the API call
                response = await self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

                # Calculate response time
                response_time_ms = (time.time() - start_time) * 1000

                # Extract token usage
                prompt_tokens = response.usage.prompt_tokens
                completion_tokens = response.usage.completion_tokens
                total_tokens = response.usage.total_tokens

                # Calculate cost
                cost = self.calculate_cost(prompt_tokens, completion_tokens)

                # Build response
                llm_response = LLMResponse(
                    content=response.choices[0].message.content,
                    model=model,
                    provider="groq",
                    tokens_used=total_tokens,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    finish_reason=response.choices[0].finish_reason,
                    response_time_ms=response_time_ms,
                    timestamp=datetime.utcnow(),
                    cost_usd=cost,
                    cached=False,
                )

                self.logger.info(
                    "GROQ request success",
                    extra={
                        "model": model,
                        "tokens_used": total_tokens,
                        "cost_usd": cost,
                        "response_time_ms": response_time_ms,
                    },
                )

                return llm_response

            except groq.RateLimitError as error:
                last_exception = error
                self.logger.warning(
                    "GROQ rate limit exceeded",
                    extra={
                        "attempt": attempt + 1,
                        "error": str(error),
                    },
                )

                if attempt < self.max_retries - 1:
                    # Exponential backoff: 2^attempt seconds
                    backoff_time = 2**attempt
                    self.logger.info(
                        "GROQ retry backoff",
                        extra={
                            "attempt": attempt + 1,
                            "backoff_seconds": backoff_time,
                        },
                    )
                    await asyncio.sleep(backoff_time)
                else:
                    raise RateLimitError(f"GROQ rate limit exceeded: {error}")

            except groq.AuthenticationError as error:
                last_exception = error
                self.logger.error("GROQ authentication error", extra={"error": str(error)})
                raise AuthenticationError(f"GROQ authentication failed: {error}")

            except groq.BadRequestError as error:
                last_exception = error
                self.logger.error(
                    "GROQ invalid request",
                    extra={
                        "error": str(error),
                        "messages_count": len(messages),
                    },
                )
                raise InvalidRequestError(f"Invalid GROQ request: {error}")

            except asyncio.TimeoutError as error:
                last_exception = error
                self.logger.warning(
                    "GROQ timeout",
                    extra={
                        "attempt": attempt + 1,
                        "timeout": self.timeout,
                    },
                )

                if attempt < self.max_retries - 1:
                    backoff_time = 2**attempt
                    await asyncio.sleep(backoff_time)
                else:
                    raise TimeoutError(f"GROQ request timeout after {self.max_retries} attempts")

            except Exception as error:
                last_exception = error
                self.logger.error(
                    "GROQ unexpected error",
                    extra={
                        "attempt": attempt + 1,
                        "error": str(error),
                        "error_type": type(error).__name__,
                    },
                )

                if attempt < self.max_retries - 1:
                    backoff_time = 2**attempt
                    await asyncio.sleep(backoff_time)
                else:
                    raise LLMProviderError(f"GROQ request failed: {error}")

        # Should not reach here, but just in case
        raise LLMProviderError(f"GROQ request failed after {self.max_retries} attempts: {last_exception}")

    async def count_tokens(self, text: str) -> int:
        """
        Estimate the number of tokens in a text.

        Note: GROQ doesn't provide a token counting API, so we use a rough estimate.
        For more accurate counting, consider using tiktoken library.

        Args:
            text: The text to count tokens for

        Returns:
            Estimated number of tokens
        """
        # Rough estimate: ~4 characters per token
        # This is a simplification and should be improved with tiktoken
        estimated_tokens = len(text) // 4
        return estimated_tokens

    def calculate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        """
        Calculate the cost of a request in USD.

        Args:
            prompt_tokens: Number of prompt tokens
            completion_tokens: Number of completion tokens

        Returns:
            Cost in USD
        """
        model_pricing = self.PRICING.get(self.model, self.PRICING["llama-3.3-70b-versatile"])

        prompt_cost = (prompt_tokens / 1_000_000) * model_pricing["prompt"]
        completion_cost = (completion_tokens / 1_000_000) * model_pricing["completion"]

        total_cost = prompt_cost + completion_cost
        return round(total_cost, 6)

    def get_rate_limits(self) -> Dict[str, int]:
        """
        Get the rate limits for GROQ provider.

        Returns:
            Dictionary with rate limit information
        """
        return {
            "requests_per_minute": self.rate_limit_rpm,
            "requests_per_day": self.rate_limit_rpd,
        }
