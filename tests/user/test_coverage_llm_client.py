"""
Comprehensive unit tests with coverage for llm_client.py
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class TestLLMClientImports(unittest.TestCase):
    """Test import scenarios for LLMClient."""
    
    def test_import_without_anthropic(self):
        """Test LLMClient behavior when anthropic library is not available."""
        with patch.dict('sys.modules', {'anthropic': None}):
            with patch('builtins.print') as mock_print:
                # Re-import the module with mocked anthropic
                if 'llm_client' in sys.modules:
                    del sys.modules['llm_client']
                
                import llm_client
                
                # Should print error message
                mock_print.assert_called_with("Anthropic library not found. Install with: pip install anthropic")
                
                # anthropic should be None
                self.assertIsNone(llm_client.anthropic)


class TestLLMClient(unittest.TestCase):
    """Test LLMClient functionality."""
    
    def setUp(self):
        """Set up test environment."""
        # Import after ensuring anthropic is available
        from llm_client import LLMClient
        self.LLMClient = LLMClient
    
    @patch.dict(os.environ, {}, clear=True)
    def test_init_without_api_key(self):
        """Test initialization without API key."""
        with self.assertRaises(ValueError) as context:
            self.LLMClient()
        
        self.assertIn("ANTHROPIC_API_KEY environment variable is required", str(context.exception))
    
    @patch('llm_client.anthropic', None)
    def test_init_without_anthropic_library(self):
        """Test initialization without anthropic library."""
        with self.assertRaises(ImportError) as context:
            self.LLMClient()
        
        self.assertEqual(str(context.exception), "Anthropic library is required")
    
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test_key'})
    @patch('llm_client.anthropic')
    def test_successful_initialization(self, mock_anthropic):
        """Test successful initialization."""
        mock_client = MagicMock()
        mock_anthropic.Anthropic.return_value = mock_client
        
        # Mock the models.list() call for dynamic discovery
        mock_model = MagicMock()
        mock_model.display_name = "Claude Sonnet 4"
        mock_model.id = "claude-sonnet-4-20250514"
        mock_model.created_at = "2025-05-22T00:00:00Z"
        mock_client.models.list.return_value.data = [mock_model]
        
        client = self.LLMClient()
        
        # Check that Anthropic was called with correct API key
        mock_anthropic.Anthropic.assert_called_once_with(api_key='test_key')
        self.assertEqual(client.client, mock_client)
        # Should use the first available model from dynamic discovery
        self.assertEqual(client.model, "claude-sonnet-4-20250514")
        self.assertEqual(client.model_name, "Claude Sonnet 4")
    
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test_key'})
    @patch('llm_client.anthropic')
    def test_generate_poetry_success(self, mock_anthropic):
        """Test successful poetry generation."""
        # Setup mock
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_content = MagicMock()
        mock_content.text = "  Beautiful poetry here  "
        mock_response.content = [mock_content]
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.Anthropic.return_value = mock_client
        
        client = self.LLMClient()
        result = client.generate_poetry("Write a haiku", max_tokens=100)
        
        # Check the call was made correctly
        mock_client.messages.create.assert_called_once_with(
            model="claude-3-5-sonnet-20241022",
            max_tokens=100,
            temperature=0.7,
            messages=[{
                "role": "user",
                "content": "Write a haiku"
            }]
        )
        
        # Check result is stripped
        self.assertEqual(result, "Beautiful poetry here")
    
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test_key'})
    @patch('llm_client.anthropic')
    def test_generate_poetry_with_default_max_tokens(self, mock_anthropic):
        """Test poetry generation with default max_tokens."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_content = MagicMock()
        mock_content.text = "Poetry"
        mock_response.content = [mock_content]
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.Anthropic.return_value = mock_client
        
        client = self.LLMClient()
        client.generate_poetry("Test prompt")
        
        # Should use default max_tokens=500
        call_args = mock_client.messages.create.call_args
        self.assertEqual(call_args[1]['max_tokens'], 500)
    
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test_key'})
    @patch('llm_client.anthropic')
    def test_generate_poetry_api_error(self, mock_anthropic):
        """Test poetry generation with API error."""
        mock_client = MagicMock()
        mock_client.messages.create.side_effect = Exception("API Error")
        mock_anthropic.Anthropic.return_value = mock_client
        
        client = self.LLMClient()
        
        with self.assertRaises(Exception) as context:
            client.generate_poetry("Test prompt")
        
        self.assertIn("Error generating poetry: API Error", str(context.exception))
    
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test_key'})
    @patch('llm_client.anthropic')
    def test_test_connection_success(self, mock_anthropic):
        """Test successful connection test."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_content = MagicMock()
        mock_content.text = "Hello world"
        mock_response.content = [mock_content]
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.Anthropic.return_value = mock_client
        
        client = self.LLMClient()
        result = client.test_connection()
        
        self.assertTrue(result)
        
        # Check it called generate_poetry with test prompt
        mock_client.messages.create.assert_called_once()
        call_args = mock_client.messages.create.call_args
        self.assertEqual(call_args[1]['max_tokens'], 10)
        self.assertIn("Write a simple two-word poem.", call_args[1]['messages'][0]['content'])
    
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test_key'})
    @patch('llm_client.anthropic')
    def test_test_connection_empty_response(self, mock_anthropic):
        """Test connection test with empty response."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_content = MagicMock()
        mock_content.text = "   "  # Empty/whitespace only
        mock_response.content = [mock_content]
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.Anthropic.return_value = mock_client
        
        client = self.LLMClient()
        result = client.test_connection()
        
        self.assertFalse(result)
    
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test_key'})
    @patch('llm_client.anthropic')
    def test_test_connection_api_error(self, mock_anthropic):
        """Test connection test with API error."""
        mock_client = MagicMock()
        mock_client.messages.create.side_effect = Exception("Connection failed")
        mock_anthropic.Anthropic.return_value = mock_client
        
        client = self.LLMClient()
        result = client.test_connection()
        
        self.assertFalse(result)
    
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test_key'})
    @patch('llm_client.anthropic')
    def test_multiple_content_items(self, mock_anthropic):
        """Test handling response with multiple content items."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        
        # Multiple content items - should use first one
        mock_content1 = MagicMock()
        mock_content1.text = "First content"
        mock_content2 = MagicMock()
        mock_content2.text = "Second content"
        mock_response.content = [mock_content1, mock_content2]
        
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.Anthropic.return_value = mock_client
        
        client = self.LLMClient()
        result = client.generate_poetry("Test")
        
        self.assertEqual(result, "First content")


if __name__ == '__main__':
    unittest.main()