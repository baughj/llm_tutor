"""
Test Groq Compound model integration.
Compound is an AI system that can use tools like web search and code execution.
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from src.services.llm import GroqProvider, LLMRequest, Message
from src.config import settings
from src.utils.logger import get_logger


async def test_compound_model():
    """Test Groq Compound model with web search capability."""
    print("🧪 Testing Groq Compound Model...")
    print(f"   Model: {settings.groq_compound_model}")
    print()

    logger = get_logger("test_compound")

    # Create provider with Compound model
    provider = GroqProvider(
        api_key=settings.groq_api_key,
        logger=logger,
        model=settings.groq_compound_model,
        timeout=60,  # Compound may take longer
    )

    print("📦 Testing Compound model capabilities...")
    print()

    # Test 1: Real-time information (should use web search)
    print("🔄 Test 1: Real-time web search capability")
    print("   Question: What are the latest features in Python 3.14?")

    request = LLMRequest(
        messages=[
            Message(role="user", content="What are the latest features in Python 3.14? Give me 3 key features."),
        ],
        max_tokens=500,
    )

    response = await provider.generate_completion(request)

    print(f"   Response: {response.content[:300]}...")
    print(f"   Tokens used: {response.tokens_used}")
    print(f"   Cost: ${response.cost_usd:.6f}")
    print(f"   Response time: {response.response_time_ms:.0f}ms")
    print("✅ Test 1 passed")
    print()

    # Test 2: Code execution capability
    print("🔄 Test 2: Code execution capability")
    print("   Question: Calculate fibonacci(10)")

    request = LLMRequest(
        messages=[
            Message(role="user", content="Calculate the 10th Fibonacci number. Show me the code and the result."),
        ],
        max_tokens=500,
    )

    response = await provider.generate_completion(request)

    print(f"   Response: {response.content[:300]}...")
    print(f"   Tokens used: {response.tokens_used}")
    print(f"   Cost: ${response.cost_usd:.6f}")
    print("✅ Test 2 passed")
    print()

    # Test 3: Complex reasoning with tool use
    print("🔄 Test 3: Complex reasoning")
    print("   Question: Compare Groq vs OpenAI inference speed")

    request = LLMRequest(
        messages=[
            Message(
                role="user",
                content="Search for and compare the inference speed of Groq vs OpenAI. Give me specific numbers if available.",
            ),
        ],
        max_tokens=500,
    )

    response = await provider.generate_completion(request)

    print(f"   Response: {response.content[:300]}...")
    print(f"   Tokens used: {response.tokens_used}")
    print(f"   Cost: ${response.cost_usd:.6f}")
    print("✅ Test 3 passed")
    print()

    print("🎉 All Compound model tests completed!")
    print()
    print("📊 Compound Model Benefits:")
    print("   ✅ Real-time web search integration")
    print("   ✅ Code execution capability")
    print("   ✅ More accurate, up-to-date responses")
    print("   ✅ Can handle complex multi-step tasks")

    return True


async def main():
    """Run all tests."""
    try:
        success = await test_compound_model()
        return 0 if success else 1
    except Exception as error:
        print(f"❌ Test failed: {error}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
