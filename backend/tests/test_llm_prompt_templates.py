"""
Tests for prompt template system.
"""
import pytest

from src.services.llm import PromptTemplateManager, PromptType


def test_get_system_prompt():
    """Test getting system prompts."""
    # Test tutor greeting prompt
    prompt = PromptTemplateManager.get_system_prompt(PromptType.TUTOR_GREETING)
    assert len(prompt) > 0
    assert "coding tutor" in prompt.lower()

    # Test exercise generation prompt
    prompt = PromptTemplateManager.get_system_prompt(PromptType.EXERCISE_GENERATION)
    assert len(prompt) > 0
    assert "exercise" in prompt.lower()


def test_render_prompt_tutor_greeting():
    """Test rendering tutor greeting prompt."""
    prompt = PromptTemplateManager.render_prompt(
        PromptType.TUTOR_GREETING,
        student_name="Alice",
        language="Python",
        skill_level="Beginner",
        career_goal="Web Developer",
    )

    assert "Alice" in prompt
    assert "Python" in prompt
    assert "Beginner" in prompt
    assert "Web Developer" in prompt


def test_render_prompt_exercise_generation():
    """Test rendering exercise generation prompt."""
    prompt = PromptTemplateManager.render_prompt(
        PromptType.EXERCISE_GENERATION,
        language="JavaScript",
        skill_level="Intermediate",
        interests="Frontend Development",
        recent_topics="React Hooks",
        difficulty="medium",
        estimated_time=45,
    )

    assert "JavaScript" in prompt
    assert "Intermediate" in prompt
    assert "Frontend Development" in prompt
    assert "React Hooks" in prompt
    assert "medium" in prompt
    assert "45" in prompt


def test_render_prompt_code_review():
    """Test rendering code review prompt."""
    code = "def hello():\n    print('hello')"
    prompt = PromptTemplateManager.render_prompt(
        PromptType.CODE_REVIEW,
        repository_url="https://github.com/user/repo",
        language="Python",
        files="app.py",
        code=code,
        skill_level="Beginner",
        learning_goals="Learn Python best practices",
    )

    assert "github.com/user/repo" in prompt
    assert "Python" in prompt
    assert "app.py" in prompt
    assert code in prompt
    assert "Beginner" in prompt
    assert "best practices" in prompt


def test_render_prompt_missing_parameter():
    """Test that missing parameters raise error."""
    with pytest.raises(KeyError):
        PromptTemplateManager.render_prompt(
            PromptType.TUTOR_GREETING,
            student_name="Alice",
            # Missing required parameters
        )


def test_create_tutor_message():
    """Test create_tutor_message helper."""
    system_prompt, user_prompt = PromptTemplateManager.create_tutor_message(
        student_name="Bob",
        language="Java",
        skill_level="Advanced",
        career_goal="Backend Engineer",
    )

    assert len(system_prompt) > 0
    assert "tutor" in system_prompt.lower()

    assert "Bob" in user_prompt
    assert "Java" in user_prompt
    assert "Advanced" in user_prompt
    assert "Backend Engineer" in user_prompt


def test_create_exercise_prompt():
    """Test create_exercise_prompt helper."""
    system_prompt, user_prompt = PromptTemplateManager.create_exercise_prompt(
        language="Python",
        skill_level="Beginner",
        interests="Data Science",
        recent_topics="Pandas",
        difficulty="easy",
        estimated_time=30,
    )

    assert len(system_prompt) > 0
    assert "exercise" in system_prompt.lower()

    assert "Python" in user_prompt
    assert "Beginner" in user_prompt
    assert "Data Science" in user_prompt
    assert "Pandas" in user_prompt
    assert "easy" in user_prompt
    assert "30" in user_prompt


def test_create_exercise_prompt_defaults():
    """Test create_exercise_prompt with default parameters."""
    system_prompt, user_prompt = PromptTemplateManager.create_exercise_prompt(
        language="Ruby",
        skill_level="Intermediate",
        interests="Web Development",
    )

    assert "Ruby" in user_prompt
    assert "Intermediate" in user_prompt
    assert "Web Development" in user_prompt
    assert "medium" in user_prompt  # Default difficulty
    assert "30" in user_prompt  # Default time


def test_create_code_review_prompt():
    """Test create_code_review_prompt helper."""
    code_sample = """
    function add(a, b) {
        return a + b;
    }
    """

    system_prompt, user_prompt = PromptTemplateManager.create_code_review_prompt(
        repository_url="https://github.com/test/repo",
        language="JavaScript",
        files="utils.js",
        code=code_sample,
        skill_level="Intermediate",
        learning_goals="Learn clean code practices",
    )

    assert len(system_prompt) > 0
    assert "review" in system_prompt.lower()

    assert "github.com/test/repo" in user_prompt
    assert "JavaScript" in user_prompt
    assert "utils.js" in user_prompt
    assert "function add" in user_prompt
    assert "Intermediate" in user_prompt
    assert "clean code" in user_prompt


def test_all_prompt_types_have_templates():
    """Test that all prompt types have templates."""
    for prompt_type in PromptType:
        # Should not raise exception
        system_prompt = PromptTemplateManager.get_system_prompt(prompt_type)
        assert len(system_prompt) > 0


def test_prompt_consistency():
    """Test that prompts are consistent across calls."""
    params = {
        "student_name": "Test User",
        "language": "Python",
        "skill_level": "Beginner",
        "career_goal": "Developer",
    }

    prompt1 = PromptTemplateManager.render_prompt(PromptType.TUTOR_GREETING, **params)
    prompt2 = PromptTemplateManager.render_prompt(PromptType.TUTOR_GREETING, **params)

    assert prompt1 == prompt2
