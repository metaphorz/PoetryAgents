#!/usr/bin/env python3
"""
Generate HTML interface with live model data from APIs.
This script fetches current models from all providers and creates a fresh HTML interface.
"""

import json
import os
from datetime import datetime

def fetch_live_model_data():
    """Fetch current model data from all available providers."""
    model_data = {}
    openrouter_data = {}
    
    print("🔍 Fetching live model data from APIs...")
    
    # Fetch Claude models
    try:
        from llm_client import LLMClient
        claude_models = LLMClient.get_available_models()
        model_data['Claude'] = claude_models
        print(f"✅ Claude: {len(claude_models)} models")
    except Exception as e:
        print(f"⚠️  Claude API unavailable: {e}")
        model_data['Claude'] = {"Claude 3.5 Sonnet": "claude-3-5-sonnet-20241022"}
    
    # Fetch Gemini models
    try:
        from gemini_client import GeminiClient
        gemini_models = GeminiClient.get_available_models()
        model_data['Gemini'] = gemini_models
        print(f"✅ Gemini: {len(gemini_models)} models")
    except Exception as e:
        print(f"⚠️  Gemini API unavailable: {e}")
        model_data['Gemini'] = {"Gemini 1.5 Flash": "gemini-1.5-flash"}
    
    # Fetch OpenAI models
    try:
        from openai_client import OpenAIClient
        openai_models = OpenAIClient.get_available_models()
        model_data['OpenAI'] = openai_models
        print(f"✅ OpenAI: {len(openai_models)} models")
    except Exception as e:
        print(f"⚠️  OpenAI API unavailable: {e}")
        model_data['OpenAI'] = {"GPT-4o": "gpt-4o"}
    
    # Fetch OpenRouter models by provider
    try:
        from openrouter_client import OpenRouterClient
        
        # Get all available models from OpenRouter
        all_models = OpenRouterClient.search_models("")  # Empty search gets all models
        
        # Organize by provider
        providers = {
            'anthropic': {},
            'openai': {},
            'google': {},
            'meta-llama': {},
            'mistralai': {},
            'qwen': {}
        }
        
        for model in all_models:
            model_id = model['id']
            model_name = model.get('name', model_id)
            
            # Extract provider from model ID
            if '/' in model_id:
                provider = model_id.split('/')[0]
                if provider in providers:
                    # Create display name from model ID
                    display_name = model_id.split('/')[-1]
                    display_name = display_name.replace('-', ' ').title()
                    display_name = display_name.replace('Gpt', 'GPT').replace('Llama', 'Llama').replace('Ai', 'AI')
                    
                    providers[provider][display_name] = model_id
        
        # Only keep providers that have models
        openrouter_data = {k: v for k, v in providers.items() if v}
        print(f"✅ OpenRouter: {sum(len(v) for v in openrouter_data.values())} models across {len(openrouter_data)} providers")
        
    except Exception as e:
        print(f"⚠️  OpenRouter API unavailable: {e}")
        # Fallback minimal data
        openrouter_data = {
            'anthropic': {"Claude 3.5 Sonnet": "anthropic/claude-3.5-sonnet"},
            'openai': {"GPT 4o": "openai/gpt-4o"}
        }
    
    return model_data, openrouter_data

def generate_html_content(model_data, openrouter_data):
    """Generate the complete HTML content with live model data."""
    
    # Convert Python dicts to JavaScript format
    model_data_js = json.dumps(model_data, indent=12)
    openrouter_data_js = json.dumps(openrouter_data, indent=12)
    
    # Create provider options for OpenRouter
    openrouter_providers = ""
    for provider_key in openrouter_data.keys():
        # Create display name
        display_name = provider_key.replace('-', ' ').title()
        if provider_key == 'meta-llama':
            display_name = 'Meta (Llama)'
        elif provider_key == 'mistralai':
            display_name = 'Mistral AI'
        elif provider_key == 'anthropic':
            display_name = 'Anthropic (Claude)'
        elif provider_key == 'openai':
            display_name = 'OpenAI'
        elif provider_key == 'google':
            display_name = 'Google (Gemini)'
        
        openrouter_providers += f'                                    <option value="{provider_key}">{display_name}</option>\n'
    
    generation_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Poetry Agents - Dynamic Model Interface</title>
    <!-- Generated on {generation_time} with live model data -->
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Georgia', serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }}

        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}

        .generation-info {{
            background: #e8f6f3;
            color: #2c3e50;
            padding: 10px;
            text-align: center;
            font-size: 0.9em;
            border-bottom: 2px solid #3498db;
        }}

        .form-container {{
            padding: 30px;
        }}

        .section {{
            margin-bottom: 25px;
            padding: 20px;
            border: 2px solid #e8f4f8;
            border-radius: 15px;
            background: #f8fcff;
        }}

        .section h2 {{
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 1.3em;
            border-bottom: 2px solid #3498db;
            padding-bottom: 8px;
        }}

        .poets-container {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 25px;
            margin-bottom: 20px;
        }}

        .poet-selection {{
            background: white;
            padding: 18px;
            border-radius: 12px;
            border: 2px solid #e1f5fe;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
        }}

        .poet-selection h3 {{
            color: #1976d2;
            margin-bottom: 12px;
            font-size: 1.1em;
        }}

        .form-group {{
            margin-bottom: 15px;
        }}

        label {{
            display: block;
            margin-bottom: 6px;
            font-weight: bold;
            color: #34495e;
            font-size: 14px;
        }}

        select, input[type="text"] {{
            width: 100%;
            padding: 10px;
            border: 2px solid #bdc3c7;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s ease;
        }}

        select:focus, input:focus {{
            outline: none;
            border-color: #3498db;
            box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
        }}

        .radio-group {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 10px;
            margin-top: 8px;
        }}

        .radio-item {{
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 8px 12px;
            border: 2px solid #e8f4f8;
            border-radius: 8px;
            background: white;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 13px;
        }}

        .radio-item:hover {{
            background: #e8f4f8;
            border-color: #3498db;
        }}

        .radio-item input[type="radio"] {{
            width: auto;
            margin: 0;
        }}

        .radio-item.selected {{
            background: #3498db;
            color: white;
            border-color: #2980b9;
        }}

        .theme-section {{
            background: white;
            padding: 20px;
            border-radius: 12px;
            border: 2px solid #e8f5e8;
        }}

        .theme-section h3 {{
            color: #27ae60;
            margin-bottom: 12px;
        }}

        #theme {{
            font-size: 16px;
            padding: 12px;
            border: 2px solid #27ae60;
        }}

        .generate-btn {{
            background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
            color: white;
            padding: 15px 35px;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
            margin-top: 25px;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .generate-btn:hover {{
            background: linear-gradient(135deg, #229954 0%, #27ae60 100%);
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(39, 174, 96, 0.3);
        }}

        .command-output {{
            display: none;
            margin-top: 25px;
            padding: 20px;
            background: #2c3e50;
            border-radius: 12px;
            border: 2px solid #34495e;
            color: #ecf0f1;
            font-family: 'Courier New', monospace;
        }}

        .command-output h3 {{
            color: #3498db;
            margin-bottom: 15px;
        }}

        .copy-btn {{
            background: #3498db;
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
            margin-left: 10px;
        }}

        .copy-btn:hover {{
            background: #2980b9;
        }}

        .instructions {{
            background: #fff3cd;
            border: 2px solid #ffeaa7;
            color: #856404;
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
        }}

        .instructions h4 {{
            margin-bottom: 10px;
            color: #b8860b;
        }}

        .instructions ol {{
            margin-left: 20px;
        }}

        .instructions li {{
            margin-bottom: 5px;
            font-size: 14px;
        }}

        @media (max-width: 768px) {{
            .poets-container {{
                grid-template-columns: 1fr;
                gap: 20px;
            }}
            
            .radio-group {{
                grid-template-columns: 1fr;
            }}
            
            .form-container {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎭 Poetry Agents</h1>
            <p>Generate poetry dialogues with live API models</p>
        </div>

        <div class="generation-info">
            📡 Model data refreshed: {generation_time} | Total models: {sum(len(models) for models in model_data.values()) + sum(len(models) for models in openrouter_data.values())}
        </div>

        <div class="form-container">
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
{openrouter_providers}                                </select>
                            </div>
                            <div class="form-group" id="poet1OpenrouterModelGroup" style="display: none;">
                                <label for="poet1OpenrouterModel">Specific Model:</label>
                                <select id="poet1OpenrouterModel" name="poet1OpenrouterModel" disabled>
                                    <option value="">First select a provider...</option>
                                </select>
                            </div>
                        </div>

                        <!-- Poet 2 -->
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
{openrouter_providers}                                </select>
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

                <!-- Poetry Form Section -->
                <div class="section">
                    <h2>📝 Poetry Settings</h2>
                    <div class="form-group">
                        <label>Poetry Form:</label>
                        <div class="radio-group">
                            <div class="radio-item">
                                <input type="radio" id="haiku" name="form" value="haiku" checked>
                                <label for="haiku">Haiku</label>
                            </div>
                            <div class="radio-item">
                                <input type="radio" id="prose" name="form" value="prose">
                                <label for="prose">Prose</label>
                            </div>
                            <div class="radio-item">
                                <input type="radio" id="sonnet" name="form" value="sonnet">
                                <label for="sonnet">Sonnet</label>
                            </div>
                            <div class="radio-item">
                                <input type="radio" id="villanelle" name="form" value="villanelle">
                                <label for="villanelle">Villanelle</label>
                            </div>
                            <div class="radio-item">
                                <input type="radio" id="limerick" name="form" value="limerick">
                                <label for="limerick">Limerick</label>
                            </div>
                            <div class="radio-item">
                                <input type="radio" id="ballad" name="form" value="ballad">
                                <label for="ballad">Ballad</label>
                            </div>
                            <div class="radio-item">
                                <input type="radio" id="ghazal" name="form" value="ghazal">
                                <label for="ghazal">Ghazal</label>
                            </div>
                            <div class="radio-item">
                                <input type="radio" id="tanka" name="form" value="tanka">
                                <label for="tanka">Tanka</label>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Conversation Length Section -->
                <div class="section">
                    <h2>💬 Conversation Length</h2>
                    <div class="form-group">
                        <label>Number of rounds:</label>
                        <div class="radio-group">
                            <div class="radio-item">
                                <input type="radio" id="rounds1" name="conversationLength" value="1">
                                <label for="rounds1">1 Round</label>
                            </div>
                            <div class="radio-item">
                                <input type="radio" id="rounds2" name="conversationLength" value="2" checked>
                                <label for="rounds2">2 Rounds</label>
                            </div>
                            <div class="radio-item">
                                <input type="radio" id="rounds3" name="conversationLength" value="3">
                                <label for="rounds3">3 Rounds</label>
                            </div>
                            <div class="radio-item">
                                <input type="radio" id="rounds4" name="conversationLength" value="4">
                                <label for="rounds4">4 Rounds</label>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Emoji Section -->
                <div class="section">
                    <h2>😊 Enhancement Options</h2>
                    <div class="form-group">
                        <label>Add emojis to enhance the poetry:</label>
                        <div class="radio-group">
                            <div class="radio-item">
                                <input type="radio" id="emojiYes" name="emojis" value="yes">
                                <label for="emojiYes">Yes, add emojis</label>
                            </div>
                            <div class="radio-item">
                                <input type="radio" id="emojiNo" name="emojis" value="no" checked>
                                <label for="emojiNo">No emojis</label>
                            </div>
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
                        <li>Open terminal/command prompt in that directory</li>
                        <li>Run: <code>python run_poetry.py</code></li>
                        <li>Your poetry will be generated and saved automatically!</li>
                    </ol>
                </div>
                
                <div class="command-text" id="pythonCode" style="display: none;"></div>
            </div>
        </div>
    </div>

    <script>
        // Live model data fetched from APIs on {generation_time}
        const modelData = {model_data_js};

        // OpenRouter model data organized by provider
        const openrouterModelData = {openrouter_data_js};

        // Radio button styling and functionality
        document.addEventListener('DOMContentLoaded', function() {{
            const radioItems = document.querySelectorAll('.radio-item');
            radioItems.forEach(item => {{
                const radio = item.querySelector('input[type="radio"]');
                
                item.addEventListener('click', function() {{
                    if (!radio.checked) {{
                        radio.checked = true;
                        radio.dispatchEvent(new Event('change'));
                    }}
                }});
                
                radio.addEventListener('change', function() {{
                    // Remove selected class from siblings
                    const siblings = radio.closest('.radio-group').querySelectorAll('.radio-item');
                    siblings.forEach(sibling => sibling.classList.remove('selected'));
                    
                    // Add selected class to current item
                    if (radio.checked) {{
                        item.classList.add('selected');
                    }}
                }});
                
                // Set initial state
                if (radio.checked) {{
                    item.classList.add('selected');
                }}
            }});

            // API mode change handler
            const apiModeRadios = document.querySelectorAll('input[name="apiMode"]');
            apiModeRadios.forEach(radio => {{
                radio.addEventListener('change', toggleApiMode);
            }});
            
            // Set initial API mode state
            toggleApiMode();

            // Direct API provider change handlers
            document.getElementById('poet1Provider').addEventListener('change', function() {{
                loadModelsForPoet(1, this.value);
            }});

            document.getElementById('poet2Provider').addEventListener('change', function() {{
                loadModelsForPoet(2, this.value);
            }});

            // OpenRouter provider change handlers
            document.getElementById('poet1OpenrouterProvider').addEventListener('change', function() {{
                loadOpenrouterModelsForPoet(1, this.value);
            }});

            document.getElementById('poet2OpenrouterProvider').addEventListener('change', function() {{
                loadOpenrouterModelsForPoet(2, this.value);
            }});
        }});

        function toggleApiMode() {{
            const apiMode = document.querySelector('input[name="apiMode"]:checked').value;
            const isOpenrouter = apiMode === 'openrouter';

            // Show/hide appropriate form groups
            ['poet1', 'poet2'].forEach(poet => {{
                const directGroup = document.getElementById(poet + 'DirectGroup');
                const modelGroup = document.getElementById(poet + 'ModelGroup');
                const openrouterGroup = document.getElementById(poet + 'OpenrouterGroup');
                const openrouterModelGroup = document.getElementById(poet + 'OpenrouterModelGroup');

                if (isOpenrouter) {{
                    directGroup.style.display = 'none';
                    modelGroup.style.display = 'none';
                    openrouterGroup.style.display = 'block';
                    openrouterModelGroup.style.display = 'block';
                    
                    // Clear direct API selections
                    document.getElementById(poet + 'Provider').selectedIndex = 0;
                    document.getElementById(poet + 'Model').selectedIndex = 0;
                    document.getElementById(poet + 'Model').disabled = true;
                }} else {{
                    directGroup.style.display = 'block';
                    modelGroup.style.display = 'block';
                    openrouterGroup.style.display = 'none';
                    openrouterModelGroup.style.display = 'none';
                    
                    // Clear OpenRouter selections
                    document.getElementById(poet + 'OpenrouterProvider').selectedIndex = 0;
                    document.getElementById(poet + 'OpenrouterModel').selectedIndex = 0;
                    document.getElementById(poet + 'OpenrouterModel').disabled = true;
                }}
            }});
        }}

        function loadModelsForPoet(poetNumber, provider) {{
            const modelSelect = document.getElementById(`poet${{poetNumber}}Model`);
            
            if (!provider) {{
                modelSelect.disabled = true;
                modelSelect.innerHTML = '<option value="">First select a provider...</option>';
                return;
            }}

            const models = modelData[provider];
            
            if (!models) {{
                modelSelect.innerHTML = '<option value="">No models available</option>';
                modelSelect.disabled = true;
                return;
            }}
            
            modelSelect.innerHTML = '<option value="">Select model...</option>';
            
            Object.entries(models).forEach(([displayName, modelId]) => {{
                const option = document.createElement('option');
                option.value = modelId;
                option.textContent = displayName;
                modelSelect.appendChild(option);
            }});
            
            modelSelect.disabled = false;
        }}

        function loadOpenrouterModelsForPoet(poetNumber, provider) {{
            const modelSelect = document.getElementById(`poet${{poetNumber}}OpenrouterModel`);
            
            if (!provider) {{
                modelSelect.disabled = true;
                modelSelect.innerHTML = '<option value="">First select a provider...</option>';
                return;
            }}

            const models = openrouterModelData[provider];
            
            if (!models) {{
                modelSelect.innerHTML = '<option value="">No models available</option>';
                modelSelect.disabled = true;
                return;
            }}
            
            modelSelect.innerHTML = '<option value="">Select model...</option>';
            
            Object.entries(models).forEach(([displayName, modelId]) => {{
                const option = document.createElement('option');
                option.value = modelId;
                option.textContent = displayName;
                modelSelect.appendChild(option);
            }});
            
            modelSelect.disabled = false;
        }}

        // Form submission handler
        document.getElementById('poetryForm').addEventListener('submit', function(e) {{
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            
            try {{
                const pythonScript = generatePythonScript(data);
                
                document.getElementById('pythonCode').textContent = pythonScript;
                document.getElementById('commandOutput').style.display = 'block';
                
                // Store the script for download
                window.generatedScript = pythonScript;
                
                // Scroll to command output
                document.getElementById('commandOutput').scrollIntoView({{ 
                    behavior: 'smooth', 
                    block: 'start' 
                }});
                
            }} catch (error) {{
                alert('Error generating script: ' + error.message);
            }}
        }});

        function generatePythonScript(data) {{
            // Validate required fields
            if (!data.theme || !data.form || !data.conversationLength) {{
                throw new Error('Please fill in all required fields');
            }}

            const isOpenrouter = data.apiMode === 'openrouter';
            let poet1Model, poet2Model;

            if (isOpenrouter) {{
                // OpenRouter mode
                if (!data.poet1OpenrouterProvider || !data.poet1OpenrouterModel || 
                    !data.poet2OpenrouterProvider || !data.poet2OpenrouterModel) {{
                    throw new Error('Please select providers and models for both poets in OpenRouter mode');
                }}
                poet1Model = data.poet1OpenrouterModel;
                poet2Model = data.poet2OpenrouterModel;
            }} else {{
                // Direct API mode
                if (!data.poet1Provider || !data.poet1Model || !data.poet2Provider || !data.poet2Model) {{
                    throw new Error('Please select providers and models for both poets');
                }}
                poet1Model = data.poet1Model;
                poet2Model = data.poet2Model;
            }}

            // Build the Python script with the user's configuration
            const script = `#!/usr/bin/env python3
"""
Custom poetry generation script created by Poetry Agents HTML interface.
Generated on ${{new Date().toLocaleString()}}
Model data refreshed: {generation_time}
"""

import sys
import os

def run_poetry_generation():
    """Run the poetry generation with your custom settings."""
    
    # Your configuration
    config = {{
        'api_mode': '${{isOpenrouter ? '2' : '1'}}',
        'poet1_provider': '${{isOpenrouter ? 'OpenRouter' : data.poet1Provider}}',
        'poet1_model': '${{poet1Model}}',
        'poet2_provider': '${{isOpenrouter ? 'OpenRouter' : data.poet2Provider}}',
        'poet2_model': '${{poet2Model}}',
        'theme': '${{data.theme.replace(/'/g, "\\\\'"')}}',
        'form': '${{data.form}}',
        'conversation_length': '${{data.conversationLength}}',
        'emojis': '${{data.emojis}}'
    }}
    
    print("🎭 Poetry Agents - Custom Generation")
    print("=" * 50)
    print(f"🎨 Theme: '{{config['theme']}}'")
    print(f"📝 Form: {{config['form']}}")
    print(f"🤖 Poet 1: {{config['poet1_provider']}} ({{config['poet1_model']}})")
    print(f"🤖 Poet 2: {{config['poet2_provider']}} ({{config['poet2_model']}})")
    print(f"💬 Rounds: {{config['conversation_length']}}")
    print(f"😊 Emojis: {{config['emojis']}}")
    print(f"📡 Models refreshed: {generation_time}")
    print()
    
    # Check if main.py exists
    if not os.path.exists('main.py'):
        print("❌ Error: main.py not found!")
        print("💡 Make sure you're running this from the PoetryAgents directory.")
        sys.exit(1)
    
    # Import and run the dialogue system directly
    try:
        from dialogue_manager import DialogueManager
        
        # Convert config to the format expected by DialogueManager
        dialogue_config = convert_config(config)
        
        print("🚀 Generating poetry dialogue...")
        
        # Generate dialogue
        manager = DialogueManager()
        dialogue_data = manager.generate_dialogue(dialogue_config)
        
        # Save to markdown file
        filename = manager.save_dialogue_to_markdown(dialogue_data)
        
        print(f"\\\\n✅ Poetry dialogue generated successfully!")
        print(f"📁 File saved: {{filename}}")
        print(f"📂 Full path: {{os.path.abspath(filename)}}")
        
        # Try to open the file
        try:
            import subprocess
            import platform
            
            system = platform.system()
            if system == "Darwin":  # macOS
                subprocess.run(["open", filename])
            elif system == "Windows":
                os.startfile(filename)
            elif system == "Linux":
                subprocess.run(["xdg-open", filename])
            
            print("🎉 Poetry file opened in your default markdown viewer!")
            
        except Exception:
            print("💡 Open the file manually to view your beautiful poetry!")
    
    except ImportError as e:
        print(f"❌ Import Error: {{e}}")
        print("💡 Make sure all dependencies are installed: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error: {{e}}")
        print("💡 Check your API keys are set in environment variables")

def convert_config(config):
    """Convert simple config to DialogueManager format."""
    
    # Handle form-specific lengths
    form = config['form']
    fixed_lengths = {{
        'haiku': (3, 'lines'),
        'sonnet': (14, 'lines'),
        'villanelle': (19, 'lines'),
        'limerick': (5, 'lines'),
        'tanka': (5, 'lines')
    }}
    
    if form in fixed_lengths:
        poem_length, length_unit = fixed_lengths[form]
    else:
        # Variable forms
        default_lengths = {{
            'prose': (2, 'paragraphs'),
            'ballad': (4, 'stanzas'),
            'ghazal': (7, 'couplets')
        }}
        poem_length, length_unit = default_lengths.get(form, (4, 'lines'))
    
    # Convert to DialogueManager format
    dialogue_config = {{
        'theme': config['theme'],
        'num_agents': 2,
        'form': form,
        'poem_length': poem_length,
        'length_unit': length_unit,
        'conversation_length': int(config['conversation_length']),
        'use_openrouter': config['api_mode'] == '2',
        'use_emojis': config['emojis'].lower() == 'yes',
        'output_format': 'markdown'
    }}
    
    if config['api_mode'] == '2':
        # OpenRouter mode
        dialogue_config.update({{
            'agent1_llm': 'OpenRouter',
            'agent2_llm': 'OpenRouter',
            'agent1_openrouter_search': config['poet1_model'],
            'agent2_openrouter_search': config['poet2_model'],
            'agent1_claude_model': None,
            'agent1_gemini_model': None,
            'agent1_openai_model': None,
            'agent2_claude_model': None,
            'agent2_gemini_model': None,
            'agent2_openai_model': None
        }})
    else:
        # Direct API mode
        dialogue_config.update({{
            'agent1_llm': config['poet1_provider'],
            'agent2_llm': config['poet2_provider'],
            'agent1_openrouter_search': None,
            'agent2_openrouter_search': None
        }})
        
        # Set specific models
        for agent_num, provider_key, model_key in [(1, 'poet1_provider', 'poet1_model'), (2, 'poet2_provider', 'poet2_model')]:
            provider = config[provider_key]
            model = config[model_key]
            
            # Initialize all to None
            dialogue_config[f'agent{{agent_num}}_claude_model'] = None
            dialogue_config[f'agent{{agent_num}}_gemini_model'] = None
            dialogue_config[f'agent{{agent_num}}_openai_model'] = None
            
            # Set the appropriate one
            if provider == 'Claude':
                dialogue_config[f'agent{{agent_num}}_claude_model'] = model
            elif provider == 'Gemini':
                dialogue_config[f'agent{{agent_num}}_gemini_model'] = model
            elif provider == 'OpenAI':
                dialogue_config[f'agent{{agent_num}}_openai_model'] = model
    
    return dialogue_config

if __name__ == '__main__':
    run_poetry_generation()`;

            return script;
        }}

        // Download button functionality
        document.getElementById('downloadBtn').addEventListener('click', function() {{
            if (!window.generatedScript) {{
                alert('Please generate a script first!');
                return;
            }}
            
            // Create a blob with the Python script content
            const blob = new Blob([window.generatedScript], {{ type: 'text/plain' }});
            const url = window.URL.createObjectURL(blob);
            
            // Create a temporary download link
            const a = document.createElement('a');
            a.href = url;
            a.download = 'run_poetry.py';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            
            // Clean up the URL object
            window.URL.revokeObjectURL(url);
            
            this.textContent = '✅ Downloaded!';
            setTimeout(() => {{
                this.textContent = '💾 Download run_poetry.py';
            }}, 2000);
        }});
    </script>
</body>
</html>'''
    
    return html_content

def main():
    """Main function to generate the HTML interface."""
    print("🎭 Generating Poetry Agents HTML Interface with Live Model Data")
    print("=" * 60)
    
    # Fetch live model data
    try:
        model_data, openrouter_data = fetch_live_model_data()
    except Exception as e:
        print(f"❌ Error fetching model data: {e}")
        print("💡 Make sure your API keys are set and you have internet access")
        return
    
    # Generate HTML content
    print("\n🌐 Generating HTML interface...")
    html_content = generate_html_content(model_data, openrouter_data)
    
    # Write to file
    output_file = "poetry_generator_live.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Generated: {output_file}")
    print(f"📏 File size: {len(html_content)} bytes")
    print(f"📊 Total models: {sum(len(models) for models in model_data.values()) + sum(len(models) for models in openrouter_data.values())}")
    
    print(f"\n🎉 Success! Open {output_file} in your browser to use the interface.")
    print("💡 To refresh with latest models, run this script again.")

if __name__ == '__main__':
    main()