"""
Tests for LLM service integration.
"""
import pytest
from src.services.llm import (
    Message,
    LLMRequest,
    GroqProvider,
    create_llm_service,
    PromptTemplateManager,
    PromptType,
)
from src.config import settings
from src.utils.logger import get_logger


@pytest.mark.asyncio
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
