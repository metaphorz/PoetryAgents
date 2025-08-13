"""
LLM Client for Anthropic API integration
Handles communication with Sonnet 4 for poetry generation.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

try:
    import anthropic
except ImportError:
    print("Anthropic library not found. Install with: pip install anthropic")
    anthropic = None

class LLMClient:
    """Client for interacting with Anthropic's Claude models."""
    
    @classmethod
    def get_available_models(cls, limit_recent=6):
        """Dynamically fetch available Claude models from the API.
        
        Args:
            limit_recent: If specified, return only the N most recent models
        """
        try:
            # Initialize a temporary client to fetch models
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable is required")
            
            temp_client = anthropic.Anthropic(api_key=api_key)
            models = temp_client.models.list(limit=50)
            
            # Sort models by creation date (newest first)
            sorted_models = sorted(models.data, key=lambda x: x.created_at, reverse=True)
            
            # Limit to most recent if specified
            if limit_recent:
                sorted_models = sorted_models[:limit_recent]
            
            # Build models dict with display names
            available_models = {}
            for model in sorted_models:
                # Use display name as key, model ID as value
                available_models[model.display_name] = model.id
            
            return available_models
        except Exception as e:
            # Fallback to known models if API fails - Sonnet 4 as default
            return {
                "Claude Sonnet 4": "claude-sonnet-4-20250514",
                "Claude Opus 4.1": "claude-opus-4-1-20250805", 
                "Claude Sonnet 3.7": "claude-3-7-sonnet-20250219",
                "Claude Sonnet 3.5 (New)": "claude-3-5-sonnet-20241022",
                "Claude Haiku 3.5": "claude-3-5-haiku-20241022",
                "Claude Sonnet 3.5 (Old)": "claude-3-5-sonnet-20240620"
            }
    
    def __init__(self, model: str = None):
        """Initialize the LLM client.
        
        Args:
            model: Model display name from get_available_models()
        """
        if not anthropic:
            raise ImportError("Anthropic library is required")
        
        # Get API key from environment
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
            
        self.client = anthropic.Anthropic(api_key=api_key)
        
        # Get available models dynamically
        available_models = self.get_available_models()
        
        # Use default if no model specified
        if model is None:
            model = list(available_models.keys())[0]  # Use first available model
        
        # Set model based on selection
        if model not in available_models:
            raise ValueError(f"Model '{model}' not available. Choose from: {list(available_models.keys())}")
        
        self.model = available_models[model]
        self.model_name = model
    
    def generate_poetry(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Generate poetry using the LLM.
        
        Args:
            prompt: The prompt for poetry generation
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Generated poetry text
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=0.7,  # Some creativity but not too random
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            raise Exception(f"Error generating poetry: {str(e)}")
    
    def test_connection(self) -> bool:
        """
        Test the connection to the API.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            test_response = self.generate_poetry("Write a simple two-word poem.", max_tokens=10)
            return len(test_response.strip()) > 0
        except Exception:
            return False