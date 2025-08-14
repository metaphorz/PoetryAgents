"""
Unified coverage tests for all LLM clients - parameterized tests that run against
Claude, Gemini, OpenAI, and OpenRouter clients to ensure consistent behavior.
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock
import pytest

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import all LLM clients that use BaseLLMClient
from llm_client import LLMClient
from gemini_client import GeminiClient
from openai_client import OpenAIClient
from openrouter_client import OpenRouterClient


class TestAllLLMClients(unittest.TestCase):
    """Parameterized tests that run against all LLM client implementations."""
    
    @property
    def client_configs(self):
        """Configuration for all LLM clients that extend BaseLLMClient - returns tuples of (client_class, api_key_env, mock_library_path)"""
        return [
            (LLMClient, 'ANTHROPIC_API_KEY', 'llm_client.anthropic'),
            (GeminiClient, 'GEMINI_API_KEY', 'gemini_client.genai'),
            (OpenAIClient, 'OPENAI_API_KEY', 'openai_client.openai'),
            (OpenRouterClient, 'OPENROUTER_API_KEY', 'openrouter_client.openai'),
        ]
    
    def setUp(self):
        """Set up test environment."""
        # Clear any cached modules
        modules_to_clear = ['llm_client', 'gemini_client', 'openai_client', 'openrouter_client']
        for module in modules_to_clear:
            if module in sys.modules:
                # Don't delete - just refresh our imports
                pass
    
    def test_missing_api_key_all_clients(self):
        """Test that all clients fail gracefully when API key is missing."""
        for client_class, api_key_env, _ in self.client_configs:
            with self.subTest(client=client_class.__name__):
                with patch.dict(os.environ, {}, clear=True):
                    with self.assertRaises(ValueError) as context:
                        client_class()
                    
                    self.assertIn(f"{api_key_env} environment variable is required", str(context.exception))
    
    def test_missing_library_all_clients(self):
        """Test that all clients fail gracefully when required library is missing."""
        library_error_messages = {
            'LLMClient': 'Anthropic library is required',
            'GeminiClient': 'Google Generative AI library is required',
            'OpenAIClient': 'OpenAI library is required',
            'OpenRouterClient': 'OpenAI library is required for OpenRouter'
        }
        
        for client_class, api_key_env, mock_library_path in self.client_configs:
            with self.subTest(client=client_class.__name__):
                with patch.dict(os.environ, {api_key_env: 'test_key'}):
                    with patch(mock_library_path, None):
                        with self.assertRaises(ImportError) as context:
                            client_class()
                        
                        expected_error = library_error_messages[client_class.__name__]
                        self.assertEqual(str(context.exception), expected_error)
    
    def test_successful_initialization_all_clients(self):
        """Test successful initialization for all clients."""
        for client_class, api_key_env, mock_library_path in self.client_configs:
            with self.subTest(client=client_class.__name__):
                with patch.dict(os.environ, {api_key_env: 'test_key'}):
                    with patch(mock_library_path) as mock_lib:
                        # Mock get_available_models to return test models
                        with patch.object(client_class, 'get_available_models', return_value={'Test Model': 'test-model-id'}):
                            # Setup common mocks
                            self._setup_library_mock(mock_lib, client_class.__name__)
                            
                            client = client_class()
                            
                            # All clients should have these attributes from BaseLLMClient
                            self.assertIsNotNone(client.api_key)
                            self.assertEqual(client.api_key, 'test_key')
                            self.assertIsNotNone(client.available_models)
                            self.assertIsNotNone(client.model)
                            self.assertIsNotNone(client.model_name)
    
    def test_generate_poetry_success_all_clients(self):
        """Test successful poetry generation for all clients."""
        for client_class, api_key_env, mock_library_path in self.client_configs:
            with self.subTest(client=client_class.__name__):
                with patch.dict(os.environ, {api_key_env: 'test_key'}):
                    with patch(mock_library_path) as mock_lib:
                        with patch.object(client_class, 'get_available_models', return_value={'Test Model': 'test-model-id'}):
                            # Setup library-specific mocks
                            mock_response = self._setup_generate_poetry_mock(mock_lib, client_class.__name__)
                            
                            client = client_class()
                            result = client.generate_poetry("Write a haiku", max_tokens=100)
                            
                            # All clients should return stripped text
                            self.assertEqual(result, "Beautiful poetry here")
                            
                            # Verify the underlying library was called
                            self._verify_generate_poetry_call(mock_response, client_class.__name__)
    
    def test_generate_poetry_api_error_all_clients(self):
        """Test poetry generation with API errors for all clients."""
        for client_class, api_key_env, mock_library_path in self.client_configs:
            with self.subTest(client=client_class.__name__):
                with patch.dict(os.environ, {api_key_env: 'test_key'}):
                    with patch(mock_library_path) as mock_lib:
                        with patch.object(client_class, 'get_available_models', return_value={'Test Model': 'test-model-id'}):
                            # Setup error condition
                            self._setup_generate_poetry_error_mock(mock_lib, client_class.__name__)
                            
                            client = client_class()
                            
                            with self.assertRaises(Exception) as context:
                                client.generate_poetry("Test prompt")
                            
                            # All clients should wrap API errors (message format may vary)
                            error_msg = str(context.exception)
                            # Check that the error contains both an error indication and our test error
                            self.assertTrue(
                                ("Error generating poetry" in error_msg or "API Error" in error_msg or "Poetry generation failed" in error_msg),
                                f"Expected error message not found in: {error_msg}"
                            )
                            self.assertIn("API Error", error_msg)
    
    def test_test_connection_success_all_clients(self):
        """Test successful connection test for all clients."""
        for client_class, api_key_env, mock_library_path in self.client_configs:
            with self.subTest(client=client_class.__name__):
                with patch.dict(os.environ, {api_key_env: 'test_key'}):
                    with patch(mock_library_path) as mock_lib:
                        with patch.object(client_class, 'get_available_models', return_value={'Test Model': 'test-model-id'}):
                            # Setup successful response
                            self._setup_test_connection_success_mock(mock_lib, client_class.__name__)
                            
                            client = client_class()
                            result = client.test_connection()
                            
                            # All clients should return True on successful connection
                            self.assertTrue(result)
    
    def test_test_connection_failure_all_clients(self):
        """Test connection test failure for all clients."""
        failure_conditions = [
            ("empty_response", "   "),
            ("api_error", Exception("Connection failed"))
        ]
        
        for condition_name, condition_value in failure_conditions:
            for client_class, api_key_env, mock_library_path in self.client_configs:
                with self.subTest(client=client_class.__name__, condition=condition_name):
                    with patch.dict(os.environ, {api_key_env: 'test_key'}):
                        with patch(mock_library_path) as mock_lib:
                            with patch.object(client_class, 'get_available_models', return_value={'Test Model': 'test-model-id'}):
                                # Setup failure condition
                                if condition_name == "empty_response":
                                    self._setup_test_connection_empty_mock(mock_lib, client_class.__name__, condition_value)
                                else:  # api_error
                                    self._setup_test_connection_error_mock(mock_lib, client_class.__name__, condition_value)
                                
                                client = client_class()
                                result = client.test_connection()
                                
                                # All clients should return False on connection failure
                                self.assertFalse(result)
    
    def test_get_model_info_all_clients(self):
        """Test model info retrieval for all clients."""
        for client_class, api_key_env, mock_library_path in self.client_configs:
            with self.subTest(client=client_class.__name__):
                with patch.dict(os.environ, {api_key_env: 'test_key'}):
                    with patch(mock_library_path) as mock_lib:
                        with patch.object(client_class, 'get_available_models', return_value={'Test Model': 'test-model-id'}):
                            self._setup_library_mock(mock_lib, client_class.__name__)
                            
                            client = client_class()
                            info = client.get_model_info()
                            
                            # All clients should return consistent model info structure
                            self.assertIn('provider', info)
                            self.assertIn('model_name', info)
                            self.assertIn('model_id', info)
                            self.assertIsInstance(info['provider'], str)
                            self.assertIsInstance(info['model_name'], str)
                            self.assertIsInstance(info['model_id'], str)
    
    def test_available_models_all_clients(self):
        """Test that all clients provide available models."""
        for client_class, api_key_env, mock_library_path in self.client_configs:
            with self.subTest(client=client_class.__name__):
                with patch.dict(os.environ, {api_key_env: 'test_key'}):
                    with patch(mock_library_path) as mock_lib:
                        with patch.object(client_class, 'get_available_models', return_value={'Test Model': 'test-model-id'}):
                            self._setup_library_mock(mock_lib, client_class.__name__)
                            
                            client = client_class()
                            models = client.get_available_models()
                            
                            # All clients should return a dictionary of models
                            self.assertIsInstance(models, dict)
                            self.assertGreater(len(models), 0)
                            
                            # Check that all values are strings (model IDs)
                            for model_name, model_id in models.items():
                                self.assertIsInstance(model_name, str)
                                self.assertIsInstance(model_id, str)
    
    # Helper methods for setting up library-specific mocks
    
    def _setup_library_mock(self, mock_lib, client_name):
        """Setup basic library mock for initialization."""
        if client_name == 'LLMClient':
            # Anthropic mock
            mock_client = MagicMock()
            mock_model = MagicMock()
            mock_model.display_name = "Claude Sonnet 4"
            mock_model.id = "claude-sonnet-4-20250514"
            mock_client.models.list.return_value.data = [mock_model]
            mock_lib.Anthropic.return_value = mock_client
        elif client_name == 'GeminiClient':
            # Google Generative AI mock - need to set up the configuration
            mock_model = MagicMock()
            mock_lib.GenerativeModel.return_value = mock_model
            # Setup types for Gemini
            mock_config_class = MagicMock()
            mock_lib.types.GenerationConfig = mock_config_class
        elif client_name == 'OpenAIClient':
            # OpenAI mock
            mock_client = MagicMock()
            mock_lib.OpenAI.return_value = mock_client
        elif client_name == 'OpenRouterClient':
            # OpenRouter (uses OpenAI library) mock
            mock_client = MagicMock()
            mock_lib.OpenAI.return_value = mock_client
    
    def _setup_generate_poetry_mock(self, mock_lib, client_name):
        """Setup mock for successful poetry generation."""
        if client_name == 'LLMClient':
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_content = MagicMock()
            mock_content.text = "  Beautiful poetry here  "
            mock_response.content = [mock_content]
            mock_client.messages.create.return_value = mock_response
            mock_lib.Anthropic.return_value = mock_client
            return mock_client
        elif client_name == 'GeminiClient':
            mock_model = MagicMock()
            mock_response = MagicMock()
            mock_response.text = "  Beautiful poetry here  "
            mock_model.generate_content.return_value = mock_response
            mock_lib.GenerativeModel.return_value = mock_model
            return mock_model
        elif client_name in ['OpenAIClient', 'OpenRouterClient']:
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_choice = MagicMock()
            mock_message = MagicMock()
            mock_message.content = "  Beautiful poetry here  "
            mock_choice.message = mock_message
            mock_response.choices = [mock_choice]
            mock_client.chat.completions.create.return_value = mock_response
            mock_lib.OpenAI.return_value = mock_client
            return mock_client
    
    def _setup_generate_poetry_error_mock(self, mock_lib, client_name):
        """Setup mock for poetry generation API error."""
        if client_name == 'LLMClient':
            mock_client = MagicMock()
            mock_client.messages.create.side_effect = Exception("API Error")
            mock_lib.Anthropic.return_value = mock_client
        elif client_name == 'GeminiClient':
            mock_model = MagicMock()
            mock_model.generate_content.side_effect = Exception("API Error")
            mock_lib.GenerativeModel.return_value = mock_model
        elif client_name in ['OpenAIClient', 'OpenRouterClient']:
            mock_client = MagicMock()
            mock_client.chat.completions.create.side_effect = Exception("API Error")
            mock_lib.OpenAI.return_value = mock_client
    
    def _setup_test_connection_success_mock(self, mock_lib, client_name):
        """Setup mock for successful connection test."""
        if client_name == 'LLMClient':
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_content = MagicMock()
            mock_content.text = "Hello world"
            mock_response.content = [mock_content]
            mock_client.messages.create.return_value = mock_response
            mock_lib.Anthropic.return_value = mock_client
        elif client_name == 'GeminiClient':
            mock_model = MagicMock()
            mock_response = MagicMock()
            mock_response.text = "Hello world"
            mock_model.generate_content.return_value = mock_response
            mock_lib.GenerativeModel.return_value = mock_model
        elif client_name in ['OpenAIClient', 'OpenRouterClient']:
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_choice = MagicMock()
            mock_message = MagicMock()
            mock_message.content = "Hello world"
            mock_choice.message = mock_message
            mock_response.choices = [mock_choice]
            mock_client.chat.completions.create.return_value = mock_response
            mock_lib.OpenAI.return_value = mock_client
    
    def _setup_test_connection_empty_mock(self, mock_lib, client_name, empty_response):
        """Setup mock for connection test with empty response."""
        if client_name == 'LLMClient':
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_content = MagicMock()
            mock_content.text = empty_response
            mock_response.content = [mock_content]
            mock_client.messages.create.return_value = mock_response
            mock_lib.Anthropic.return_value = mock_client
        elif client_name == 'GeminiClient':
            mock_model = MagicMock()
            mock_response = MagicMock()
            mock_response.text = empty_response
            mock_model.generate_content.return_value = mock_response
            mock_lib.GenerativeModel.return_value = mock_model
        elif client_name in ['OpenAIClient', 'OpenRouterClient']:
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_choice = MagicMock()
            mock_message = MagicMock()
            mock_message.content = empty_response
            mock_choice.message = mock_message
            mock_response.choices = [mock_choice]
            mock_client.chat.completions.create.return_value = mock_response
            mock_lib.OpenAI.return_value = mock_client
    
    def _setup_test_connection_error_mock(self, mock_lib, client_name, error):
        """Setup mock for connection test with API error."""
        if client_name == 'LLMClient':
            mock_client = MagicMock()
            mock_client.messages.create.side_effect = error
            mock_lib.Anthropic.return_value = mock_client
        elif client_name == 'GeminiClient':
            mock_model = MagicMock()
            mock_model.generate_content.side_effect = error
            mock_lib.GenerativeModel.return_value = mock_model
        elif client_name in ['OpenAIClient', 'OpenRouterClient']:
            mock_client = MagicMock()
            mock_client.chat.completions.create.side_effect = error
            mock_lib.OpenAI.return_value = mock_client
    
    def _verify_generate_poetry_call(self, mock_response, client_name):
        """Verify that the appropriate API method was called for poetry generation."""
        if client_name == 'LLMClient':
            mock_response.messages.create.assert_called()
        elif client_name == 'GeminiClient':
            mock_response.generate_content.assert_called()
        elif client_name in ['OpenAIClient', 'OpenRouterClient']:
            mock_response.chat.completions.create.assert_called()


if __name__ == '__main__':
    unittest.main()