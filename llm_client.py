"""
Claude LLM Client for Anthropic API integration.
Refactored to use BaseLLMClient for consistency and reduced duplication.
"""

import os
from typing import Dict
from base_llm_client import BaseLLMClient
from exceptions import APIError, ModelNotAvailableError

try:
    import anthropic
except ImportError:
    print("Anthropic library not found. Install with: pip install anthropic")
    anthropic = None

class LLMClient(BaseLLMClient):
    """Client for interacting with Anthropic's Claude models."""
    
    def __init__(self, model: str = None):
        """Initialize the Claude client."""
        if not anthropic:
            raise ImportError("Anthropic library is required")
        
        super().__init__(model, 'ANTHROPIC_API_KEY')
    
    @classmethod
    def get_available_models(cls, limit_recent: int = 6) -> Dict[str, str]:
        """Get available Claude models from the API."""
        try:
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
                available_models[model.display_name] = model.id
            
            return available_models
        except Exception as e:
            raise Exception(f"Failed to fetch Claude models: {str(e)}")
    
    def _initialize_client(self):
        """Initialize the Anthropic client."""
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def generate_poetry(self, prompt: str, max_tokens: int = 500) -> str:
        """Generate poetry using Claude."""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            raise APIError("Claude", f"Poetry generation failed: {str(e)}", e)