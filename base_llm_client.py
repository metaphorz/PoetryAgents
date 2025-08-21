"""
Base class for all LLM clients to eliminate code duplication.
Provides common functionality for API key management, model handling, and poetry generation.
Includes security measures for input validation and error handling.
"""

import os
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv
from security_utils import SecurityValidator, SecureErrorHandler, SecurityValidationResult

load_dotenv()

class BaseLLMClient(ABC):
    """Abstract base class for all LLM clients."""
    
    def __init__(self, model: str = None, api_key_env: str = None):
        """
        Initialize the base LLM client.
        
        Args:
            model: Model display name from get_available_models()
            api_key_env: Environment variable name for API key
        """
        self.api_key_env = api_key_env
        self.api_key = self._get_api_key()
        self.available_models = self.__class__.get_available_models()
        self.model, self.model_name = self._initialize_model(model)
        self._initialize_client()
    
    def _get_api_key(self) -> str:
        """Get API key from environment variables."""
        if not self.api_key_env:
            raise ValueError("API key environment variable name not specified")
        
        api_key = os.getenv(self.api_key_env)
        if not api_key:
            raise ValueError(f"{self.api_key_env} environment variable is required")
        
        return api_key
    
    def _initialize_model(self, model: str) -> Tuple[str, str]:
        """
        Initialize model selection with security validation.
        
        Args:
            model: Model display name OR model ID
            
        Returns:
            Tuple of (model_id, model_name)
        """
        # Use default if no model specified
        if model is None:
            model = list(self.available_models.keys())[0]
        
        # Validate model parameter for security
        is_valid, sanitized_model = SecurityValidator.validate_model_parameter(model)
        if not is_valid:
            raise ValueError("Invalid model parameter provided")
        
        model = sanitized_model
        
        # Check if it's a display name (key) or model ID (value)
        if model in self.available_models:
            # It's a display name, get the model ID
            return self.available_models[model], model
        elif model in self.available_models.values():
            # It's a model ID, find the display name
            for display_name, model_id in self.available_models.items():
                if model_id == model:
                    return model_id, display_name
        
        # If we get here, the model wasn't found
        raise ValueError("Specified model is not available")
    
    @classmethod
    @abstractmethod
    def get_available_models(cls, limit_recent: int = 6) -> Dict[str, str]:
        """
        Get available models for this provider.
        
        Args:
            limit_recent: Number of recent models to return
            
        Returns:
            Dict mapping display names to model IDs
        """
        pass
    
    @abstractmethod
    def _initialize_client(self):
        """Initialize the provider-specific client."""
        pass
    
    def _validate_and_sanitize_input(self, prompt: str, max_tokens: int = 500) -> Tuple[str, int, List[str]]:
        """
        Validate and sanitize input parameters for security.
        
        Args:
            prompt: The prompt for poetry generation
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Tuple of (sanitized_prompt, validated_max_tokens, warnings)
        """
        # Validate and sanitize prompt
        validation_result = SecurityValidator.sanitize_prompt(prompt)
        
        if not validation_result.is_safe:
            SecureErrorHandler.log_error_securely(
                ValueError("Potentially dangerous prompt blocked"),
                "prompt_validation",
                prompt
            )
            # Still allow execution with sanitized content for user experience
            # but log the security event
        
        # Validate max_tokens
        is_valid_tokens, validated_tokens = SecurityValidator.validate_max_tokens(max_tokens)
        if not is_valid_tokens:
            validation_result.warnings.append(f"max_tokens adjusted from {max_tokens} to {validated_tokens}")
        
        return validation_result.sanitized_content, validated_tokens, validation_result.warnings
    
    @abstractmethod
    def generate_poetry(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Generate poetry using the LLM with security validation.
        
        Args:
            prompt: The prompt for poetry generation
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Generated poetry text
        """
        pass
    
    def test_connection(self) -> bool:
        """
        Test the connection to the API with secure error handling.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            test_response = self.generate_poetry("Write a simple two-word poem.", max_tokens=10)
            return len(test_response.strip()) > 0
        except Exception as e:
            # Log error securely without exposing details to caller
            SecureErrorHandler.log_error_securely(e, "connection_test")
            return False
    
    def get_model_info(self) -> Dict[str, str]:
        """Get information about the current model."""
        return {
            'provider': self.__class__.__name__.replace('Client', ''),
            'model_name': self.model_name,
            'model_id': self.model
        }