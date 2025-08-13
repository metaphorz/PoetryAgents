#!/usr/bin/env python3
"""
Test script for LLMClientFactory
"""

import sys
import os
# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

import unittest
from unittest.mock import Mock, patch
from llm_factory import LLMClientFactory
from exceptions import ConfigurationError

class TestLLMClientFactory(unittest.TestCase):
    """Test cases for LLMClientFactory"""
    
    def test_validate_configuration_success(self):
        """Test successful configuration validation"""
        config = {
            'theme': 'test theme',
            'form': 'haiku',
            'poem_length': 3,
            'conversation_length': 1,
            'use_openrouter': False,
            'agent1_llm': 'Claude',
            'agent2_llm': 'Gemini'
        }
        
        self.assertTrue(LLMClientFactory.validate_configuration(config))
    
    def test_validate_configuration_missing_required_key(self):
        """Test validation fails with missing required key"""
        config = {
            'theme': 'test theme',
            'form': 'haiku'
            # Missing poem_length, conversation_length
        }
        
        with self.assertRaises(ValueError) as context:
            LLMClientFactory.validate_configuration(config)
        self.assertIn('Missing required configuration key', str(context.exception))
    
    def test_validate_configuration_openrouter_missing_search(self):
        """Test validation fails when OpenRouter is used but search terms missing"""
        config = {
            'theme': 'test theme',
            'form': 'haiku',
            'poem_length': 3,
            'conversation_length': 1,
            'use_openrouter': True,
            'agent2_openrouter_search': 'Claude'
            # Missing agent1_openrouter_search
        }
        
        with self.assertRaises(ValueError) as context:
            LLMClientFactory.validate_configuration(config)
        self.assertIn('Missing OpenRouter search term', str(context.exception))
    
    def test_get_client_display_name_claude(self):
        """Test display name generation for Claude"""
        config = {
            'use_openrouter': False,
            'agent1_llm': 'Claude',
            'agent1_claude_model': 'Claude Sonnet 4'
        }
        
        display_name = LLMClientFactory.get_client_display_name(config, 1)
        self.assertEqual(display_name, 'Claude (Claude Sonnet 4)')
    
    def test_get_client_display_name_openrouter(self):
        """Test display name generation for OpenRouter"""
        config = {
            'use_openrouter': True,
            'agent1_openrouter_search': 'anthropic/claude-3-sonnet'
        }
        
        display_name = LLMClientFactory.get_client_display_name(config, 1)
        self.assertEqual(display_name, 'OpenRouter (anthropic/claude-3-sonnet)')
    
    def test_get_client_display_name_gemini(self):
        """Test display name generation for Gemini"""
        config = {
            'use_openrouter': False,
            'agent2_llm': 'Gemini',
            'agent2_gemini_model': 'Gemini 2.5 Flash'
        }
        
        display_name = LLMClientFactory.get_client_display_name(config, 2)
        self.assertEqual(display_name, 'Gemini (Gemini 2.5 Flash)')
    
    def test_get_client_display_name_openai(self):
        """Test display name generation for OpenAI"""
        config = {
            'use_openrouter': False,
            'agent1_llm': 'OpenAI',
            'agent1_openai_model': 'GPT-4o'
        }
        
        display_name = LLMClientFactory.get_client_display_name(config, 1)
        self.assertEqual(display_name, 'OpenAI (GPT-4o)')
    
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'})
    @patch('llm_client.LLMClient')
    def test_create_client_claude_direct_api(self, mock_llm_client):
        """Test client creation for Claude direct API"""
        config = {
            'use_openrouter': False,
            'agent1_llm': 'Claude',
            'agent1_claude_model': 'Claude Sonnet 4'
        }
        
        mock_client_instance = Mock()
        mock_llm_client.return_value = mock_client_instance
        
        result = LLMClientFactory.create_client(config, 1)
        
        mock_llm_client.assert_called_once_with('Claude Sonnet 4')
        self.assertEqual(result, mock_client_instance)
    
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'})
    @patch('openrouter_client.OpenRouterClient')
    def test_create_client_openrouter(self, mock_openrouter_client):
        """Test client creation for OpenRouter"""
        config = {
            'use_openrouter': True,
            'agent1_openrouter_search': 'anthropic/claude-3-sonnet'
        }
        
        mock_client_instance = Mock()
        mock_openrouter_client.return_value = mock_client_instance
        
        result = LLMClientFactory.create_client(config, 1)
        
        mock_openrouter_client.assert_called_once_with('anthropic/claude-3-sonnet')
        self.assertEqual(result, mock_client_instance)
    
    def test_create_client_unsupported_llm(self):
        """Test client creation fails for unsupported LLM"""
        config = {
            'use_openrouter': False,
            'agent1_llm': 'UnsupportedLLM'
        }
        
        with self.assertRaises(ValueError) as context:
            LLMClientFactory.create_client(config, 1)
        self.assertIn('Unsupported LLM choice', str(context.exception))

def run_tests():
    """Run all tests and return results"""
    print("Testing LLMClientFactory...")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestLLMClientFactory)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ All LLMClientFactory tests passed!")
        return True
    else:
        print(f"❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        return False

if __name__ == "__main__":
    run_tests()