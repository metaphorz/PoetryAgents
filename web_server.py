#!/usr/bin/env python3
"""
Flask web server for Poetry Agents web interface.
Provides API endpoints for model selection and poetry generation.
"""

import os
import json
from datetime import datetime
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from dialogue_manager import DialogueManager
from llm_client import LLMClient
from gemini_client import GeminiClient
from openai_client import OpenAIClient
from openrouter_client import OpenRouterClient

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Serve the HTML file
@app.route('/')
def index():
    return send_file('index.html')

# API endpoint to get available models for a provider
@app.route('/api/models/<provider>')
def get_models(provider):
    """Get available models for a specific provider."""
    try:
        if provider == 'claude':
            models = LLMClient.get_available_models()
        elif provider == 'gemini':
            models = GeminiClient.get_available_models()
        elif provider == 'openai':
            models = OpenAIClient.get_available_models()
        elif provider == 'openrouter':
            # Fetch all available OpenRouter models from API
            models = OpenRouterClient.get_available_models(limit_recent=None)
        else:
            return jsonify({'error': 'Unknown provider'}), 400
        
        return jsonify(models)
    
    except Exception as e:
        return jsonify({'error': f'Failed to load models: {str(e)}'}), 500

# API endpoint to generate poetry
@app.route('/api/generate', methods=['POST'])
def generate_poetry():
    """Generate poetry dialogue based on user parameters."""
    try:
        data = request.json
        
        # Validate required fields (emojis is optional boolean)
        required_fields = ['poet1Provider', 'poet1Model', 'poet2Provider', 'poet2Model', 
                          'theme', 'form', 'conversationLength']
        
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Handle optional useEmojis field (default to False)
        if 'useEmojis' not in data:
            data['useEmojis'] = False
        
        # Convert web form data to dialogue manager format
        config = convert_web_data_to_config(data)
        
        # Generate dialogue
        manager = DialogueManager()
        dialogue_data = manager.generate_dialogue(config)
        
        # Save to markdown file
        filename = manager.save_dialogue_to_markdown(dialogue_data)
        
        return jsonify({
            'success': True,
            'filename': os.path.basename(filename),
            'full_path': filename
        })
        
    except Exception as e:
        app.logger.error(f"Poetry generation error: {str(e)}")
        return jsonify({'error': f'Poetry generation failed: {str(e)}'}), 500

def convert_web_data_to_config(data):
    """Convert web form data to dialogue manager configuration format."""
    
    # Determine if using OpenRouter
    use_openrouter = (data['poet1Provider'] == 'openrouter' or 
                     data['poet2Provider'] == 'openrouter')
    
    # Map poetry forms that need length specification
    form = data['form']
    if form in ['haiku', 'sonnet', 'villanelle', 'limerick', 'tanka']:
        # Fixed forms have predetermined lengths
        fixed_lengths = {
            'haiku': 3,
            'sonnet': 14,
            'villanelle': 19,
            'limerick': 5,
            'tanka': 5
        }
        poem_length = fixed_lengths[form]
        length_unit = 'lines'
    else:
        # Variable forms default to reasonable values
        if form == 'prose':
            poem_length = 2  # 2 paragraphs
            length_unit = 'paragraphs'
        elif form == 'ballad':
            poem_length = 4  # 4 stanzas
            length_unit = 'stanzas'
        elif form == 'ghazal':
            poem_length = 7  # 7 couplets
            length_unit = 'couplets'
        else:
            poem_length = 4  # Default
            length_unit = 'lines'
    
    config = {
        'theme': data['theme'],
        'num_agents': 2,
        'form': form,
        'poem_length': poem_length,
        'length_unit': length_unit,
        'conversation_length': int(data['conversationLength']),
        'use_openrouter': use_openrouter,
        'use_emojis': data['useEmojis'],
        'output_format': 'markdown'
    }
    
    # Set up agent configurations
    if use_openrouter:
        # OpenRouter mode
        config.update({
            'agent1_llm': 'OpenRouter',
            'agent2_llm': 'OpenRouter',
            'agent1_openrouter_search': data['poet1Model'] if data['poet1Provider'] == 'openrouter' else 'anthropic/claude-3.5-sonnet',
            'agent2_openrouter_search': data['poet2Model'] if data['poet2Provider'] == 'openrouter' else 'anthropic/claude-3.5-sonnet',
            'agent1_claude_model': None,
            'agent1_gemini_model': None,
            'agent1_openai_model': None,
            'agent2_claude_model': None,
            'agent2_gemini_model': None,
            'agent2_openai_model': None
        })
    else:
        # Direct API mode - fix case sensitivity 
        def normalize_provider_name(provider):
            provider_lower = provider.lower()
            if provider_lower == 'openai':
                return 'OpenAI'
            elif provider_lower == 'claude':
                return 'Claude'
            elif provider_lower == 'gemini':
                return 'Gemini'
            else:
                return provider.title()
        
        config.update({
            'agent1_llm': normalize_provider_name(data['poet1Provider']),
            'agent2_llm': normalize_provider_name(data['poet2Provider']),
            'agent1_openrouter_search': None,
            'agent2_openrouter_search': None
        })
        
        # Set specific models for each agent
        for agent_num, provider_key, model_key in [
            (1, 'poet1Provider', 'poet1Model'),
            (2, 'poet2Provider', 'poet2Model')
        ]:
            provider = data[provider_key]
            model_id = data[model_key]
            
            # Initialize all model configs to None
            config[f'agent{agent_num}_claude_model'] = None
            config[f'agent{agent_num}_gemini_model'] = None
            config[f'agent{agent_num}_openai_model'] = None
            
            # Convert model ID back to display name for proper display
            display_name = model_id  # fallback
            provider_lower = provider.lower()
            
            try:
                if provider_lower == 'claude':
                    claude_models = LLMClient.get_available_models()
                    # Find display name from model ID
                    for disp_name, model_id_check in claude_models.items():
                        if model_id_check == model_id:
                            display_name = disp_name
                            break
                    config[f'agent{agent_num}_claude_model'] = display_name
                    
                elif provider_lower == 'gemini':
                    gemini_models = GeminiClient.get_available_models()
                    # Find display name from model ID
                    for disp_name, model_id_check in gemini_models.items():
                        if model_id_check == model_id:
                            display_name = disp_name
                            break
                    config[f'agent{agent_num}_gemini_model'] = display_name
                    
                elif provider_lower == 'openai':
                    openai_models = OpenAIClient.get_available_models()
                    # Find display name from model ID
                    for disp_name, model_id_check in openai_models.items():
                        if model_id_check == model_id:
                            display_name = disp_name
                            break
                    config[f'agent{agent_num}_openai_model'] = display_name
                    
            except Exception as e:
                # If we can't fetch models, just use the model_id
                if provider_lower == 'claude':
                    config[f'agent{agent_num}_claude_model'] = model_id
                elif provider_lower == 'gemini':
                    config[f'agent{agent_num}_gemini_model'] = model_id
                elif provider_lower == 'openai':
                    config[f'agent{agent_num}_openai_model'] = model_id
    
    return config

# Endpoint to download generated files
@app.route('/download/<filename>')
def download_file(filename):
    """Download a generated poetry file."""
    try:
        return send_from_directory('outputs', filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

# Health check endpoint
@app.route('/api/health')
def health_check():
    """Simple health check endpoint."""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Ensure outputs directory exists
    os.makedirs('outputs', exist_ok=True)
    
    # Run the server
    print("🚀 Starting Poetry Agents Web Server...")
    print("📱 Open your browser to: http://localhost:8080")
    print("🛑 Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=8080)