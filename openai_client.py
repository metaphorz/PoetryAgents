"""
OpenAI Client for OpenAI API integration
Handles communication with OpenAI models for poetry generation.
"""

import os
from typing import Optional
from dotenv import load_dotenv
from base_llm_client import BaseLLMClient

# Load environment variables from .env file
load_dotenv()

try:
    import openai
except ImportError:
    print("OpenAI library not found. Install with: pip install openai")
    openai = None

class OpenAIClient(BaseLLMClient):
    """Client for interacting with OpenAI's models."""
    
    @classmethod
    def get_available_models(cls, limit_recent=6):
        """Dynamically fetch available OpenAI models from the API.
        
        Args:
            limit_recent: If specified, return only the N most recent models
        """
        try:
            # Initialize temporary client to fetch models
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable is required")
            
            temp_client = openai.OpenAI(api_key=api_key)
            models = temp_client.models.list()
            
            # Filter for chat completion models and sort by creation date
            chat_models = []
            # Exclude models that don't work with chat completions
            excluded_patterns = ['deep-research', 'audio', 'realtime', 'image', 'tts', 'transcribe', 'search']
            
            for model in models.data:
                if any(keyword in model.id for keyword in ['gpt-4', 'gpt-3.5', 'o1', 'o3', 'chatgpt']):
                    # Skip models that use different endpoints
                    if not any(pattern in model.id for pattern in excluded_patterns):
                        chat_models.append(model)
            
            # Sort by creation date (newest first)
            chat_models.sort(key=lambda x: x.created, reverse=True)
            
            # Limit to most recent if specified
            if limit_recent:
                chat_models = chat_models[:limit_recent]
            
            # Build models dict - use model ID as both key and value for simplicity
            available_models = {}
            for model in chat_models:
                # Create a display name from model ID
                display_name = model.id.replace('-', ' ').title()
                available_models[display_name] = model.id
            
            return available_models
        except Exception as e:
            raise Exception(f"Failed to fetch OpenAI models: {str(e)}")
    
    def __init__(self, model: str = None):
        """Initialize the OpenAI client.
        
        Args:
            model: Model display name from get_available_models()
        """
        # Call parent constructor with API key environment variable
        super().__init__(model, 'OPENAI_API_KEY')
    
    def _initialize_client(self):
        """Initialize the OpenAI client."""
        if not openai:
            raise ImportError("OpenAI library is required")
            
        self.client = openai.OpenAI(api_key=self.api_key)
    
    def generate_poetry(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Generate poetry using OpenAI.
        
        Args:
            prompt: The prompt for poetry generation
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Generated poetry text
        """
        try:
            # Handle different parameters for different model types
            params = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            # Add model-specific parameters
            if any(model in self.model for model in ['o1', 'o3']):
                # o1/o3 models use different parameters
                params['max_completion_tokens'] = max_tokens
                # o1/o3 models don't support temperature, top_p, etc.
            else:
                # Standard GPT models
                params.update({
                    'max_tokens': max_tokens,
                    'temperature': 0.7,
                    'top_p': 1.0,
                    'frequency_penalty': 0.0,
                    'presence_penalty': 0.0
                })
            
            response = self.client.chat.completions.create(**params)
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"Error generating poetry with OpenAI: {str(e)}")