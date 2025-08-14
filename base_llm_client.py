"""
Base class for all LLM clients to eliminate code duplication.
Provides common functionality for API key management, model handling, and poetry generation.
"""

import os
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv

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
        self.available_models = self.get_available_models()
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
        Initialize model selection.
        
        Args:
            model: Model display name OR model ID
            
        Returns:
            Tuple of (model_id, model_name)
        """
        # Use default if no model specified
        if model is None:
            model = list(self.available_models.keys())[0]
        
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
        raise ValueError(f"Model '{model}' not available. Choose from: {list(self.available_models.keys())} or {list(self.available_models.values())}")
    
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
    
    @abstractmethod
    def generate_poetry(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Generate poetry using the LLM.
        
        Args:
            prompt: The prompt for poetry generation
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Generated poetry text
        """
        pass
    
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
    
    def get_model_info(self) -> Dict[str, str]:
        """Get information about the current model."""
        return {
            'provider': self.__class__.__name__.replace('Client', ''),
            'model_name': self.model_name,
            'model_id': self.model
        }