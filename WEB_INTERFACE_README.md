# Poetry Agents Web Interface

## Overview

A beautiful, user-friendly web interface for the Poetry Agents system that simplifies the poetry generation process through an intuitive browser-based interface.

## Features

### 🎨 Modern Design
- Responsive layout that works on desktop and mobile
- Beautiful gradient backgrounds and smooth animations
- Professional typography optimized for poetry content
- Interactive radio buttons and form elements

### 🤖 Dual Poet Selection
- Side-by-side selection for Poet 1 and Poet 2
- Support for all 4 LLM providers:
  - **Claude (Anthropic)** - Multiple Sonnet, Opus, and Haiku models
  - **Gemini (Google)** - Pro, Flash, and 1.0 variants
  - **OpenAI** - GPT-4o, GPT-4 Turbo, GPT-3.5 Turbo
  - **OpenRouter** - 100+ models with curated popular selections
- Dynamic model loading based on provider selection
- Real-time validation and error handling

### 📝 Poetry Configuration
- **Theme Input**: Free-form text field for creative inspiration
- **Poetry Forms**: Radio button selection for:
  - Haiku (5-7-5 syllables)
  - Prose (free verse paragraphs)
  - Sonnet (14 lines)
  - Limerick (humorous 5-line form)
- **Conversation Length**: 1-4 rounds of poet exchanges
- **Emoji Enhancement**: Optional emoji integration

### 🚀 Streamlined Workflow
1. Select providers and models for both poets
2. Enter your creative theme
3. Choose poetry form and conversation length
4. Generate and download beautiful markdown files
5. One-click file download with formatted poetry

## Quick Start

### 1. Start the Web Server
```bash
# Option A: Simple startup with dependency checking
python start_web.py

# Option B: Direct server start
python web_server.py

# Option C: Interactive demo with browser opening
python demo_web.py
```

### 2. Open Your Browser
Navigate to: **http://localhost:5000**

### 3. Create Poetry
- Select your preferred LLM models
- Enter an inspiring theme
- Choose your poetry style
- Click "Generate Poetry Dialogue"
- Download your beautiful poetry markdown file

## API Endpoints

The web interface is powered by a Flask backend with these endpoints:

- `GET /` - Serve the main HTML interface
- `GET /api/models/<provider>` - Get available models for a provider
- `POST /api/generate` - Generate poetry dialogue
- `GET /download/<filename>` - Download generated files
- `GET /api/health` - Health check

## File Structure

```
📁 Web Interface Files
├── index.html              # Main web interface
├── web_server.py           # Flask backend server
├── start_web.py           # Startup script with checks
├── demo_web.py            # Interactive demo
└── WEB_INTERFACE_README.md # This documentation
```

## Technical Details

### Frontend (index.html)
- **Pure HTML/CSS/JavaScript** - No external dependencies
- **Responsive Design** - Grid layout with mobile support
- **Real-time Validation** - Form validation and user feedback
- **Dynamic Loading** - AJAX calls for model lists
- **Error Handling** - Graceful error display and recovery

### Backend (web_server.py)
- **Flask Framework** - Lightweight Python web server
- **CORS Enabled** - Cross-origin request support
- **Security** - Input validation and sanitization
- **Integration** - Direct connection to existing Poetry Agents system
- **File Management** - Automatic markdown file generation and serving

### Configuration Translation
The web interface automatically translates user selections into the format expected by the existing Poetry Agents system:

```python
# Web form data → Poetry system config
{
  'poet1Provider': 'claude',
  'poet1Model': 'claude-3-5-sonnet',
  'theme': 'autumn rain',
  'form': 'haiku'
} 
→ 
{
  'agent1_llm': 'Claude',
  'agent1_claude_model': 'claude-3-5-sonnet-20241022',
  'theme': 'autumn rain',
  'form': 'haiku',
  'poem_length': 3,
  'length_unit': 'lines'
}
```

## Example Themes

Try these creative themes in the web interface:

**Nature & Seasons**
- "morning frost on spider webs"
- "the last autumn leaf falling"
- "ocean waves under starlight"

**Urban & Modern**
- "neon reflections in rain puddles"
- "the empty subway at midnight"
- "coffee shop conversations"

**Fantasy & Imagination**
- "a library that exists between dimensions"
- "the dragon who learned to paint"
- "messages written in cloud formations"

**Emotional & Abstract**
- "the weight of unspoken words"
- "dancing with your own shadow"
- "the sound of memory"

## Benefits Over CLI

### User Experience
- **Visual Selection** instead of numbered lists
- **Immediate Feedback** with real-time validation
- **No Command Memorization** - everything is clickable
- **Error Recovery** - clear error messages and retry options

### Accessibility
- **Cross-Platform** - works on any device with a browser
- **No Terminal Required** - perfect for non-technical users
- **Modern Interface** - familiar web patterns and interactions
- **Mobile Friendly** - responsive design for tablets and phones

### Workflow
- **Faster Setup** - visual model selection vs. CLI navigation
- **Batch Operations** - easy to generate multiple poems with different settings
- **File Management** - direct download links for generated content
- **Session Persistence** - form remembers your last selections

## Troubleshooting

### Server Won't Start
```bash
# Check if Flask is installed
pip install flask flask-cors

# Check if all dependencies are available
python -c "import flask, flask_cors; print('✅ Dependencies OK')"
```

### Models Not Loading
- Verify API keys are set in environment variables
- Check network connectivity
- Look for error messages in browser developer console

### Generation Fails
- Ensure both poets have valid model selections
- Check that theme field is not empty
- Verify API keys have sufficient credits/quota

## Development

To extend the web interface:

1. **Add New Providers**: Update `web_server.py` models endpoint
2. **New Poetry Forms**: Add to radio button group and form handling
3. **UI Improvements**: Modify `index.html` styles and JavaScript
4. **API Features**: Extend Flask routes in `web_server.py`

The web interface is designed to be modular and easily extensible while maintaining the full power of the underlying Poetry Agents system.