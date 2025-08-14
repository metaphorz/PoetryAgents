"""
Coverage tests for llm_factory.py - the new factory pattern implementation
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from llm_factory import LLMClientFactory

class TestLLMClientFactory(unittest.TestCase):
    """Comprehensive coverage tests for LLMClientFactory"""
    
    def test_validate_configuration_complete_success(self):
        """Test successful validation with complete configuration"""
        config = {
            'theme': 'winter landscape',
            'form': 'haiku', 
            'poem_length': 3,
            'conversation_length': 2,
            'use_openrouter': False,
            'agent1_llm': 'Claude',
            'agent2_llm': 'Gemini',
            'num_agents': 2
        }
        
        result = LLMClientFactory.validate_configuration(config)
        self.assertTrue(result)
    
    def test_validate_configuration_missing_theme(self):
        """Test validation fails when theme is missing"""
        config = {
            'form': 'haiku',
            'poem_length': 3,
            'conversation_length': 1
        }
        
        with self.assertRaises(ValueError) as context:
            LLMClientFactory.validate_configuration(config)
        
        self.assertIn('Missing required configuration key: theme', str(context.exception))
    
    def test_validate_configuration_missing_form(self):
        """Test validation fails when form is missing"""
        config = {
            'theme': 'test',
            'poem_length': 3,
            'conversation_length': 1
        }
        
        with self.assertRaises(ValueError) as context:
            LLMClientFactory.validate_configuration(config)
        
        self.assertIn('Missing required configuration key: form', str(context.exception))
    
    def test_validate_configuration_missing_poem_length(self):
        """Test validation fails when poem_length is missing"""
        config = {
            'theme': 'test',
            'form': 'haiku',
            'conversation_length': 1
        }
        
        with self.assertRaises(ValueError) as context:
            LLMClientFactory.validate_configuration(config)
        
        self.assertIn('Missing required configuration key: poem_length', str(context.exception))
    
    def test_validate_configuration_missing_conversation_length(self):
        """Test validation fails when conversation_length is missing"""
        config = {
            'theme': 'test',
            'form': 'haiku',
            'poem_length': 3
        }
        
        with self.assertRaises(ValueError) as context:
            LLMClientFactory.validate_configuration(config)
        
        self.assertIn('Missing required configuration key: conversation_length', str(context.exception))
    
    def test_validate_configuration_openrouter_missing_agent1_search(self):
        """Test validation fails when OpenRouter is used but agent1 search term missing"""
        config = {
            'theme': 'test',
            'form': 'haiku',
            'poem_length': 3,
            'conversation_length': 1,
            'use_openrouter': True,
            'agent2_openrouter_search': 'claude-3-sonnet'
        }
        
        with self.assertRaises(ValueError) as context:
            LLMClientFactory.validate_configuration(config)
        
        self.assertIn('Missing OpenRouter search term for agent 1', str(context.exception))
    
    def test_validate_configuration_openrouter_missing_agent2_search(self):
        """Test validation fails when OpenRouter is used but agent2 search term missing"""
        config = {
            'theme': 'test',
            'form': 'haiku', 
            'poem_length': 3,
            'conversation_length': 1,
            'use_openrouter': True,
            'agent1_openrouter_search': 'claude-3-sonnet'
        }
        
        with self.assertRaises(ValueError) as context:
            LLMClientFactory.validate_configuration(config)
        
        self.assertIn('Missing OpenRouter search term for agent 2', str(context.exception))
    
    def test_validate_configuration_direct_api_missing_agent1_llm(self):
        """Test validation fails when direct API is used but agent1 LLM missing"""
        config = {
            'theme': 'test',
            'form': 'haiku',
            'poem_length': 3,
            'conversation_length': 1,
            'use_openrouter': False,
            'agent2_llm': 'Gemini'
        }
        
        with self.assertRaises(ValueError) as context:
            LLMClientFactory.validate_configuration(config)
        
        self.assertIn('Missing LLM choice for agent 1', str(context.exception))
    
    def test_validate_configuration_direct_api_missing_agent2_llm(self):
        """Test validation fails when direct API is used but agent2 LLM missing"""
        config = {
            'theme': 'test',
            'form': 'haiku',
            'poem_length': 3,
            'conversation_length': 1, 
            'use_openrouter': False,
            'agent1_llm': 'Claude'
        }
        
        with self.assertRaises(ValueError) as context:
            LLMClientFactory.validate_configuration(config)
        
        self.assertIn('Missing LLM choice for agent 2', str(context.exception))
    
    def test_get_client_display_name_claude(self):
        """Test display name generation for Claude"""
        config = {
            'use_openrouter': False,
            'agent1_llm': 'Claude',
            'agent1_claude_model': 'Claude Sonnet 4'
        }
        
        display_name = LLMClientFactory.get_client_display_name(config, 1)
        self.assertEqual(display_name, 'Claude (Claude Sonnet 4)')
    
    def test_get_client_display_name_gemini(self):
        """Test display name generation for Gemini"""
        config = {
            'use_openrouter': False,
            'agent2_llm': 'Gemini',
            'agent2_gemini_model': 'Gemini 2.5 Pro'
        }
        
        display_name = LLMClientFactory.get_client_display_name(config, 2)
        self.assertEqual(display_name, 'Gemini (Gemini 2.5 Pro)')
    
    def test_get_client_display_name_openai(self):
        """Test display name generation for OpenAI"""
        config = {
            'use_openrouter': False,
            'agent1_llm': 'OpenAI',
            'agent1_openai_model': 'GPT-4o'
        }
        
        display_name = LLMClientFactory.get_client_display_name(config, 1)
        self.assertEqual(display_name, 'OpenAI (GPT-4o)')
    
    def test_get_client_display_name_openrouter(self):
        """Test display name generation for OpenRouter"""
        config = {
            'use_openrouter': True,
            'agent1_openrouter_search': 'anthropic/claude-3-sonnet'
        }
        
        display_name = LLMClientFactory.get_client_display_name(config, 1)
        self.assertEqual(display_name, 'OpenRouter (anthropic/claude-3-sonnet)')
    
    def test_get_client_display_name_defaults(self):
        """Test display name generation with default values"""
        config = {
            'use_openrouter': False,
            'agent1_llm': 'Claude'
            # Missing agent1_claude_model - should use default
        }
        
        display_name = LLMClientFactory.get_client_display_name(config, 1)
        self.assertEqual(display_name, 'Claude (Claude Sonnet 4)')
    
    def test_get_client_display_name_unknown_provider(self):
        """Test display name generation for unknown provider"""
        config = {
            'use_openrouter': False,
            'agent1_llm': 'UnknownProvider'
        }
        
        display_name = LLMClientFactory.get_client_display_name(config, 1)
        self.assertEqual(display_name, 'Unknown')
    
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'})
    @patch('llm_client.LLMClient')
    def test_create_client_claude(self, mock_llm_client):
        """Test client creation for Claude"""
        config = {
            'use_openrouter': False,
            'agent1_llm': 'Claude',
            'agent1_claude_model': 'Claude Sonnet 4'
        }
        
        mock_instance = MagicMock()
        mock_llm_client.return_value = mock_instance
        
        result = LLMClientFactory.create_client(config, 1)
        
        mock_llm_client.assert_called_once_with('Claude Sonnet 4')
        self.assertEqual(result, mock_instance)
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'})
    @patch('gemini_client.GeminiClient')
    def test_create_client_gemini(self, mock_gemini_client):
        """Test client creation for Gemini"""
        config = {
            'use_openrouter': False,
            'agent2_llm': 'Gemini',
            'agent2_gemini_model': 'Gemini 2.5 Flash'
        }
        
        mock_instance = MagicMock()
        mock_gemini_client.return_value = mock_instance
        
        result = LLMClientFactory.create_client(config, 2)
        
        mock_gemini_client.assert_called_once_with('Gemini 2.5 Flash')
        self.assertEqual(result, mock_instance)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    @patch('openai_client.OpenAIClient')
    def test_create_client_openai(self, mock_openai_client):
        """Test client creation for OpenAI"""
        config = {
            'use_openrouter': False,
            'agent1_llm': 'OpenAI',
            'agent1_openai_model': 'GPT-4o'
        }
        
        mock_instance = MagicMock()
        mock_openai_client.return_value = mock_instance
        
        result = LLMClientFactory.create_client(config, 1)
        
        mock_openai_client.assert_called_once_with('GPT-4o')
        self.assertEqual(result, mock_instance)
    
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'})
    @patch('openrouter_client.OpenRouterClient')
    def test_create_client_openrouter(self, mock_openrouter_client):
        """Test client creation for OpenRouter"""
        config = {
            'use_openrouter': True,
            'agent1_openrouter_search': 'anthropic/claude-3-sonnet'
        }
        
        mock_instance = MagicMock()
        mock_openrouter_client.return_value = mock_instance
        
        result = LLMClientFactory.create_client(config, 1)
        
        mock_openrouter_client.assert_called_once_with('anthropic/claude-3-sonnet')
        self.assertEqual(result, mock_instance)
    
    def test_create_client_unsupported_llm(self):
        """Test client creation fails for unsupported LLM"""
        config = {
            'use_openrouter': False,
            'agent1_llm': 'UnsupportedLLM'
        }
        
        with self.assertRaises(ValueError) as context:
            LLMClientFactory.create_client(config, 1)
        
        self.assertIn('Unsupported LLM choice: UnsupportedLLM', str(context.exception))

if __name__ == '__main__':
    unittest.main()