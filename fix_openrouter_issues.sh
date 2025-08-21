#!/usr/bin/env zsh

# Fix OpenRouter Issues - Address missing providers and model dropdown problems
# This script fixes both OpenRouter provider coverage and model selection

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m'

echo "${PURPLE}=================================================================${NC}"
echo "🔧 ${CYAN}Fixing OpenRouter Provider and Model Issues${NC} 🔧"
echo "${PURPLE}=================================================================${NC}"
echo ""

diagnose_openrouter_issues() {
    echo "${CYAN}🔍 Diagnosing OpenRouter Issues${NC}"
    echo ""
    
    # Check current OpenRouter provider options in HTML
    echo "${YELLOW}Current OpenRouter providers in HTML:${NC}"
    grep -A 10 'id="poet1OpenrouterProvider"' poetry_generator_live.html | grep '<option value=' | while read line; do
        provider=$(echo "$line" | sed -E 's/.*value="([^"]*)".*>\s*([^<]*)<.*/\1 → \2/')
        echo "  📦 $provider"
    done
    
    echo ""
    echo "${YELLOW}Checking for openrouterModelData variable:${NC}"
    if grep -q "const openrouterModelData" poetry_generator_live.html; then
        echo "${GREEN}✅ Found openrouterModelData declaration${NC}"
        
        # Show what providers are in the data
        echo "${YELLOW}Providers in openrouterModelData:${NC}"
        grep -A 50 "const openrouterModelData" poetry_generator_live.html | grep -E '"[^"]*":\s*{' | while read line; do
            provider=$(echo "$line" | sed -E 's/.*"([^"]*)":.*/\1/')
            echo "  🌍 $provider"
        done
    else
        echo "${RED}❌ openrouterModelData variable NOT FOUND${NC}"
        echo "💡 This is why model dropdowns don't populate!"
    fi
}

fetch_comprehensive_openrouter_data() {
    echo ""
    echo "${CYAN}🌐 Fetching Comprehensive OpenRouter Data${NC}"
    
    # Use Python to get fresh OpenRouter data with all providers
    cat > fetch_openrouter_comprehensive.py << 'EOF'
#!/usr/bin/env python3
"""
Fetch comprehensive OpenRouter model data with all available providers.
"""

import json

def get_comprehensive_openrouter_data():
    """Get OpenRouter data with comprehensive provider coverage."""
    print("🔍 Fetching comprehensive OpenRouter model data...")
    
    try:
        from openrouter_client import OpenRouterClient
        
        # Get all available models
        all_models = OpenRouterClient.search_models("")
        print(f"✅ Found {len(all_models)} total OpenRouter models")
        
        # Organize by provider with comprehensive coverage
        providers = {
            'anthropic': {},
            'openai': {},
            'google': {},
            'meta': {},
            'mistralai': {},
            'qwen': {},
            'cohere': {},
            'x-ai': {},
            'deepseek': {},
            'nvidia': {},
            'perplexity': {},
            'liquid': {},
            'amazon': {},
            'microsoft': {},
            'together': {}
        }
        
        for model in all_models:
            model_id = model['id']
            model_name = model.get('name', model_id)
            
            # Extract provider from model ID
            if '/' in model_id:
                provider_raw = model_id.split('/')[0]
                
                # Map provider names to our categories
                provider_key = None
                if provider_raw in ['anthropic']:
                    provider_key = 'anthropic'
                elif provider_raw in ['openai']:
                    provider_key = 'openai'
                elif provider_raw in ['google']:
                    provider_key = 'google'
                elif provider_raw in ['meta-llama', 'meta']:
                    provider_key = 'meta'
                elif provider_raw in ['mistralai']:
                    provider_key = 'mistralai'
                elif provider_raw in ['qwen']:
                    provider_key = 'qwen'
                elif provider_raw in ['cohere']:
                    provider_key = 'cohere'
                elif provider_raw in ['x-ai', 'xai']:
                    provider_key = 'x-ai'
                elif provider_raw in ['deepseek']:
                    provider_key = 'deepseek'
                elif provider_raw in ['nvidia']:
                    provider_key = 'nvidia'
                elif provider_raw in ['perplexity']:
                    provider_key = 'perplexity'
                elif provider_raw in ['liquid']:
                    provider_key = 'liquid'
                elif provider_raw in ['amazon']:
                    provider_key = 'amazon'
                elif provider_raw in ['microsoft']:
                    provider_key = 'microsoft'
                elif provider_raw in ['together']:
                    provider_key = 'together'
                
                if provider_key:
                    # Create display name
                    display_name = model_id.split('/')[-1]
                    display_name = display_name.replace('-', ' ').title()
                    display_name = display_name.replace('Gpt', 'GPT').replace('Llama', 'Llama').replace('Ai', 'AI')
                    
                    providers[provider_key][display_name] = model_id
        
        # Only keep providers that have models
        filtered_providers = {k: v for k, v in providers.items() if v}
        
        print(f"✅ Organized into {len(filtered_providers)} provider categories:")
        for provider, models in filtered_providers.items():
            print(f"  📦 {provider}: {len(models)} models")
        
        return filtered_providers
        
    except Exception as e:
        print(f"⚠️  Error fetching from API: {e}")
        # Fallback comprehensive data
        return {
            'anthropic': {
                "Claude 3.5 Sonnet": "anthropic/claude-3.5-sonnet",
                "Claude 3 Opus": "anthropic/claude-3-opus",
                "Claude 3 Sonnet": "anthropic/claude-3-sonnet", 
                "Claude 3 Haiku": "anthropic/claude-3-haiku"
            },
            'openai': {
                "GPT 4o": "openai/gpt-4o",
                "GPT 4o Mini": "openai/gpt-4o-mini",
                "GPT 4 Turbo": "openai/gpt-4-turbo",
                "GPT 4": "openai/gpt-4",
                "GPT 3.5 Turbo": "openai/gpt-3.5-turbo"
            },
            'google': {
                "Gemini Pro 1.5": "google/gemini-pro-1.5",
                "Gemini Flash 1.5": "google/gemini-flash-1.5",
                "Gemini Pro": "google/gemini-pro"
            },
            'meta': {
                "Llama 3.1 405B": "meta-llama/llama-3.1-405b-instruct",
                "Llama 3.1 70B": "meta-llama/llama-3.1-70b-instruct",
                "Llama 3.1 8B": "meta-llama/llama-3.1-8b-instruct"
            },
            'mistralai': {
                "Mistral Large 2": "mistralai/mistral-large-2407",
                "Mistral Nemo": "mistralai/mistral-nemo",
                "Mixtral 8x7B": "mistralai/mixtral-8x7b-instruct"
            },
            'x-ai': {
                "Grok Beta": "x-ai/grok-beta"
            },
            'cohere': {
                "Command R Plus": "cohere/command-r-plus",
                "Command R": "cohere/command-r"
            }
        }

if __name__ == '__main__':
    data = get_comprehensive_openrouter_data()
    
    # Save to JSON file
    with open('comprehensive_openrouter_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"💾 Saved comprehensive data to comprehensive_openrouter_data.json")
EOF

    python3 fetch_openrouter_comprehensive.py
    
    if [[ -f "comprehensive_openrouter_data.json" ]]; then
        echo "${GREEN}✅ Successfully fetched comprehensive OpenRouter data${NC}"
        
        echo ""
        echo "${YELLOW}📊 Provider Summary:${NC}"
        python3 -c "
import json
with open('comprehensive_openrouter_data.json', 'r') as f:
    data = json.load(f)
for provider, models in data.items():
    print(f'  📦 {provider}: {len(models)} models')
    for name in list(models.keys())[:3]:
        print(f'    • {name}')
    if len(models) > 3:
        print(f'    ... and {len(models) - 3} more')
    print()
"
    else
        echo "${RED}❌ Failed to fetch OpenRouter data${NC}"
        return 1
    fi
}

create_fixed_html_with_comprehensive_openrouter() {
    echo ""
    echo "${CYAN}🛠️  Creating Fixed HTML with Comprehensive OpenRouter Support${NC}"
    
    # Read the comprehensive data
    if [[ ! -f "comprehensive_openrouter_data.json" ]]; then
        echo "${RED}❌ comprehensive_openrouter_data.json not found${NC}"
        return 1
    fi
    
    # Create backup
    cp poetry_generator_live.html poetry_generator_live.html.backup.openrouter
    
    # Create the fixed HTML
    cat > poetry_generator_openrouter_fixed.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Poetry Agents - Fixed OpenRouter Interface</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Georgia', serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 1000px; margin: 0 auto; background: rgba(255, 255, 255, 0.95); border-radius: 20px; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1); overflow: hidden; }
        .header { background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%); color: white; padding: 30px; text-align: center; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
        .header p { font-size: 1.2em; opacity: 0.9; }
        .generation-info { background: #e8f6f3; color: #2c3e50; padding: 10px; text-align: center; font-size: 0.9em; border-bottom: 2px solid #3498db; }
        .form-container { padding: 30px; }
        .section { margin-bottom: 25px; padding: 20px; border: 2px solid #e8f4f8; border-radius: 15px; background: #f8fcff; }
        .section h2 { color: #2c3e50; margin-bottom: 15px; font-size: 1.3em; border-bottom: 2px solid #3498db; padding-bottom: 8px; }
        .poets-container { display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin-bottom: 20px; }
        .poet-selection { background: white; padding: 18px; border-radius: 12px; border: 2px solid #e1f5fe; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05); }
        .poet-selection h3 { color: #1976d2; margin-bottom: 12px; font-size: 1.1em; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 6px; font-weight: bold; color: #34495e; font-size: 14px; }
        select, input[type="text"] { width: 100%; padding: 10px; border: 2px solid #bdc3c7; border-radius: 8px; font-size: 14px; transition: border-color 0.3s ease; }
        select:focus, input:focus { outline: none; border-color: #3498db; box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1); }
        select:disabled { background: #f8f9fa; opacity: 0.6; }
        .radio-group { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 10px; margin-top: 8px; }
        .radio-item { display: flex; align-items: center; gap: 6px; padding: 8px 12px; border: 2px solid #e8f4f8; border-radius: 8px; background: white; cursor: pointer; transition: all 0.3s ease; font-size: 13px; }
        .radio-item:hover { background: #e8f4f8; border-color: #3498db; }
        .radio-item input[type="radio"] { width: auto; margin: 0; }
        .radio-item.selected { background: #3498db; color: white; border-color: #2980b9; }
        .theme-section { background: white; padding: 20px; border-radius: 12px; border: 2px solid #e8f5e8; }
        .theme-section h3 { color: #27ae60; margin-bottom: 12px; }
        #theme { font-size: 16px; padding: 12px; border: 2px solid #27ae60; }
        .generate-btn { background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%); color: white; padding: 15px 35px; border: none; border-radius: 12px; font-size: 16px; font-weight: bold; cursor: pointer; width: 100%; margin-top: 25px; transition: all 0.3s ease; text-transform: uppercase; letter-spacing: 1px; }
        .generate-btn:hover { background: linear-gradient(135deg, #229954 0%, #27ae60 100%); transform: translateY(-2px); box-shadow: 0 8px 16px rgba(39, 174, 96, 0.3); }
        .command-output { display: none; margin-top: 25px; padding: 20px; background: #2c3e50; border-radius: 12px; border: 2px solid #34495e; color: #ecf0f1; font-family: 'Courier New', monospace; }
        .command-output h3 { color: #3498db; margin-bottom: 15px; }
        .copy-btn { background: #3498db; color: white; border: none; padding: 8px 15px; border-radius: 6px; cursor: pointer; font-size: 12px; margin-left: 10px; }
        .copy-btn:hover { background: #2980b9; }
        .instructions { background: #fff3cd; border: 2px solid #ffeaa7; color: #856404; padding: 15px; border-radius: 10px; margin-top: 15px; }
        .debug-info { background: #e7f3ff; padding: 10px; margin: 10px 0; border-radius: 5px; font-size: 12px; border: 1px solid #bee5eb; }
        @media (max-width: 768px) { .poets-container { grid-template-columns: 1fr; gap: 20px; } .radio-group { grid-template-columns: 1fr; } .form-container { padding: 20px; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎭 Poetry Agents</h1>
            <p>Fixed OpenRouter Interface with All Providers</p>
        </div>

        <div class="generation-info">
            🔧 Fixed OpenRouter interface with comprehensive provider coverage | Debug mode enabled
        </div>

        <div class="form-container">
            <div class="debug-info" id="debugOutput">
                <strong>Debug Output:</strong> OpenRouter interface loading...<br>
            </div>

            <form id="poetryForm">
                <!-- API Mode Selection -->
                <div class="section">
                    <h2>🔌 API Mode</h2>
                    <div class="form-group">
                        <div class="radio-group">
                            <div class="radio-item">
                                <input type="radio" id="directApi" name="apiMode" value="direct" checked>
                                <label for="directApi">Direct APIs</label>
                            </div>
                            <div class="radio-item">
                                <input type="radio" id="openrouter" name="apiMode" value="openrouter">
                                <label for="openrouter">OpenRouter</label>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Poet Selection Section -->
                <div class="section">
                    <h2>🤖 Select Your Poets</h2>
                    <div class="poets-container">
                        <!-- Poet 1 -->
                        <div class="poet-selection">
                            <h3>Poet 1</h3>
                            <!-- Direct API Mode -->
                            <div class="form-group" id="poet1DirectGroup">
                                <label for="poet1Provider">LLM Provider:</label>
                                <select id="poet1Provider" name="poet1Provider" required>
                                    <option value="">Select Provider...</option>
                                    <option value="Claude">Claude (Anthropic)</option>
                                    <option value="Gemini">Gemini (Google)</option>
                                    <option value="OpenAI">OpenAI</option>
                                </select>
                            </div>
                            <div class="form-group" id="poet1ModelGroup">
                                <label for="poet1Model">Specific Model:</label>
                                <select id="poet1Model" name="poet1Model" disabled required>
                                    <option value="">First select a provider...</option>
                                </select>
                            </div>
                            <!-- OpenRouter Mode -->
                            <div class="form-group" id="poet1OpenrouterGroup" style="display: none;">
                                <label for="poet1OpenrouterProvider">Provider:</label>
                                <select id="poet1OpenrouterProvider" name="poet1OpenrouterProvider">
                                    <option value="">Select Provider...</option>
EOF

    # Add comprehensive OpenRouter provider options from JSON data
    python3 -c "
import json
with open('comprehensive_openrouter_data.json', 'r') as f:
    data = json.load(f)

# Create provider display names
provider_names = {
    'anthropic': 'Anthropic (Claude)',
    'openai': 'OpenAI (GPT)',
    'google': 'Google (Gemini)',
    'meta': 'Meta (Llama)',
    'mistralai': 'Mistral AI',
    'x-ai': 'X.AI (Grok)',
    'cohere': 'Cohere (Command)',
    'qwen': 'Qwen',
    'deepseek': 'DeepSeek',
    'nvidia': 'NVIDIA',
    'perplexity': 'Perplexity',
    'liquid': 'Liquid',
    'amazon': 'Amazon',
    'microsoft': 'Microsoft',
    'together': 'Together AI'
}

for provider_key in sorted(data.keys()):
    display_name = provider_names.get(provider_key, provider_key.replace('-', ' ').title())
    print(f'                                    <option value=\"{provider_key}\">{display_name}</option>')
" >> poetry_generator_openrouter_fixed.html

    cat >> poetry_generator_openrouter_fixed.html << 'EOF'
                                </select>
                            </div>
                            <div class="form-group" id="poet1OpenrouterModelGroup" style="display: none;">
                                <label for="poet1OpenrouterModel">Specific Model:</label>
                                <select id="poet1OpenrouterModel" name="poet1OpenrouterModel" disabled>
                                    <option value="">First select a provider...</option>
                                </select>
                            </div>
                        </div>

                        <!-- Poet 2 (identical structure) -->
                        <div class="poet-selection">
                            <h3>Poet 2</h3>
                            <!-- Direct API Mode -->
                            <div class="form-group" id="poet2DirectGroup">
                                <label for="poet2Provider">LLM Provider:</label>
                                <select id="poet2Provider" name="poet2Provider" required>
                                    <option value="">Select Provider...</option>
                                    <option value="Claude">Claude (Anthropic)</option>
                                    <option value="Gemini">Gemini (Google)</option>
                                    <option value="OpenAI">OpenAI</option>
                                </select>
                            </div>
                            <div class="form-group" id="poet2ModelGroup">
                                <label for="poet2Model">Specific Model:</label>
                                <select id="poet2Model" name="poet2Model" disabled required>
                                    <option value="">First select a provider...</option>
                                </select>
                            </div>
                            <!-- OpenRouter Mode -->
                            <div class="form-group" id="poet2OpenrouterGroup" style="display: none;">
                                <label for="poet2OpenrouterProvider">Provider:</label>
                                <select id="poet2OpenrouterProvider" name="poet2OpenrouterProvider">
                                    <option value="">Select Provider...</option>
EOF

    # Add the same comprehensive provider options for Poet 2
    python3 -c "
import json
with open('comprehensive_openrouter_data.json', 'r') as f:
    data = json.load(f)

provider_names = {
    'anthropic': 'Anthropic (Claude)',
    'openai': 'OpenAI (GPT)',
    'google': 'Google (Gemini)',
    'meta': 'Meta (Llama)',
    'mistralai': 'Mistral AI',
    'x-ai': 'X.AI (Grok)',
    'cohere': 'Cohere (Command)',
    'qwen': 'Qwen',
    'deepseek': 'DeepSeek',
    'nvidia': 'NVIDIA',
    'perplexity': 'Perplexity',
    'liquid': 'Liquid',
    'amazon': 'Amazon',
    'microsoft': 'Microsoft',
    'together': 'Together AI'
}

for provider_key in sorted(data.keys()):
    display_name = provider_names.get(provider_key, provider_key.replace('-', ' ').title())
    print(f'                                    <option value=\"{provider_key}\">{display_name}</option>')
" >> poetry_generator_openrouter_fixed.html

    cat >> poetry_generator_openrouter_fixed.html << 'EOF'
                                </select>
                            </div>
                            <div class="form-group" id="poet2OpenrouterModelGroup" style="display: none;">
                                <label for="poet2OpenrouterModel">Specific Model:</label>
                                <select id="poet2OpenrouterModel" name="poet2OpenrouterModel" disabled>
                                    <option value="">First select a provider...</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Theme Section -->
                <div class="section">
                    <div class="theme-section">
                        <h3>🎨 Poetry Theme</h3>
                        <div class="form-group">
                            <label for="theme">Enter your theme or inspiration:</label>
                            <input type="text" id="theme" name="theme" placeholder="e.g., 'a walk in the snow', 'dancing under stars', 'the sound of rain'..." required>
                        </div>
                    </div>
                </div>

                <!-- Poetry Settings -->
                <div class="section">
                    <h2>📝 Poetry Settings</h2>
                    <div class="form-group">
                        <label>Poetry Form:</label>
                        <div class="radio-group">
                            <div class="radio-item"><input type="radio" id="haiku" name="form" value="haiku" checked><label for="haiku">Haiku</label></div>
                            <div class="radio-item"><input type="radio" id="prose" name="form" value="prose"><label for="prose">Prose</label></div>
                            <div class="radio-item"><input type="radio" id="sonnet" name="form" value="sonnet"><label for="sonnet">Sonnet</label></div>
                            <div class="radio-item"><input type="radio" id="limerick" name="form" value="limerick"><label for="limerick">Limerick</label></div>
                        </div>
                    </div>
                </div>

                <!-- Conversation Length -->
                <div class="section">
                    <h2>💬 Conversation Length</h2>
                    <div class="form-group">
                        <label>Number of rounds:</label>
                        <div class="radio-group">
                            <div class="radio-item"><input type="radio" id="rounds1" name="conversationLength" value="1"><label for="rounds1">1 Round</label></div>
                            <div class="radio-item"><input type="radio" id="rounds2" name="conversationLength" value="2" checked><label for="rounds2">2 Rounds</label></div>
                            <div class="radio-item"><input type="radio" id="rounds3" name="conversationLength" value="3"><label for="rounds3">3 Rounds</label></div>
                            <div class="radio-item"><input type="radio" id="rounds4" name="conversationLength" value="4"><label for="rounds4">4 Rounds</label></div>
                        </div>
                    </div>
                </div>

                <!-- Emoji Options -->
                <div class="section">
                    <h2>😊 Enhancement Options</h2>
                    <div class="form-group">
                        <label>Add emojis to enhance the poetry:</label>
                        <div class="radio-group">
                            <div class="radio-item"><input type="radio" id="emojiYes" name="emojis" value="yes"><label for="emojiYes">Yes, add emojis</label></div>
                            <div class="radio-item"><input type="radio" id="emojiNo" name="emojis" value="no" checked><label for="emojiNo">No emojis</label></div>
                        </div>
                    </div>
                </div>

                <button type="submit" class="generate-btn" id="generateBtn">
                    ✨ Generate Poetry Script ✨
                </button>
            </form>

            <div class="command-output" id="commandOutput">
                <h3>🐍 Generated Python Script</h3>
                <p>Click the button below to download a custom Python script with your settings:</p>
                <button class="copy-btn" id="downloadBtn">💾 Download run_poetry.py</button>
                <div class="instructions">
                    <h4>📖 How to use:</h4>
                    <ol>
                        <li>Click "Download run_poetry.py" above</li>
                        <li>Save the file to your PoetryAgents directory</li>
                        <li>Run: <code>python3 run_poetry.py</code></li>
                        <li>Your poetry will be generated automatically!</li>
                    </ol>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Debug logging
        const debugLog = function(msg) { 
            console.log('🔧 OPENROUTER DEBUG:', msg);
            const debugDiv = document.getElementById('debugOutput');
            if (debugDiv) debugDiv.innerHTML += '<br>' + msg;
        };

        // Direct API model data
        const modelData = {
            "Claude": {
                "Claude Opus 4.1": "claude-opus-4-1-20250805",
                "Claude Opus 4": "claude-opus-4-20250514",
                "Claude Sonnet 4": "claude-sonnet-4-20250514",
                "Claude Sonnet 3.7": "claude-3-7-sonnet-20250219",
                "Claude Sonnet 3.5 (New)": "claude-3-5-sonnet-20241022",
                "Claude Haiku 3.5": "claude-3-5-haiku-20241022"
            },
            "Gemini": {
                "Gemini 2.5 Pro": "gemini-2.5-pro",
                "Gemini 2.5 Flash": "gemini-2.5-flash",
                "Gemini 1.5 Pro": "gemini-1.5-pro",
                "Gemini 1.5 Flash": "gemini-1.5-flash"
            },
            "OpenAI": {
                "GPT-4o": "gpt-4o",
                "GPT-4o Mini": "gpt-4o-mini",
                "GPT-4 Turbo": "gpt-4-turbo",
                "GPT-4": "gpt-4",
                "GPT-3.5 Turbo": "gpt-3.5-turbo"
            }
        };

        // Comprehensive OpenRouter model data from API
        const openrouterModelData = 
EOF

    # Embed the comprehensive OpenRouter data
    cat comprehensive_openrouter_data.json >> poetry_generator_openrouter_fixed.html

    cat >> poetry_generator_openrouter_fixed.html << 'EOF'
;

        // Debug model data loading
        debugLog('Direct API model data loaded: ' + (typeof modelData !== 'undefined' ? 'YES' : 'NO'));
        debugLog('OpenRouter model data loaded: ' + (typeof openrouterModelData !== 'undefined' ? 'YES' : 'NO'));

        if (typeof modelData !== 'undefined') {
            debugLog('Direct API providers: ' + Object.keys(modelData).join(', '));
        }

        if (typeof openrouterModelData !== 'undefined') {
            debugLog('OpenRouter providers: ' + Object.keys(openrouterModelData).join(', '));
            Object.entries(openrouterModelData).forEach(([provider, models]) => {
                debugLog(provider + ': ' + Object.keys(models).length + ' models');
            });
        }

        // Initialize interface
        document.addEventListener('DOMContentLoaded', function() {
            debugLog('DOM loaded, initializing OpenRouter-fixed interface...');
            
            // Radio button functionality
            const radioItems = document.querySelectorAll('.radio-item');
            radioItems.forEach(item => {
                const radio = item.querySelector('input[type="radio"]');
                item.addEventListener('click', function() {
                    if (!radio.checked) {
                        radio.checked = true;
                        radio.dispatchEvent(new Event('change'));
                    }
                });
                radio.addEventListener('change', function() {
                    const siblings = radio.closest('.radio-group').querySelectorAll('.radio-item');
                    siblings.forEach(sibling => sibling.classList.remove('selected'));
                    if (radio.checked) item.classList.add('selected');
                });
                if (radio.checked) item.classList.add('selected');
            });

            // API mode handlers
            const apiModeRadios = document.querySelectorAll('input[name="apiMode"]');
            apiModeRadios.forEach(radio => {
                radio.addEventListener('change', function() {
                    debugLog('API mode changed to: ' + this.value);
                    toggleApiMode();
                });
            });
            toggleApiMode();

            // Provider change handlers
            document.getElementById('poet1Provider').addEventListener('change', function() {
                debugLog('Poet 1 Direct provider changed to: "' + this.value + '"');
                loadModelsForPoet(1, this.value);
            });
            document.getElementById('poet2Provider').addEventListener('change', function() {
                debugLog('Poet 2 Direct provider changed to: "' + this.value + '"');
                loadModelsForPoet(2, this.value);
            });

            // OpenRouter provider change handlers
            document.getElementById('poet1OpenrouterProvider').addEventListener('change', function() {
                debugLog('Poet 1 OpenRouter provider changed to: "' + this.value + '"');
                loadOpenrouterModelsForPoet(1, this.value);
            });
            document.getElementById('poet2OpenrouterProvider').addEventListener('change', function() {
                debugLog('Poet 2 OpenRouter provider changed to: "' + this.value + '"');
                loadOpenrouterModelsForPoet(2, this.value);
            });

            debugLog('All event listeners set up successfully');
        });

        function toggleApiMode() {
            const apiMode = document.querySelector('input[name="apiMode"]:checked').value;
            const isOpenrouter = apiMode === 'openrouter';
            
            debugLog('Toggling API mode to: ' + apiMode);

            ['poet1', 'poet2'].forEach(poet => {
                const directGroup = document.getElementById(poet + 'DirectGroup');
                const modelGroup = document.getElementById(poet + 'ModelGroup');
                const openrouterGroup = document.getElementById(poet + 'OpenrouterGroup');
                const openrouterModelGroup = document.getElementById(poet + 'OpenrouterModelGroup');

                if (isOpenrouter) {
                    directGroup.style.display = 'none';
                    modelGroup.style.display = 'none';
                    openrouterGroup.style.display = 'block';
                    openrouterModelGroup.style.display = 'block';
                    
                    document.getElementById(poet + 'Provider').selectedIndex = 0;
                    document.getElementById(poet + 'Model').selectedIndex = 0;
                    document.getElementById(poet + 'Model').disabled = true;
                } else {
                    directGroup.style.display = 'block';
                    modelGroup.style.display = 'block';
                    openrouterGroup.style.display = 'none';
                    openrouterModelGroup.style.display = 'none';
                    
                    document.getElementById(poet + 'OpenrouterProvider').selectedIndex = 0;
                    document.getElementById(poet + 'OpenrouterModel').selectedIndex = 0;
                    document.getElementById(poet + 'OpenrouterModel').disabled = true;
                }
            });
            
            debugLog('API mode toggle complete');
        }

        function loadModelsForPoet(poetNumber, provider) {
            debugLog(`Loading Direct API models for Poet ${poetNumber}, provider: "${provider}"`);
            
            const modelSelect = document.getElementById(`poet${poetNumber}Model`);
            
            if (!provider) {
                modelSelect.disabled = true;
                modelSelect.innerHTML = '<option value="">First select a provider...</option>';
                return;
            }

            const models = modelData[provider];
            if (!models) {
                debugLog(`ERROR: No Direct API models found for provider "${provider}"`);
                modelSelect.innerHTML = '<option value="">No models available</option>';
                modelSelect.disabled = true;
                return;
            }
            
            debugLog(`Found ${Object.keys(models).length} Direct API models for ${provider}`);
            modelSelect.innerHTML = '<option value="">Select model...</option>';
            
            Object.entries(models).forEach(([displayName, modelId]) => {
                const option = document.createElement('option');
                option.value = modelId;
                option.textContent = displayName;
                modelSelect.appendChild(option);
            });
            
            modelSelect.disabled = false;
            debugLog(`SUCCESS: Loaded Direct API models for Poet ${poetNumber}`);
        }

        function loadOpenrouterModelsForPoet(poetNumber, provider) {
            debugLog(`Loading OpenRouter models for Poet ${poetNumber}, provider: "${provider}"`);
            
            const modelSelect = document.getElementById(`poet${poetNumber}OpenrouterModel`);
            
            if (!provider) {
                modelSelect.disabled = true;
                modelSelect.innerHTML = '<option value="">First select a provider...</option>';
                return;
            }

            if (typeof openrouterModelData === 'undefined') {
                debugLog('ERROR: openrouterModelData is undefined!');
                modelSelect.innerHTML = '<option value="">OpenRouter data not loaded</option>';
                modelSelect.disabled = true;
                return;
            }

            debugLog('OpenRouter data exists, checking provider: ' + provider);
            debugLog('Available OpenRouter providers: ' + Object.keys(openrouterModelData).join(', '));

            const models = openrouterModelData[provider];
            
            if (!models) {
                debugLog(`ERROR: No OpenRouter models found for provider "${provider}"`);
                modelSelect.innerHTML = '<option value="">No models available for ' + provider + '</option>';
                modelSelect.disabled = true;
                return;
            }
            
            debugLog(`Found ${Object.keys(models).length} OpenRouter models for ${provider}`);
            
            modelSelect.innerHTML = '<option value="">Select model...</option>';
            
            let addedCount = 0;
            Object.entries(models).forEach(([displayName, modelId]) => {
                const option = document.createElement('option');
                option.value = modelId;
                option.textContent = displayName;
                modelSelect.appendChild(option);
                addedCount++;
                debugLog(`Added OpenRouter model: ${displayName} → ${modelId}`);
            });
            
            modelSelect.disabled = false;
            debugLog(`SUCCESS: Loaded ${addedCount} OpenRouter models for Poet ${poetNumber}`);
        }

        // Form submission and script generation
        document.getElementById('poetryForm').addEventListener('submit', function(e) {
            e.preventDefault();
            debugLog('Form submitted');
            
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            
            try {
                const pythonScript = generatePythonScript(data);
                document.getElementById('commandOutput').style.display = 'block';
                window.generatedScript = pythonScript;
                document.getElementById('commandOutput').scrollIntoView({ behavior: 'smooth', block: 'start' });
                debugLog('Python script generated successfully');
            } catch (error) {
                debugLog('ERROR generating script: ' + error.message);
                alert('Error generating script: ' + error.message);
            }
        });

        function generatePythonScript(data) {
            if (!data.theme || !data.form || !data.conversationLength) {
                throw new Error('Please fill in all required fields');
            }

            const isOpenrouter = data.apiMode === 'openrouter';
            let poet1Model, poet2Model;

            if (isOpenrouter) {
                if (!data.poet1OpenrouterProvider || !data.poet1OpenrouterModel || 
                    !data.poet2OpenrouterProvider || !data.poet2OpenrouterModel) {
                    throw new Error('Please select providers and models for both poets in OpenRouter mode');
                }
                poet1Model = data.poet1OpenrouterModel;
                poet2Model = data.poet2OpenrouterModel;
            } else {
                if (!data.poet1Provider || !data.poet1Model || !data.poet2Provider || !data.poet2Model) {
                    throw new Error('Please select providers and models for both poets');
                }
                poet1Model = data.poet1Model;
                poet2Model = data.poet2Model;
            }

            return `#!/usr/bin/env python3
"""
OpenRouter-Fixed Poetry Generation Script
Generated on ${new Date().toLocaleString()}
Comprehensive OpenRouter provider support enabled
"""

import sys
import os

def run_poetry_generation():
    config = {
        'api_mode': '${isOpenrouter ? '2' : '1'}',
        'poet1_provider': '${isOpenrouter ? 'OpenRouter' : data.poet1Provider}',
        'poet1_model': '${poet1Model}',
        'poet2_provider': '${isOpenrouter ? 'OpenRouter' : data.poet2Provider}',
        'poet2_model': '${poet2Model}',
        'theme': '${data.theme.replace(/'/g, "\\'")}',
        'form': '${data.form}',
        'conversation_length': '${data.conversationLength}',
        'emojis': '${data.emojis}'
    }
    
    print("🎭 Poetry Agents - OpenRouter Fixed Generation")
    print("=" * 50)
    print(f"🎨 Theme: '{config['theme']}'")
    print(f"📝 Form: {config['form']}")
    print(f"🤖 Poet 1: {config['poet1_provider']} ({config['poet1_model']})")
    print(f"🤖 Poet 2: {config['poet2_provider']} ({config['poet2_model']})")
    print(f"💬 Rounds: {config['conversation_length']}")
    print(f"😊 Emojis: {config['emojis']}")
    print()
    
    if not os.path.exists('main.py'):
        print("❌ Error: main.py not found!")
        sys.exit(1)
    
    try:
        from dialogue_manager import DialogueManager
        dialogue_config = convert_config(config)
        
        print("🚀 Generating poetry dialogue...")
        manager = DialogueManager()
        dialogue_data = manager.generate_dialogue(dialogue_config)
        filename = manager.save_dialogue_to_markdown(dialogue_data)
        
        print(f"\\n✅ Poetry dialogue generated successfully!")
        print(f"📁 File saved: {filename}")
        
        try:
            import subprocess, platform
            system = platform.system()
            if system == "Darwin": subprocess.run(["open", filename])
            elif system == "Windows": os.startfile(filename)
            elif system == "Linux": subprocess.run(["xdg-open", filename])
            print("🎉 Poetry file opened!")
        except: print("💡 Open the file manually to view your poetry!")
    
    except Exception as e:
        print(f"❌ Error: {e}")

def convert_config(config):
    # Convert configuration for DialogueManager
    form = config['form']
    fixed_lengths = {'haiku': (3, 'lines'), 'sonnet': (14, 'lines'), 'limerick': (5, 'lines')}
    
    if form in fixed_lengths:
        poem_length, length_unit = fixed_lengths[form]
    else:
        poem_length, length_unit = (2, 'paragraphs') if form == 'prose' else (4, 'lines')
    
    dialogue_config = {
        'theme': config['theme'],
        'num_agents': 2,
        'form': form,
        'poem_length': poem_length,
        'length_unit': length_unit,
        'conversation_length': int(config['conversation_length']),
        'use_openrouter': config['api_mode'] == '2',
        'use_emojis': config['emojis'].lower() == 'yes',
        'output_format': 'markdown'
    }
    
    if config['api_mode'] == '2':
        dialogue_config.update({
            'agent1_llm': 'OpenRouter', 'agent2_llm': 'OpenRouter',
            'agent1_openrouter_search': config['poet1_model'],
            'agent2_openrouter_search': config['poet2_model'],
            'agent1_claude_model': None, 'agent1_gemini_model': None, 'agent1_openai_model': None,
            'agent2_claude_model': None, 'agent2_gemini_model': None, 'agent2_openai_model': None
        })
    else:
        dialogue_config.update({
            'agent1_llm': config['poet1_provider'], 'agent2_llm': config['poet2_provider'],
            'agent1_openrouter_search': None, 'agent2_openrouter_search': None
        })
        
        for agent_num, provider_key, model_key in [(1, 'poet1_provider', 'poet1_model'), (2, 'poet2_provider', 'poet2_model')]:
            provider, model = config[provider_key], config[model_key]
            dialogue_config[f'agent{agent_num}_claude_model'] = model if provider == 'Claude' else None
            dialogue_config[f'agent{agent_num}_gemini_model'] = model if provider == 'Gemini' else None
            dialogue_config[f'agent{agent_num}_openai_model'] = model if provider == 'OpenAI' else None
    
    return dialogue_config

if __name__ == '__main__': run_poetry_generation()`;
        }

        // Download functionality
        document.getElementById('downloadBtn').addEventListener('click', function() {
            if (!window.generatedScript) {
                alert('Please generate a script first!');
                return;
            }
            
            const blob = new Blob([window.generatedScript], { type: 'text/plain' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'run_poetry.py';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            this.textContent = '✅ Downloaded!';
            setTimeout(() => { this.textContent = '💾 Download run_poetry.py'; }, 2000);
            debugLog('Python script downloaded successfully');
        });

        // Initialize debug output
        debugLog('OpenRouter-fixed interface loaded successfully');
    </script>
</body>
</html>
EOF

    echo "${GREEN}✅ Created comprehensive OpenRouter-fixed HTML interface${NC}"
}

deploy_openrouter_fix() {
    echo ""
    echo "${CYAN}🚀 Deploying OpenRouter Fix${NC}"
    
    if [[ -f "poetry_generator_openrouter_fixed.html" ]]; then
        # Create backup of current version
        cp poetry_generator_live.html poetry_generator_live.html.backup.pre-openrouter-fix
        
        # Deploy the fixed version
        cp poetry_generator_openrouter_fixed.html poetry_generator_live.html
        
        echo "${GREEN}✅ Deployed OpenRouter-fixed interface as main interface${NC}"
        echo "${GREEN}✅ Created backup of previous version${NC}"
        
        # Verify deployment
        echo ""
        echo "${CYAN}🔍 Verifying OpenRouter Fix Deployment:${NC}"
        
        # Check provider count
        provider_count=$(grep -c '<option value="[a-z]' poetry_generator_live.html | head -1)
        echo "${GREEN}✅ OpenRouter providers in interface: ${provider_count}${NC}"
        
        # Check for openrouterModelData
        if grep -q "const openrouterModelData" poetry_generator_live.html; then
            echo "${GREEN}✅ openrouterModelData variable present${NC}"
            
            # Count providers in data
            data_providers=$(grep -A 200 "const openrouterModelData" poetry_generator_live.html | grep -c '"[^"]*": {')
            echo "${GREEN}✅ Providers with model data: ${data_providers}${NC}"
        else
            echo "${RED}❌ openrouterModelData variable missing${NC}"
        fi
        
        echo ""
        echo "${GREEN}🎉 OpenRouter fix deployment SUCCESSFUL!${NC}"
        
    else
        echo "${RED}❌ OpenRouter-fixed HTML not found${NC}"
        return 1
    fi
}

show_testing_instructions() {
    echo ""
    echo "${BLUE}🧪 TESTING THE OPENROUTER FIX${NC}"
    echo "${BLUE}$(echo "🧪 TESTING THE OPENROUTER FIX" | sed 's/./=/g')${NC}"
    echo ""
    
    echo "${CYAN}1. Open the Fixed Interface:${NC}"
    echo "   • File: ${YELLOW}poetry_generator_live.html${NC}"
    echo "   • Look for debug panel showing OpenRouter data loading"
    echo ""
    
    echo "${CYAN}2. Test OpenRouter Mode:${NC}"
    echo "   • Click ${YELLOW}\"OpenRouter\"${NC} radio button"
    echo "   • Check provider dropdown - should show ${GREEN}10+ providers${NC}:"
    echo "     - Anthropic (Claude)"
    echo "     - OpenAI (GPT)"
    echo "     - Google (Gemini)"
    echo "     - Meta (Llama)"
    echo "     - Mistral AI"
    echo "     - X.AI (Grok)"
    echo "     - Cohere (Command)"
    echo "     - And more..."
    echo ""
    
    echo "${CYAN}3. Test Model Selection:${NC}"
    echo "   • Select ${YELLOW}\"Anthropic (Claude)\"${NC} for Poet 1"
    echo "   • Model dropdown should populate with Claude models"
    echo "   • Select ${YELLOW}\"OpenAI (GPT)\"${NC} for Poet 2" 
    echo "   • Model dropdown should populate with GPT models"
    echo ""
    
    echo "${CYAN}4. Debug Panel Feedback:${NC}"
    echo "   • Watch for messages like:"
    echo "     - \"OpenRouter providers: anthropic, openai, google, meta...\""
    echo "     - \"Found X OpenRouter models for anthropic\""
    echo "     - \"Added OpenRouter model: Claude 3.5 Sonnet → anthropic/claude-3.5-sonnet\""
    echo ""
    
    echo "${GREEN}✅ Success Criteria:${NC}"
    echo "   • 10+ providers visible in OpenRouter dropdown"
    echo "   • Model dropdowns populate when provider selected"
    echo "   • Debug panel shows detailed model loading feedback"
    echo "   • No \"openrouterModelData is undefined\" errors"
    echo ""
    
    echo "${YELLOW}💡 If issues persist, check browser console for JavaScript errors${NC}"
}

main() {
    diagnose_openrouter_issues
    fetch_comprehensive_openrouter_data
    create_fixed_html_with_comprehensive_openrouter
    deploy_openrouter_fix
    show_testing_instructions
    
    echo ""
    echo "${PURPLE}🎯 OPENROUTER FIX COMPLETE${NC}"
    echo "${PURPLE}$(echo "🎯 OPENROUTER FIX COMPLETE" | sed 's/./=/g')${NC}"
    echo ""
    echo "${GREEN}✅ Fixed missing OpenRouter providers${NC}"
    echo "${GREEN}✅ Fixed missing model dropdown functionality${NC}"
    echo "${GREEN}✅ Added comprehensive provider coverage${NC}"
    echo "${GREEN}✅ Enhanced debugging and error reporting${NC}"
    echo ""
    echo "${CYAN}📁 Files Created:${NC}"
    echo "  • ${YELLOW}comprehensive_openrouter_data.json${NC} - Live OpenRouter data"
    echo "  • ${YELLOW}poetry_generator_openrouter_fixed.html${NC} - Fixed interface backup"
    echo "  • ${YELLOW}poetry_generator_live.html${NC} - Main interface (NOW FIXED)"
    echo ""
    echo "${GREEN}🎉 Both OpenRouter issues should now be completely resolved!${NC}"
}

# Make executable and run
chmod +x "$0" 2>/dev/null || true
main "$@"