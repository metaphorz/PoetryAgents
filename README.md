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

The system asks 6 questions:
1. **Theme:** "a walk in the snow"
2. **Number of agents:** 2
3. **Form:** Choose from 8 formats (haiku, prose, sonnet, villanelle, limerick, ballad, ghazal, tanka)
4. **Poem length:** lines/stanzas per poem (varies by format)
5. **Conversation length:** rounds of dialogue
6. **Emojis:** Whether to enhance poetry with thematic emojis

## Demo Scripts

- `python demo_run.py` - Runs the example from Requirements.md
- `python test_system.py` - Tests both haiku and prose scenarios

## Features

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
- **Dialogue Flow:** First agent uses theme, others respond to previous poetry
- **Enhanced Output:** Markdown files with character backgrounds and clean formatting
- **ASCII Art:** AI-generated thematic art for each poetry dialogue
- **Emoji Enhancement:** Optional emoji integration placed after relevant words

## Files

- `main.py` - Interactive CLI interface
- `dialogue_manager.py` - Core dialogue orchestration
- `llm_client.py` - Anthropic API integration
- `prompts.py` - LLM prompt templates
- `character_names.py` - Fictional character database
- `test_system.py` - Testing scenarios