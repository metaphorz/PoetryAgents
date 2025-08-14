"""
Coverage tests for base_llm_client.py - the new abstract base class
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from base_llm_client import BaseLLMClient
from exceptions import APIError

class MockLLMClient(BaseLLMClient):
    """Mock implementation for testing BaseLLMClient"""
    
    def get_available_models(self, limit_recent=6):
        return {
            "Test Model 1": "test-model-1", 
            "Test Model 2": "test-model-2"
        }
    
    def _initialize_client(self):
        self.client = MagicMock()
    
    def generate_poetry(self, prompt, max_tokens=500):
        return "Test poetry response"

class TestBaseLLMClient(unittest.TestCase):
    """Comprehensive coverage tests for BaseLLMClient"""
    
    def test_abstract_methods_requirement(self):
        """Test that BaseLLMClient cannot be instantiated directly"""
        with self.assertRaises(TypeError):
            BaseLLMClient()
    
    @patch.dict(os.environ, {'TEST_API_KEY': 'test-key-123'})
    def test_successful_initialization(self):
        """Test successful initialization with all parameters"""
        client = MockLLMClient(model='Test Model 2', api_key_env='TEST_API_KEY')
        
        self.assertEqual(client.api_key, 'test-key-123')
        self.assertEqual(client.model_name, 'Test Model 2')
        self.assertEqual(client.model, 'test-model-2')
        self.assertIsNotNone(client.client)
    
    @patch.dict(os.environ, {'TEST_API_KEY': 'test-key-123'})
    def test_default_model_selection(self):
        """Test that first available model is used when none specified"""
        client = MockLLMClient(api_key_env='TEST_API_KEY')
        
        self.assertEqual(client.model_name, 'Test Model 1')  # First in list
        self.assertEqual(client.model, 'test-model-1')
    
    def test_missing_api_key_env_var_name(self):
        """Test initialization fails when API key env var name not provided"""
        with self.assertRaises(ValueError) as context:
            MockLLMClient()
        
        self.assertIn('API key environment variable name not specified', str(context.exception))
    
    def test_missing_api_key_value(self):
        """Test initialization fails when API key env var doesn't exist"""
        with self.assertRaises(ValueError) as context:
            MockLLMClient(api_key_env='NONEXISTENT_KEY')
        
        self.assertIn('environment variable is required', str(context.exception))
    
    @patch.dict(os.environ, {'TEST_API_KEY': 'test-key-123'})
    def test_invalid_model_selection(self):
        """Test initialization fails with invalid model name"""
        with self.assertRaises(ValueError) as context:
            MockLLMClient(model='Nonexistent Model', api_key_env='TEST_API_KEY')
        
        self.assertIn('not available', str(context.exception))
    
    @patch.dict(os.environ, {'TEST_API_KEY': 'test-key-123'})
    def test_get_model_info(self):
        """Test model information retrieval"""
        client = MockLLMClient(model='Test Model 2', api_key_env='TEST_API_KEY')
        info = client.get_model_info()
        
        expected = {
            'provider': 'MockLLM',
            'model_name': 'Test Model 2',
            'model_id': 'test-model-2'
        }
        self.assertEqual(info, expected)
    
    @patch.dict(os.environ, {'TEST_API_KEY': 'test-key-123'})
    def test_test_connection_success(self):
        """Test successful connection test"""
        client = MockLLMClient(api_key_env='TEST_API_KEY')
        result = client.test_connection()
        
        self.assertTrue(result)
    
    @patch.dict(os.environ, {'TEST_API_KEY': 'test-key-123'})
    def test_test_connection_failure(self):
        """Test connection test failure when generate_poetry raises exception"""
        client = MockLLMClient(api_key_env='TEST_API_KEY')
        
        # Mock generate_poetry to raise exception
        with patch.object(client, 'generate_poetry', side_effect=Exception("API Error")):
            result = client.test_connection()
        
        self.assertFalse(result)
    
    @patch.dict(os.environ, {'TEST_API_KEY': 'test-key-123'})
    def test_test_connection_empty_response(self):
        """Test connection test failure when generate_poetry returns empty string"""
        client = MockLLMClient(api_key_env='TEST_API_KEY')
        
        # Mock generate_poetry to return empty string
        with patch.object(client, 'generate_poetry', return_value=''):
            result = client.test_connection()
        
        self.assertFalse(result)
    
    @patch.dict(os.environ, {'TEST_API_KEY': 'test-key-123'})
    def test_test_connection_whitespace_only_response(self):
        """Test connection test failure when generate_poetry returns only whitespace"""
        client = MockLLMClient(api_key_env='TEST_API_KEY')
        
        # Mock generate_poetry to return whitespace
        with patch.object(client, 'generate_poetry', return_value='   \n\t  '):
            result = client.test_connection()
        
        self.assertFalse(result)
    
    @patch.dict(os.environ, {'TEST_API_KEY': 'test-key-123'})
    def test_abstract_method_implementation_required(self):
        """Test that abstract methods must be implemented by subclasses"""
        
        # Test get_available_models
        class IncompleteClient1(BaseLLMClient):
            def _initialize_client(self):
                pass
            def generate_poetry(self, prompt, max_tokens=500):
                return "test"
            # Missing get_available_models
        
        with self.assertRaises(TypeError):
            IncompleteClient1(api_key_env='TEST_API_KEY')
        
        # Test _initialize_client
        class IncompleteClient2(BaseLLMClient):
            def get_available_models(self, limit_recent=6):
                return {"Test": "test"}
            def generate_poetry(self, prompt, max_tokens=500):
                return "test"
            # Missing _initialize_client
        
        with self.assertRaises(TypeError):
            IncompleteClient2(api_key_env='TEST_API_KEY')
        
        # Test generate_poetry
        class IncompleteClient3(BaseLLMClient):
            def get_available_models(self, limit_recent=6):
                return {"Test": "test"}
            def _initialize_client(self):
                pass
            # Missing generate_poetry
        
        with self.assertRaises(TypeError):
            IncompleteClient3(api_key_env='TEST_API_KEY')

if __name__ == '__main__':
    unittest.main()