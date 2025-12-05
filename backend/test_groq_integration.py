"""
Quick integration test for GROQ service.
This script tests the basic GROQ integration to ensure everything works.
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from src.services.llm import create_llm_service, Message
from src.config import settings
from src.utils.logger import get_logger


async def test_basic_completion():
    """Test basic GROQ completion."""
    print("🧪 Testing GROQ Integration...")
    print(f"   Model: {settings.groq_model}")
    print(f"   Rate Limit: {settings.groq_rate_limit_rpm} RPM")
    print()

    # Create service without caching/rate limiting for simplicity
    print("📦 Creating LLM service...")
    service = await create_llm_service(
        enable_caching=False,
        enable_rate_limiting=False,
    )
    print("✅ Service created successfully")
    print()

    # Test 1: Simple completion
    print("🔄 Test 1: Simple completion")
    messages = [
        Message(role="user", content="Say 'Hello from GROQ!' and nothing else."),
    ]

    response = await service.generate_completion(
        messages=messages,
        max_tokens=50,
    )

    print(f"   Response: {response.content}")
    print(f"   Tokens used: {response.tokens_used}")
    print(f"   Cost: ${response.cost_usd:.6f}")
    print(f"   Response time: {response.response_time_ms:.0f}ms")
    print("✅ Test 1 passed")
    print()

    # Test 2: With system prompt
    print("🔄 Test 2: With system prompt")
    messages = [
        Message(role="user", content="What is 2+2?"),
    ]

    response = await service.generate_completion(
        messages=messages,
        system_prompt="You are a helpful math tutor. Be very concise.",
        max_tokens=50,
    )

    print(f"   Response: {response.content}")
    print(f"   Tokens used: {response.tokens_used}")
    print(f"   Cost: ${response.cost_usd:.6f}")
    print("✅ Test 2 passed")
    print()

    # Test 3: Prompt template
    print("🔄 Test 3: Using prompt template")
    from src.services.llm import PromptTemplateManager

    system_prompt, user_prompt = PromptTemplateManager.create_tutor_message(
        student_name="Test User",
        language="Python",
        skill_level="Beginner",
        career_goal="Web Developer",
    )

    messages = [
        Message(role="user", content=user_prompt),
    ]

    response = await service.generate_completion(
        messages=messages,
        system_prompt=system_prompt,
        max_tokens=200,
    )

    print(f"   Response: {response.content[:200]}...")
    print(f"   Tokens used: {response.tokens_used}")
    print(f"   Cost: ${response.cost_usd:.6f}")
    print("✅ Test 3 passed")
    print()

    print("🎉 All tests passed! GROQ integration is working correctly.")
    return True


async def main():
    """Run all tests."""
    try:
        success = await test_basic_completion()
        return 0 if success else 1
    except Exception as error:
        print(f"❌ Test failed: {error}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
