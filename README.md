# Poetry Agent Dialogue Generator

A system that creates poetry dialogues between AI agents using Google Gemini and Anthropic Claude, where agents respond to each other based on themes and previous poetry.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install anthropic google-generativeai python-dotenv
   ```

2. **Set up API keys:**
   Each agent can use either Google Gemini or Anthropic Claude. You can use either one, or both for agent discourse.
   
   **For Anthropic Claude:**
   - Sign up at [console.anthropic.com](https://console.anthropic.com)
   - Go to "API Keys" and create a new key
   - Add to `.env` file:
     ```
     ANTHROPIC_API_KEY=your_claude_api_key_here
     ```
   
   **For Google Gemini:**
   - Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create a new API key
   - Add to `.env` file:
     ```
     GEMINI_API_KEY=your_gemini_api_key_here
     ```

3. **Run the system:**
   ```bash
   python main.py
   ```

## Example Usage

The system asks 7 questions:
1. **Theme:** "a walk in the snow"
2. **Form:** Choose from 8 formats (haiku, prose, sonnet, villanelle, limerick, ballad, ghazal, tanka)
3. **Poem length:** Automatic for fixed forms (haiku, sonnet, etc.) or user-specified for variable forms (ballad stanzas, ghazal couplets, prose paragraphs)
4. **Conversation length:** How many rounds of conversation (each agent writes one poem per round)
5. **Agent 1 LLM:** Claude or Gemini
6. **Agent 2 LLM:** Claude or Gemini
7. **Emojis:** Whether to enhance poetry with thematic emojis

## Demo Scripts

- `python demo_run.py` - Runs the example from Requirements.md
- `python test_system.py` - Tests both haiku and prose scenarios

## Features

- **Dual LLM Support:** Choose Claude or Gemini for each agent independently
- **Poetry Forms:** 8 supported formats including:
  - **Haiku:** Traditional 5-7-5 syllable structure
  - **Prose:** Free verse poetry
  - **Sonnet:** Shakespearean 14-line ABAB CDCD EFEF GG rhyme scheme
  - **Villanelle:** 19-line form with refrains (like Dylan Thomas's "Do Not Go Gentle")
  - **Limerick:** 5-line AABBA humorous verse
  - **Ballad:** Narrative quatrains telling stories
  - **Ghazal:** Persian/Urdu form with repeated radif (ending phrase)
  - **Tanka:** Japanese 5-7-5-7-7 syllable structure
- **Literary Personas:** 35+ detailed character profiles with source literature and qualities
- **Agent Names:** Random selection from classic literature (Austen, Tolkien, Doyle, etc.)
- **Smart Length Handling:** Automatic traditional lengths for fixed forms, user-specified for variable forms
- **Enhanced Output:** Markdown files with character backgrounds, LLM attribution, and clean formatting
- **ASCII Art:** AI-generated thematic art for each poetry dialogue
- **Emoji Enhancement:** Optional emoji integration placed after relevant words

## Files

- `main.py` - Interactive CLI interface
- `dialogue_manager.py` - Core dialogue orchestration with dual LLM support
- `llm_client.py` - Anthropic Claude API integration
- `gemini_client.py` - Google Gemini API integration
- `prompts.py` - LLM prompt templates for all poetry forms
- `character_names.py` - Literary character database with detailed personas
- `tests/` - Organized test suite:
  - `tests/auto/` - Automatic system tests
  - `tests/user/` - User-specified tests