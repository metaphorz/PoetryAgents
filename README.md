# Poetry Agent Dialogue Generator

A system that creates poetry dialogues between AI agents using Anthropic's Sonnet 4, where agents respond to each other based on themes and previous poetry.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install anthropic python-dotenv
   ```

2. **Set up API key:**
   - Add your Anthropic API key to `.env` file:
     ```
     ANTHROPIC_API_KEY=your_api_key_here
     ```

3. **Run the system:**
   ```bash
   python main.py
   ```

## Example Usage

The system asks 5 questions:
1. **Theme:** "a walk in the snow"
2. **Number of agents:** 2
3. **Form:** haiku or prose
4. **Poem length:** lines/stanzas per poem
5. **Conversation length:** rounds of dialogue

## Demo Scripts

- `python demo_run.py` - Runs the example from Requirements.md
- `python test_system.py` - Tests both haiku and prose scenarios

## Features

- **Poetry Forms:** Haiku (5-7-5 syllables) and prose (free verse)
- **Agent Names:** Random selection from 100+ fictional characters
- **Dialogue Flow:** First agent uses theme, others respond to previous poetry
- **Formatted Output:** Titles, bold agent names, proper poetry formatting

## Files

- `main.py` - Interactive CLI interface
- `dialogue_manager.py` - Core dialogue orchestration
- `llm_client.py` - Anthropic API integration
- `prompts.py` - LLM prompt templates
- `character_names.py` - Fictional character database
- `test_system.py` - Testing scenarios