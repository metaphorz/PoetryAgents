#!/usr/bin/env python3
"""
Create Working Main Interface
Takes the working debug version and enhances it to be a full main interface.
"""

import os

def create_working_main_interface():
    """Create a working main interface based on the debug version that works."""
    
    print("🛠️ Creating working main interface based on debug version...")
    
    # Read the working debug version
    with open("poetry_generator_debug.html", 'r', encoding='utf-8') as f:
        debug_content = f.read()
    
    # Read the original main interface to get additional features
    with open("poetry_generator_live.html", 'r', encoding='utf-8') as f:
        main_content = f.read()
    
    # Extract model data from main interface (it has more models)
    import re
    model_data_match = re.search(r'const modelData = \{(.*?)\};', main_content, re.DOTALL)
    if model_data_match:
        full_model_data = "const modelData = {" + model_data_match.group(1) + "};"
    else:
        # Fallback to debug version data
        full_model_data = '''const modelData = {
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
                "Gemini 2.5 Flash-Lite": "gemini-2.5-flash-lite",
                "Gemini 2.5 Pro Preview 03-25": "gemini-2.5-pro-preview-03-25",
                "Gemini 2.5 Pro Preview 05-06": "gemini-2.5-pro-preview-05-06",
                "Gemini 2.5 Pro Preview": "gemini-2.5-pro-preview-06-05"
            },
            "OpenAI": {
                "Gpt 4.1 Nano": "gpt-4.1-nano",
                "Gpt 4.1 Nano 2025 04 14": "gpt-4.1-nano-2025-04-14",
                "Gpt 4.1 Mini": "gpt-4.1-mini",
                "Gpt 4.1 Mini 2025 04 14": "gpt-4.1-mini-2025-04-14",
                "Gpt 4.1": "gpt-4.1",
                "Gpt 4.1 2025 04 14": "gpt-4.1-2025-04-14"
            }
        };'''
    
    # Create a working main interface
    working_main = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Poetry Agents - AI Poetry Dialogue Generator</title>
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

        select, input[type="text"], input[type="number"] {{
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

        select:disabled {{
            opacity: 0.5;
            background: #f0f0f0;
            cursor: not-allowed;
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

        .api-mode {{
            display: flex;
            gap: 15px;
            margin: 15px 0;
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

        .loading {{
            opacity: 0.7;
            cursor: not-allowed;
        }}

        #loadingMessage {{
            display: none;
            text-align: center;
            margin: 20px 0;
            padding: 15px;
            background: #e8f4f8;
            border-radius: 8px;
            color: #2c3e50;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎭 Poetry Agents</h1>
            <p>AI Poetry Dialogue Generator</p>
        </div>

        <div class="form-container">
            <form id="poetryForm">
                <div class="section">
                    <h2>🔌 API Configuration</h2>
                    <div class="api-mode">
                        <label><input type="radio" name="apiMode" value="direct" checked> Direct APIs (Claude, OpenAI, Gemini)</label>
                        <label><input type="radio" name="apiMode" value="openrouter"> OpenRouter (100+ Models)</label>
                    </div>
                </div>

                <div class="section" id="directApiSection">
                    <h2>🎭 Poet Configuration</h2>
                    <div class="poets-container">
                        <div class="poet-selection">
                            <h3>🎭 Poet 1</h3>
                            <div class="form-group">
                                <label for="poet1Provider">LLM Provider:</label>
                                <select id="poet1Provider" name="poet1Provider" required>
                                    <option value="">Select Provider...</option>
                                    <option value="Claude">Claude (Anthropic)</option>
                                    <option value="OpenAI">OpenAI</option>
                                    <option value="Gemini">Gemini (Google)</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="poet1Model">Specific Model:</label>
                                <select id="poet1Model" name="poet1Model" disabled required>
                                    <option value="">First select a provider...</option>
                                </select>
                            </div>
                        </div>

                        <div class="poet-selection">
                            <h3>🎭 Poet 2</h3>
                            <div class="form-group">
                                <label for="poet2Provider">LLM Provider:</label>
                                <select id="poet2Provider" name="poet2Provider" required>
                                    <option value="">Select Provider...</option>
                                    <option value="Claude">Claude (Anthropic)</option>
                                    <option value="OpenAI">OpenAI</option>
                                    <option value="Gemini">Gemini (Google)</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="poet2Model">Specific Model:</label>
                                <select id="poet2Model" name="poet2Model" disabled required>
                                    <option value="">First select a provider...</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="section">
                    <h2>📝 Poetry Configuration</h2>
                    <div class="form-group">
                        <label for="theme">Theme:</label>
                        <input type="text" id="theme" name="theme" placeholder="e.g., a walk in the snow" required>
                    </div>
                    
                    <div class="form-group">
                        <label>Poetry Form:</label>
                        <div class="radio-group">
                            <div class="radio-item">
                                <input type="radio" id="form_haiku" name="form" value="haiku" checked>
                                <label for="form_haiku">Haiku</label>
                            </div>
                            <div class="radio-item">
                                <input type="radio" id="form_prose" name="form" value="prose">
                                <label for="form_prose">Prose</label>
                            </div>
                            <div class="radio-item">
                                <input type="radio" id="form_sonnet" name="form" value="sonnet">
                                <label for="form_sonnet">Sonnet</label>
                            </div>
                            <div class="radio-item">
                                <input type="radio" id="form_limerick" name="form" value="limerick">
                                <label for="form_limerick">Limerick</label>
                            </div>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label for="conversationLength">Conversation Rounds:</label>
                        <input type="number" id="conversationLength" name="conversationLength" min="1" max="10" value="3" required>
                    </div>
                    
                    <div class="form-group">
                        <label>
                            <input type="checkbox" id="useEmojis" name="useEmojis" checked>
                            Enhance with emojis
                        </label>
                    </div>
                </div>

                <button type="submit" class="generate-btn" id="generateBtn">
                    🎨 Generate Poetry Dialogue
                </button>
            </form>
            
            <div id="loadingMessage">
                <p>🎭 Generating poetry dialogue... This may take a moment.</p>
            </div>
        </div>
    </div>

    <script>
        // Full model data from main interface
        {full_model_data}

        function debugLog(message) {{
            console.log(`[Poetry Agents] ${{message}}`);
        }}

        function loadModelsForPoet(poetNumber, provider) {{
            debugLog(`Loading models for Poet ${{poetNumber}}, Provider: "${{provider}}"`);
            
            const modelSelect = document.getElementById(`poet${{poetNumber}}Model`);
            
            if (!modelSelect) {{
                debugLog(`ERROR: Model select element not found: poet${{poetNumber}}Model`);
                return;
            }}
            
            if (!provider) {{
                debugLog(`No provider selected - disabling dropdown`);
                modelSelect.disabled = true;
                modelSelect.innerHTML = '<option value="">First select a provider...</option>';
                return;
            }}

            debugLog(`Looking for models for provider: "${{provider}}"`);
            
            const models = modelData[provider];
            
            if (!models) {{
                debugLog(`ERROR: No models found for provider: ${{provider}}`);
                modelSelect.innerHTML = '<option value="">No models available</option>';
                modelSelect.disabled = true;
                return;
            }}
            
            debugLog(`Found ${{Object.keys(models).length}} models for ${{provider}}`);
            
            // Clear and populate dropdown
            modelSelect.innerHTML = '<option value="">Select model...</option>';
            
            Object.entries(models).forEach(([displayName, modelId]) => {{
                const option = document.createElement('option');
                option.value = modelId;
                option.textContent = displayName;
                modelSelect.appendChild(option);
            }});
            
            // Enable the dropdown
            modelSelect.disabled = false;
            debugLog(`SUCCESS: Enabled dropdown with ${{Object.keys(models).length}} models`);
        }}

        function toggleApiMode() {{
            const apiMode = document.querySelector('input[name="apiMode"]:checked').value;
            debugLog(`Toggling API mode to: ${{apiMode}}`);
            
            const directSection = document.getElementById('directApiSection');
            
            if (apiMode === 'direct') {{
                directSection.style.display = 'block';
                debugLog(`Showing Direct API mode`);
            }} else {{
                directSection.style.display = 'none';
                debugLog(`OpenRouter mode not implemented in this version`);
                alert('OpenRouter mode coming soon! Please use Direct APIs for now.');
                document.querySelector('input[name="apiMode"][value="direct"]').checked = true;
            }}
        }}

        // Set up event listeners when page loads
        document.addEventListener('DOMContentLoaded', function() {{
            debugLog(`Page loaded - setting up event listeners...`);
            
            // API mode change handlers
            const apiModeRadios = document.querySelectorAll('input[name="apiMode"]');
            apiModeRadios.forEach(radio => {{
                radio.addEventListener('change', toggleApiMode);
            }});
            
            // Provider change handlers
            const poet1Provider = document.getElementById('poet1Provider');
            const poet2Provider = document.getElementById('poet2Provider');
            
            if (poet1Provider) {{
                poet1Provider.addEventListener('change', function() {{
                    debugLog(`Poet 1 provider changed to: "${{this.value}}"`);
                    loadModelsForPoet(1, this.value);
                }});
                debugLog(`Poet 1 provider event listener set up`);
            }} else {{
                debugLog(`ERROR: Poet 1 provider element not found`);
            }}

            if (poet2Provider) {{
                poet2Provider.addEventListener('change', function() {{
                    debugLog(`Poet 2 provider changed to: "${{this.value}}"`);
                    loadModelsForPoet(2, this.value);
                }});
                debugLog(`Poet 2 provider event listener set up`);
            }} else {{
                debugLog(`ERROR: Poet 2 provider element not found`);
            }}
            
            // Form submission handler
            const form = document.getElementById('poetryForm');
            form.addEventListener('submit', function(e) {{
                e.preventDefault();
                debugLog('Form submitted - this would generate poetry');
                alert('Poetry generation coming soon! For now, the dropdowns are working.');
            }});
            
            debugLog(`All event listeners set up successfully`);
            debugLog(`Ready to test - select providers to see if dropdowns enable`);
        }});
    </script>
</body>
</html>'''
    
    # Write the working main interface
    working_file = "poetry_generator_working.html"
    with open(working_file, 'w', encoding='utf-8') as f:
        f.write(working_main)
    
    print(f"✅ Created working main interface: {working_file}")
    return working_file

def main():
    """Create a working main interface."""
    
    print("🛠️ Creating Working Main Interface")
    print("=" * 45)
    
    working_file = create_working_main_interface()
    
    print(f"\n✅ Working main interface created: {working_file}")
    print(f"📍 Full path: {os.path.abspath(working_file)}")
    
    print(f"\n🧪 This version:")
    print("   • Uses the EXACT same JavaScript logic as the working debug version")
    print("   • Has the full main interface design and layout") 
    print("   • Includes comprehensive debugging")
    print("   • Should have working dropdowns")
    
    print(f"\n🚀 Test it:")
    print(f"1. Open: file://{os.path.abspath(working_file)}")
    print("2. Open browser console (F12) to see debug messages")
    print("3. Select providers for Poet 1 and 2")
    print("4. Verify model dropdowns populate and enable")
    
    return working_file

if __name__ == "__main__":
    main()