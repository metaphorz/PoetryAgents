# Poetry Agents - One-Script Solution 🎭

## The Complete Shell Script That Does Everything

**`poetry_agents.sh`** - Your one-stop solution for Poetry Agents with dynamic model fetching!

## Quick Start

```bash
# Make it executable (first time only)
chmod +x poetry_agents.sh

# Run everything automatically
./poetry_agents.sh
```

**That's it!** The script will:
1. ✅ Check all requirements
2. 🔄 Fetch live models from all APIs  
3. 🌐 Generate fresh HTML interface
4. 🚀 Open it in your browser automatically

## All Available Commands

```bash
# Complete workflow (default)
./poetry_agents.sh

# Just refresh models and regenerate interface
./poetry_agents.sh --refresh

# Just open existing interface
./poetry_agents.sh --open  

# Check requirements only
./poetry_agents.sh --check

# Clean everything and start fresh
./poetry_agents.sh --clean

# Show help
./poetry_agents.sh --help
```

## What It Does

### 🔍 **Smart Requirements Checking**
- Verifies you're in the right directory
- Checks Python 3 availability
- Auto-installs dependencies from `requirements.txt`
- Validates API keys (needs at least one)
- Shows colorful status for each check

### 📡 **Live Model Data Fetching**  
- Calls **all available APIs** to get current models
- **No hardcoded models** - everything is fresh from APIs
- Handles API failures gracefully with fallbacks
- Embeds model data directly in HTML (no server needed)

### 🌐 **Dynamic HTML Generation**
- Creates `poetry_generator_live.html` with live model data
- Shows timestamp of when models were fetched
- Displays total model count in the interface
- Works completely offline once generated

### 🚀 **Automatic Browser Opening**
- Detects your OS (macOS, Linux, Windows)
- Opens the HTML file in your default browser
- Works with any modern browser

### 🎨 **User-Friendly Experience**
- Colorful terminal output with emojis
- Clear progress indicators
- Helpful error messages
- Usage instructions and examples

## Example Output

```
🎭 Poetry Agents - Complete Workflow Script 🎭
=================================================================

Checking Requirements
=====================
✅ Found main.py - in correct directory  
✅ Python 3 is available
✅ HTML generator script found
✅ Dependencies updated
✅ OpenAI API key found
⚠️  ANTHROPIC_API_KEY not set

🚀 Generating Fresh HTML Interface with Live Model Data
======================================================
💡 Fetching live model data from APIs...
✅ Claude: 6 models
✅ Gemini: 6 models  
✅ OpenAI: 6 models
✅ OpenRouter: 11 models across 4 providers
✅ Fresh HTML interface generated successfully!

🌐 Opening HTML Interface
========================
✅ Interface opened in your default browser!
```

## Benefits

### ✨ **Zero Manual Setup**
- One command does everything
- No need to remember multiple steps
- Automatic dependency management
- Intelligent error handling

### 🔄 **Always Current**
- Models fetched fresh from APIs every time
- `--refresh` option to update models anytime
- Timestamp shown in interface
- No stale or outdated model lists

### 🎯 **Multiple Workflows**
- Quick refresh: `--refresh`
- Just open: `--open`
- Check setup: `--check`
- Fresh start: `--clean`

### 💻 **Cross-Platform**
- Works on macOS, Linux, Windows
- Uses appropriate browser opening method
- Color support in terminals
- zsh and bash compatible

## API Key Requirements

Set at least one of these environment variables:

```bash
export ANTHROPIC_API_KEY="your-key-here"
export OPENAI_API_KEY="your-key-here"  
export GOOGLE_API_KEY="your-key-here"
export OPENROUTER_API_KEY="your-key-here"
```

The script will work with any combination - it fetches models from whatever APIs you have keys for.

## File Structure After Running

```
📁 PoetryAgents/
├── poetry_agents.sh              ← The magic script
├── poetry_generator_live.html    ← Generated interface (fresh models)
├── generate_html_interface.py    ← HTML generator (used by script)
├── run_poetry.py                ← Downloaded from HTML interface
└── outputs/                     ← Your poetry appears here
```

## Troubleshooting

### Script Won't Run
```bash
# Make sure it's executable
chmod +x poetry_agents.sh

# Check you're in the right directory
ls main.py  # Should exist
```

### No API Keys
```bash
# Set at least one API key
export OPENAI_API_KEY="your-key-here"
./poetry_agents.sh --check
```

### Browser Doesn't Open
```bash
# Open manually
./poetry_agents.sh --refresh  # Generate fresh interface
open poetry_generator_live.html  # macOS
# or
xdg-open poetry_generator_live.html  # Linux
```

### Models Not Current
```bash
# Refresh with latest models
./poetry_agents.sh --refresh
```

## Pro Tips

🚀 **Daily Use**: Run `./poetry_agents.sh --refresh` to get the latest models

🎨 **Theme Ideas**: 
- "first snow of winter"
- "robot learning to love" 
- "ancient library at midnight"
- "neon lights in rain"

💡 **Model Combos**:
- Claude + OpenAI (different thinking styles)
- Same provider (consistent style)
- OpenRouter experimental models

---

**🎭 One script. Everything included. Poetry made simple.**