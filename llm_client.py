"""
Claude LLM Client for Anthropic API integration.
Refactored to use BaseLLMClient for consistency and reduced duplication.
Includes security improvements for input validation and error handling.
"""

import os
from typing import Dict
from base_llm_client import BaseLLMClient
from exceptions import APIError, ModelNotAvailableError
from security_utils import SecureErrorHandler

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
            SecureErrorHandler.log_error_securely(e, "claude_model_fetch")
            raise Exception("Failed to fetch Claude models")
    
    def _initialize_client(self):
        """Initialize the Anthropic client."""
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def generate_poetry(self, prompt: str, max_tokens: int = 500) -> str:
        """Generate poetry using Claude with security validation."""
        # Validate and sanitize input
        sanitized_prompt, validated_tokens, warnings = self._validate_and_sanitize_input(prompt, max_tokens)
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=validated_tokens,
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": sanitized_prompt
                    }
                ]
            )
            
            return response.content[0].text.strip()
            
        except anthropic.AuthenticationError as e:
            SecureErrorHandler.log_error_securely(e, "claude_auth", prompt)
            raise APIError("Claude", "Authentication failed. Please check your API key.", e)
        except anthropic.RateLimitError as e:
            SecureErrorHandler.log_error_securely(e, "claude_rate_limit", prompt)
            raise APIError("Claude", "Rate limit exceeded. Please wait and try again.", e)
        except anthropic.APIError as e:
            SecureErrorHandler.log_error_securely(e, "claude_api", prompt)
            raise APIError("Claude", "Service temporarily unavailable. Please try again later.", e)
        except Exception as e:
            SecureErrorHandler.log_error_securely(e, "claude_generation", prompt)
            raise APIError("Claude", "Poetry generation failed. Please try again.", e)