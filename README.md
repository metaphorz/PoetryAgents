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
   ./start_web_server.sh
   ```
   Then open your browser to: http://localhost:8080
   
   **To stop the web server:**
   ```bash
   ./stop_web_server.sh
   ```
   
   **Option B: Command Line Interface**
   ```bash
   python main.py
   ```

## Web Interface Features

### **API Mode Selection**
The web interface offers two distinct modes for accessing AI models:

**Direct API Mode:**
- Connect directly to individual provider APIs
- Choose from Claude (Anthropic), Gemini (Google), or OpenAI models
- Each agent can use a different provider
- Requires specific API keys for each provider

**OpenRouter Mode:**
- Access 100+ models through OpenRouter's unified API
- Single API key provides access to multiple providers
- Dynamic model list fetched from OpenRouter's live catalog
- Includes latest models from Anthropic, OpenAI, Meta, Google, Mistral, and more

### **Model Selection**
- **Dynamic Interface:** Provider options change based on selected API mode
- **Real-time Loading:** Model lists fetched live from APIs
- **Independent Selection:** Each poet can use different models/providers
- **Comprehensive Coverage:** From fast models for experimentation to premium models for quality

## Example Usage

### **Web Interface Workflow:**
1. **API Mode:** Choose between Direct APIs or OpenRouter
2. **Poet 1 & 2:** Select providers and specific models for each agent
3. **Theme:** Enter creative inspiration (e.g., "a walk in the snow")
4. **Poetry Form:** Choose from 12 formats (haiku, tanka, prose, sonnet, villanelle, limerick, ballad, ghazal, heroic couplet, sestina, pindaric ode, quatrain)
5. **Conversation Length:** Select number of rounds (1-4)
6. **Emoji Enhancement:** Choose whether to add thematic emojis
7. **Generate:** Create poetry dialogue and download as markdown file

## Usage Examples

### **Web Interface (Recommended)**
```bash
# Start the server
./start_web_server.sh

# Open browser to http://localhost:8080
# Configure your poetry dialogue through the web form
# Download generated markdown files from the browser

# Stop the server when done
./stop_web_server.sh
```

### **Command Line Interface**
```bash
# Traditional CLI interface
python main.py

# Follow interactive prompts for configuration
```

### **Utility Scripts**
- `python scripts/run_poetry.py` - Direct poetry generation script
- `scripts/poetry_agents.sh` - Comprehensive workflow automation

## Features

- **Multi-LLM Support:** Choose from Claude, Gemini, OpenAI, or 100+ OpenRouter models for each agent independently
- **Auto-Critique System:** Intelligent poetry evaluation and improvement
  - **Judge LLM Selection:** Automatically selects a different LLM as judge to avoid bias
  - **Literary Analysis:** Evaluates thematic coherence, form adherence, quality, flow, and character voice
  - **Conversation Improvement:** Creates enhanced versions based on critique feedback
  - **Three-Section Output:** Original conversation, detailed critique, and revised conversation
- **Poetry Forms:** 12 supported formats including:
  - **Haiku:** Traditional Japanese 5-7-5 syllable structure
  - **Tanka:** Japanese 5-7-5-7-7 syllable structure
  - **Prose:** Free verse poetry
  - **Sonnet:** 14-line form with various rhyme schemes
  - **Villanelle:** 19-line form with complex refrains (like Dylan Thomas's "Do Not Go Gentle")
  - **Limerick:** 5-line AABBA humorous verse
  - **Ballad:** Narrative quatrains with alternating meter
  - **Ghazal:** Persian/Arabic form with repeated radif and complex rhyme
  - **Heroic Couplet:** Pairs of rhyming lines in iambic pentameter
  - **Sestina:** 39-line form with intricate end-word repetition pattern
  - **Pindaric Ode:** Irregular, celebratory verses with varying structure
  - **Quatrain:** Four-line stanzas with various rhyme schemes
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

### **Core System**
- `main.py` - Interactive CLI interface with multi-LLM model selection
- `dialogue_manager.py` - Core dialogue orchestration with multi-LLM support and critique integration
- `critique_service.py` - Auto-critique system with judge selection and conversation improvement
- `web_server.py` - Flask web server providing API endpoints for web interface
- `index.html` - Modern web interface with dynamic model selection

### **Web Server Management**
- `start_web_server.sh` - Startup script that loads environment variables and starts server
- `stop_web_server.sh` - Script to safely stop the web server
- `start_web.py` - Python web server startup with dependency and environment checks

### **LLM Integrations**
- `llm_client.py` - Anthropic Claude API integration (Sonnet 4, Opus 4.1, etc.)
- `gemini_client.py` - Google Gemini API integration (2.5 Pro, 2.5 Flash, etc.)
- `openai_client.py` - OpenAI API integration (GPT-4o, GPT-4 Turbo, etc.)
- `openrouter_client.py` - OpenRouter API integration (100+ models)

### **Poetry System**
- `poetry_rules.py` - Comprehensive structural rules for all 12 poetry forms
- `prompts.py` - LLM prompt templates with form-specific rules
- `character_names.py` - Literary character database with detailed personas

### **Utilities & Scripts**
- `scripts/` - Utility scripts:
  - `poetry_agents.sh` - Comprehensive workflow script
  - `generate_html_interface.py` - HTML interface generator
  - `run_poetry.py` - Direct poetry generation script
- `docs/` - Documentation files
- `outputs/` - Generated poetry dialogues (markdown files)
- `tests/` - Organized test suite:
  - `tests/auto/` - Automatic system tests for all features
  - `tests/user/` - User-specified coverage tests