#!/usr/bin/env python3
"""
Test script for BaseLLMClient abstract base class
"""

import sys
import os
# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

import unittest
from unittest.mock import Mock, patch
from base_llm_client import BaseLLMClient
from exceptions import APIError, ConfigurationError

class MockLLMClient(BaseLLMClient):
    """Mock implementation for testing BaseLLMClient"""
    
    def get_available_models(self, limit_recent=6):
        return {
            "Model A": "model-a-123",
            "Model B": "model-b-456", 
            "Model C": "model-c-789"
        }
    
    def _initialize_client(self):
        self.mock_client = Mock()
    
    def generate_poetry(self, prompt, max_tokens=500):
        return "Test poem\nGenerated successfully"

class TestBaseLLMClient(unittest.TestCase):
    """Test cases for BaseLLMClient"""
    
    @patch.dict(os.environ, {'TEST_API_KEY': 'test-key-123'})
    def test_initialization_with_valid_api_key(self):
        """Test successful initialization with valid API key"""
        client = MockLLMClient(api_key_env='TEST_API_KEY')
        self.assertEqual(client.api_key, 'test-key-123')
        self.assertEqual(client.model_name, 'Model A')  # Should use first available
        self.assertEqual(client.model, 'model-a-123')
    
    @patch.dict(os.environ, {'TEST_API_KEY': 'test-key-123'})
    def test_initialization_with_specific_model(self):
        """Test initialization with specific model selection"""
        client = MockLLMClient(model='Model B', api_key_env='TEST_API_KEY')
        self.assertEqual(client.model_name, 'Model B')
        self.assertEqual(client.model, 'model-b-456')
    
    def test_initialization_without_api_key(self):
        """Test initialization fails without API key"""
        with self.assertRaises(ValueError) as context:
            MockLLMClient(api_key_env='NONEXISTENT_KEY')
        self.assertIn('environment variable is required', str(context.exception))
    
    @patch.dict(os.environ, {'TEST_API_KEY': 'test-key-123'})
    def test_invalid_model_selection(self):
        """Test initialization fails with invalid model"""
        with self.assertRaises(ValueError) as context:
            MockLLMClient(model='Nonexistent Model', api_key_env='TEST_API_KEY')
        self.assertIn('not available', str(context.exception))
    
    @patch.dict(os.environ, {'TEST_API_KEY': 'test-key-123'})
    def test_get_model_info(self):
        """Test model information retrieval"""
        client = MockLLMClient(model='Model C', api_key_env='TEST_API_KEY')
        info = client.get_model_info()
        
        expected_info = {
            'provider': 'MockLLM',
            'model_name': 'Model C',
            'model_id': 'model-c-789'
        }
        self.assertEqual(info, expected_info)
    
    @patch.dict(os.environ, {'TEST_API_KEY': 'test-key-123'})
    def test_test_connection_success(self):
        """Test successful connection test"""
        client = MockLLMClient(api_key_env='TEST_API_KEY')
        self.assertTrue(client.test_connection())
    
    @patch.dict(os.environ, {'TEST_API_KEY': 'test-key-123'})
    def test_test_connection_failure(self):
        """Test connection test failure"""
        client = MockLLMClient(api_key_env='TEST_API_KEY')
        
        # Mock generate_poetry to raise exception
        with patch.object(client, 'generate_poetry', side_effect=Exception("API Error")):
            self.assertFalse(client.test_connection())

def run_tests():
    """Run all tests and return results"""
    print("Testing BaseLLMClient...")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestBaseLLMClient)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ All BaseLLMClient tests passed!")
        return True
    else:
        print(f"❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        return False

if __name__ == "__main__":
    run_tests()