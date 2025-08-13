"""
Factory for creating LLM clients with standardized configuration.
Centralizes client creation and removes duplication from dialogue_manager.py
"""

from typing import Dict, Any, Optional
from base_llm_client import BaseLLMClient

class LLMClientFactory:
    """Factory for creating LLM clients."""
    
    @staticmethod
    def create_client(config: Dict[str, Any], agent_number: int) -> BaseLLMClient:
        """
        Create an LLM client based on configuration.
        
        Args:
            config: Configuration dictionary from user input
            agent_number: 1 or 2 for agent1/agent2 settings
            
        Returns:
            Configured LLM client instance
        """
        # Determine agent-specific settings
        agent_key = f'agent{agent_number}'
        llm_choice = config.get(f'{agent_key}_llm', 'Claude')
        
        if config.get('use_openrouter', False):
            # OpenRouter path
            from openrouter_client import OpenRouterClient
            search_term = config.get(f'{agent_key}_openrouter_search', 'Claude')
            return OpenRouterClient(search_term)
        
        else:
            # Direct API path
            if llm_choice == 'Claude':
                from llm_client import LLMClient
                model = config.get(f'{agent_key}_claude_model', 'Claude Sonnet 4')
                return LLMClient(model)
                
            elif llm_choice == 'Gemini':
                from gemini_client import GeminiClient  
                model = config.get(f'{agent_key}_gemini_model', 'Gemini 2.5 Flash')
                return GeminiClient(model)
                
            elif llm_choice == 'OpenAI':
                from openai_client import OpenAIClient
                model = config.get(f'{agent_key}_openai_model', 'GPT-4o')
                return OpenAIClient(model)
                
            else:
                raise ValueError(f"Unsupported LLM choice: {llm_choice}")
    
    @staticmethod
    def get_client_display_name(config: Dict[str, Any], agent_number: int) -> str:
        """
        Get display name for the client based on configuration.
        
        Args:
            config: Configuration dictionary
            agent_number: 1 or 2 for agent1/agent2
            
        Returns:
            Display name string for the LLM
        """
        agent_key = f'agent{agent_number}'
        
        if config.get('use_openrouter', False):
            search_term = config.get(f'{agent_key}_openrouter_search', 'Claude')
            return f"OpenRouter ({search_term})"
        
        else:
            llm_choice = config.get(f'{agent_key}_llm', 'Claude')
            
            if llm_choice == 'Claude':
                model = config.get(f'{agent_key}_claude_model', 'Claude Sonnet 4')
                return f"Claude ({model})"
            elif llm_choice == 'Gemini':
                model = config.get(f'{agent_key}_gemini_model', 'Gemini 2.5 Flash')  
                return f"Gemini ({model})"
            elif llm_choice == 'OpenAI':
                model = config.get(f'{agent_key}_openai_model', 'GPT-4o')
                return f"OpenAI ({model})"
            
        return "Unknown"
    
    @staticmethod
    def validate_configuration(config: Dict[str, Any]) -> bool:
        """
        Validate that the configuration has all required settings.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            True if configuration is valid
            
        Raises:
            ValueError: If configuration is invalid
        """
        required_keys = ['theme', 'form', 'poem_length', 'conversation_length']
        
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required configuration key: {key}")
        
        # Validate agent configurations
        for agent_num in [1, 2]:
            agent_key = f'agent{agent_num}'
            
            if config.get('use_openrouter', False):
                search_key = f'{agent_key}_openrouter_search'
                if search_key not in config:
                    raise ValueError(f"Missing OpenRouter search term for agent {agent_num}")
            else:
                llm_key = f'{agent_key}_llm'
                if llm_key not in config:
                    raise ValueError(f"Missing LLM choice for agent {agent_num}")
        
        return True