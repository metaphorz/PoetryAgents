# Test Organization

This directory contains tests organized into two categories:

## `/auto/` - Automatic Tests
These are tests created and performed automatically by Claude Code. They verify system functionality, features, and regression testing.

**Current automatic tests:**
- `test_ascii_art.py` - Tests ASCII art generation functionality
- `test_dual_llm.py` - Tests dual LLM (Claude + Gemini) poetry generation
- `test_emoji_enhancement.py` - Tests emoji integration in poetry
- `test_form_specific_lengths.py` - Tests form-dependent length handling
- `test_gemini.py` - Tests Gemini API connection and poetry generation
- `test_llm_combinations.py` - Tests all possible LLM combinations
- `test_markdown_output.py` - Tests markdown file generation
- `test_personas.py` - Tests literary character persona system
- `test_poetry_formats.py` - Tests different poetry forms (haiku, sonnet, etc.)
- `test_question_flow.py` - Documents the user interface question flow
- `test_simplified_interface.py` - Tests simplified interface (always 2 agents)
- `test_system.py` - System-wide integration tests

## `/user/` - User-Specified Tests
These are tests manually specified by the user for specific scenarios or validation needs.

**To run automatic tests:**
```bash
python tests/auto/test_name.py
```

**To add user tests:**
Place custom test files in `tests/user/` directory.