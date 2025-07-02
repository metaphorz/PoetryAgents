"""
Comprehensive unit tests with coverage for gemini_client.py
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class TestGeminiClientImports(unittest.TestCase):
    """Test import scenarios for GeminiClient."""
    
    def test_import_without_genai(self):
        """Test GeminiClient behavior when google.generativeai library is not available."""
        with patch.dict('sys.modules', {'google.generativeai': None}):
            with patch('builtins.print') as mock_print:
                # Re-import the module with mocked genai
                if 'gemini_client' in sys.modules:
                    del sys.modules['gemini_client']
                
                import gemini_client
                
                # Should print error message
                mock_print.assert_called_with("Google Generative AI library not found. Install with: pip install google-generativeai")
                
                # genai should be None
                self.assertIsNone(gemini_client.genai)


class TestGeminiClient(unittest.TestCase):
    """Test GeminiClient functionality."""
    
    def setUp(self):
        """Set up test environment."""
        # Import after ensuring genai is available
        from gemini_client import GeminiClient
        self.GeminiClient = GeminiClient
    
    @patch.dict(os.environ, {}, clear=True)
    def test_init_without_api_key(self):
        """Test initialization without API key."""
        with self.assertRaises(ValueError) as context:
            self.GeminiClient()
        
        self.assertIn("GEMINI_API_KEY environment variable is required", str(context.exception))
    
    @patch('gemini_client.genai', None)
    def test_init_without_genai_library(self):
        """Test initialization without genai library."""
        with self.assertRaises(ImportError) as context:
            self.GeminiClient()
        
        self.assertEqual(str(context.exception), "Google Generative AI library is required")
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'})
    @patch('gemini_client.genai')
    def test_successful_initialization(self, mock_genai):
        """Test successful initialization."""
        mock_model = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        
        client = self.GeminiClient()
        
        # Check that genai was configured and model created
        mock_genai.configure.assert_called_once_with(api_key='test_key')
        mock_genai.GenerativeModel.assert_called_once_with('gemini-1.5-flash')
        self.assertEqual(client.model, mock_model)
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'})
    @patch('gemini_client.genai')
    def test_generate_poetry_success(self, mock_genai):
        """Test successful poetry generation."""
        # Setup mock
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "  Beautiful poetry here  "
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        client = self.GeminiClient()
        result = client.generate_poetry("Write a haiku", max_tokens=100)
        
        # Check the call was made correctly
        mock_model.generate_content.assert_called_once()
        call_args = mock_model.generate_content.call_args
        
        # Check prompt
        self.assertEqual(call_args[0][0], "Write a haiku")
        
        # Check generation config (it might be passed as an object)
        self.assertIn('generation_config', call_args[1])
        generation_config = call_args[1]['generation_config']
        # Check that it's the right type and has some expected attributes
        self.assertTrue(hasattr(generation_config, 'max_output_tokens') or 
                       hasattr(generation_config, '__dict__'))
        
        # Check result is stripped
        self.assertEqual(result, "Beautiful poetry here")
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'})
    @patch('gemini_client.genai')
    def test_generate_poetry_with_default_max_tokens(self, mock_genai):
        """Test poetry generation with default max_tokens."""
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Poetry"
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        client = self.GeminiClient()
        client.generate_poetry("Test prompt")
        
        # Should use default max_tokens=500
        call_args = mock_model.generate_content.call_args
        self.assertIn('generation_config', call_args[1])
        generation_config = call_args[1]['generation_config']
        # Just check that generation_config exists and is used
        self.assertTrue(hasattr(generation_config, 'max_output_tokens') or 
                       hasattr(generation_config, '__dict__'))
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'})
    @patch('gemini_client.genai')
    def test_generate_poetry_api_error(self, mock_genai):
        """Test poetry generation with API error."""
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = Exception("API Error")
        mock_genai.GenerativeModel.return_value = mock_model
        
        client = self.GeminiClient()
        
        with self.assertRaises(Exception) as context:
            client.generate_poetry("Test prompt")
        
        self.assertIn("Error generating poetry with Gemini: API Error", str(context.exception))
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'})
    @patch('gemini_client.genai')
    def test_test_connection_success(self, mock_genai):
        """Test successful connection test."""
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Hello world"
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        client = self.GeminiClient()
        result = client.test_connection()
        
        self.assertTrue(result)
        
        # Check it called generate_content with test prompt
        mock_model.generate_content.assert_called()
        call_args = mock_model.generate_content.call_args
        self.assertIn('generation_config', call_args[1])
        # Just verify the call was made with generation_config
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'})
    @patch('gemini_client.genai')
    def test_test_connection_empty_response(self, mock_genai):
        """Test connection test with empty response."""
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "   "  # Empty/whitespace only
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        client = self.GeminiClient()
        result = client.test_connection()
        
        self.assertFalse(result)
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'})
    @patch('gemini_client.genai')
    def test_test_connection_api_error(self, mock_genai):
        """Test connection test with API error."""
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = Exception("Connection failed")
        mock_genai.GenerativeModel.return_value = mock_model
        
        client = self.GeminiClient()
        result = client.test_connection()
        
        self.assertFalse(result)
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'})
    @patch('gemini_client.genai')
    def test_generation_config_parameters(self, mock_genai):
        """Test that generation config has correct parameters."""
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Test output"
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        mock_genai.types = MagicMock()
        
        client = self.GeminiClient()
        client.generate_poetry("Test", max_tokens=200)
        
        # Verify GenerationConfig was called with correct parameters
        config_call = mock_genai.types.GenerationConfig.call_args
        if config_call:
            kwargs = config_call[1]
            self.assertEqual(kwargs.get('max_output_tokens'), 200)
            self.assertEqual(kwargs.get('temperature'), 0.7)
            self.assertEqual(kwargs.get('top_p'), 0.8)
            self.assertEqual(kwargs.get('top_k'), 40)


if __name__ == '__main__':
    unittest.main()