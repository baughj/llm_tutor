"""
Base LLM provider abstraction for CodeMentor.
Defines the interface that all LLM providers must implement.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Message:
    """Represents a chat message."""
    role: str  # "system", "user", or "assistant"
    content: str


@dataclass
class LLMResponse:
    """Standard response format from LLM providers."""
    content: str
    model: str
    provider: str
    tokens_used: int
    prompt_tokens: int
    completion_tokens: int
    finish_reason: str
    response_time_ms: float
    timestamp: datetime
    cached: bool = False
    cost_usd: float = 0.0


@dataclass
class LLMRequest:
    """Standard request format for LLM providers."""
    messages: List[Message]
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    model: Optional[str] = None
    system_prompt: Optional[str] = None


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""

    def __init__(self, api_key: str, logger):
        """Initialize the provider with API key and logger."""
        self.api_key = api_key
        self.logger = logger
        self.provider_name = self.__class__.__name__

    @abstractmethod
    async def generate_completion(self, request: LLMRequest) -> LLMResponse:
        """
        Generate a completion from the LLM.

        Args:
            request: The LLM request containing messages and parameters

        Returns:
            LLMResponse object containing the response and metadata

        Raises:
            LLMProviderError: If the request fails
        """
        pass

    @abstractmethod
    async def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in a text.

        Args:
            text: The text to count tokens for

        Returns:
            Number of tokens
        """
        pass

    @abstractmethod
    def calculate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        """
        Calculate the cost of a request in USD.

        Args:
            prompt_tokens: Number of prompt tokens
            completion_tokens: Number of completion tokens

        Returns:
            Cost in USD
        """
        pass

    @abstractmethod
    def get_rate_limits(self) -> Dict[str, int]:
        """
        Get the rate limits for this provider.

        Returns:
            Dictionary with rate limit information
        """
        pass


class LLMProviderError(Exception):
    """Base exception for LLM provider errors."""
    pass


class RateLimitError(LLMProviderError):
    """Raised when rate limit is exceeded."""
    pass


class AuthenticationError(LLMProviderError):
    """Raised when authentication fails."""
    pass


class InvalidRequestError(LLMProviderError):
    """Raised when the request is invalid."""
    pass


class TimeoutError(LLMProviderError):
    """Raised when the request times out."""
    pass
