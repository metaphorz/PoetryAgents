"""
Configuration management for the Poetry Agent system.
Handles environment variables, settings, and validation.
"""

import os
from typing import Dict, Any, List
from dotenv import load_dotenv
from exceptions import ConfigurationError

class ConfigManager:
    """Manages configuration and environment settings."""
    
    def __init__(self):
        """Initialize configuration manager."""
        load_dotenv()
        self.required_env_vars = {
            'ANTHROPIC_API_KEY': 'Anthropic Claude API',
            'GEMINI_API_KEY': 'Google Gemini API', 
            'OPENAI_API_KEY': 'OpenAI API',
            'OPENROUTER_API_KEY': 'OpenRouter API'
        }
    
    def validate_api_keys(self, required_providers: List[str] = None) -> Dict[str, bool]:
        """
        Validate that required API keys are present.
        
        Args:
            required_providers: List of required providers ('claude', 'gemini', 'openai', 'openrouter')
            
        Returns:
            Dict mapping provider to availability status
        """
        provider_mapping = {
            'claude': 'ANTHROPIC_API_KEY',
            'gemini': 'GEMINI_API_KEY', 
            'openai': 'OPENAI_API_KEY',
            'openrouter': 'OPENROUTER_API_KEY'
        }
        
        status = {}
        for provider, env_var in provider_mapping.items():
            has_key = bool(os.getenv(env_var))
            status[provider] = has_key
            
            # Check if this provider is required but missing
            if required_providers and provider in required_providers and not has_key:
                raise ConfigurationError(f"Missing required API key: {env_var}")
        
        return status
    
    def get_api_key(self, provider: str) -> str:
        """
        Get API key for a specific provider.
        
        Args:
            provider: Provider name ('claude', 'gemini', 'openai', 'openrouter')
            
        Returns:
            API key string
            
        Raises:
            ConfigurationError: If API key is not found
        """
        env_var_mapping = {
            'claude': 'ANTHROPIC_API_KEY',
            'gemini': 'GEMINI_API_KEY',
            'openai': 'OPENAI_API_KEY', 
            'openrouter': 'OPENROUTER_API_KEY'
        }
        
        env_var = env_var_mapping.get(provider.lower())
        if not env_var:
            raise ConfigurationError(f"Unknown provider: {provider}")
        
        api_key = os.getenv(env_var)
        if not api_key:
            raise ConfigurationError(f"Missing API key for {provider}: {env_var}")
        
        return api_key
    
    def validate_dialogue_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate dialogue configuration.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            True if valid
            
        Raises:
            ConfigurationError: If configuration is invalid
        """
        required_keys = [
            'theme', 'num_agents', 'form', 'poem_length', 'conversation_length'
        ]
        
        for key in required_keys:
            if key not in config:
                raise ConfigurationError(f"Missing required configuration: {key}")
        
        # Validate form
        valid_forms = ['haiku', 'prose', 'sonnet', 'villanelle', 'limerick', 'ballad', 'ghazal', 'tanka']
        if config['form'] not in valid_forms:
            raise ConfigurationError(f"Invalid form: {config['form']}. Valid forms: {', '.join(valid_forms)}")
        
        # Validate numeric values
        if config['num_agents'] < 1:
            raise ConfigurationError("Number of agents must be at least 1")
        
        if config['poem_length'] < 1:
            raise ConfigurationError("Poem length must be at least 1")
        
        if config['conversation_length'] < 1:
            raise ConfigurationError("Conversation length must be at least 1")
        
        return True
    
    def get_available_providers(self) -> List[str]:
        """Get list of providers with available API keys."""
        available = []
        for provider in ['claude', 'gemini', 'openai', 'openrouter']:
            try:
                self.get_api_key(provider)
                available.append(provider)
            except ConfigurationError:
                continue
        
        return available
    
    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """Get default configuration values."""
        return {
            'theme': '',
            'num_agents': 2,
            'form': 'haiku',
            'poem_length': 3,
            'length_unit': 'lines',
            'conversation_length': 1,
            'use_openrouter': False,
            'use_emojis': False,
            'output_format': 'markdown'
        }