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
