# Poetry Agent Dialogue Generator

A system that creates poetry dialogues between AI agents using Claude, Gemini, OpenAI, or OpenRouter, where agents engage in continuous conversation by responding to the complete dialogue history.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install anthropic google-generativeai openai python-dotenv requests
   ```

2. **Set up API keys:**
   You have two options for accessing LLM models:
   
   **Option 1: OpenRouter (Recommended - Simplest)**
   - Sign up at [openrouter.ai](https://openrouter.ai)
   - Get your API key from the Keys section
   - Add to `.env` file:
     ```
     OPENROUTER_API_KEY=your_openrouter_api_key_here
     ```
   - Access to 100+ models from multiple providers through one key
   
   **Option 2: Individual Provider APIs**
   Set up keys for the specific providers you want to use:
   
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
   
   **For OpenAI:**
   - Sign up at [platform.openai.com](https://platform.openai.com)
   - Go to API Keys and create a new key
   - Add to `.env` file:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

3. **Run the system:**

   **Option A: Web Interface (Recommended - User Friendly)**
   ```bash
   python start_web.py
   ```
   Then open your browser to: http://localhost:5000
   
   **Option B: Command Line Interface**
   ```bash
   python main.py
   ```

## Example Usage

The system asks 8 questions:
1. **API Mode:** Choose between Direct APIs or OpenRouter
2. **Agent 1 Model:** Select specific model for first agent
3. **Agent 2 Model:** Select specific model for second agent  
4. **Theme:** "a walk in the snow"
5. **Form:** Choose from 8 formats (haiku, prose, sonnet, villanelle, limerick, ballad, ghazal, tanka)
6. **Poem length:** Automatic for fixed forms (haiku, sonnet, etc.) or user-specified for variable forms (ballad stanzas, ghazal couplets, prose paragraphs)
7. **Conversation length:** How many rounds of conversation (each agent writes one poem per round)
8. **Emojis:** Whether to enhance poetry with thematic emojis

## Demo Scripts

- `python demo_run.py` - Runs the example from Requirements.md
- `python test_system.py` - Tests both haiku and prose scenarios

## Features

- **Multi-LLM Support:** Choose from Claude, Gemini, OpenAI, or 100+ OpenRouter models for each agent independently
- **Auto-Critique System:** Intelligent poetry evaluation and improvement
  - **Judge LLM Selection:** Automatically selects a different LLM as judge to avoid bias
  - **Literary Analysis:** Evaluates thematic coherence, form adherence, quality, flow, and character voice
  - **Conversation Improvement:** Creates enhanced versions based on critique feedback
  - **Three-Section Output:** Original conversation, detailed critique, and revised conversation
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

## Auto-Critique System

The system automatically evaluates and improves poetry conversations using an intelligent judge LLM:

### Judge Selection Logic
- **Direct API Mode:** Judge selects from unused providers (if agents use Claude + Gemini, judge uses OpenAI)
- **OpenRouter Mode:** Judge selects the latest model from an unused provider (Google → Anthropic → OpenAI priority) through OpenRouter
- **Bias Prevention:** Judge is always different from conversation agents to ensure objective evaluation

### Critique Process
1. **Literary Analysis:** Judge evaluates:
   - Thematic coherence with the chosen theme
   - Adherence to poetic form requirements
   - Literary quality (imagery, metaphors, word choice)
   - Conversational flow between agents
   - Distinct character voices
   
2. **Structured Feedback:** Detailed critique with specific suggestions for improvement

3. **Conversation Enhancement:** Judge creates improved versions addressing identified weaknesses

### Enhanced Output Format
The markdown output contains three comprehensive sections:
- **Original Conversation:** Initial poetry dialogue with LLM attribution
- **Literary Critique:** Detailed analysis from the judge LLM  
- **Revised Conversation:** Improved version incorporating critique feedback

## Files

- `main.py` - Interactive CLI interface with multi-LLM model selection
- `dialogue_manager.py` - Core dialogue orchestration with multi-LLM support and critique integration
- `critique_service.py` - Auto-critique system with judge selection and conversation improvement
- `llm_client.py` - Anthropic Claude API integration (Sonnet 4, Opus 4.1, etc.)
- `gemini_client.py` - Google Gemini API integration (2.5 Pro, 2.5 Flash, etc.)
- `openai_client.py` - OpenAI API integration (GPT-4o, GPT-4 Turbo, etc.)
- `openrouter_client.py` - OpenRouter API integration (100+ models)
- `poetry_rules.py` - Comprehensive structural rules for all poetry forms
- `prompts.py` - LLM prompt templates with form-specific rules
- `character_names.py` - Literary character database with detailed personas
- `tests/` - Organized test suite:
  - `tests/auto/` - Automatic system tests for all features
  - `tests/user/` - User-specified coverage tests