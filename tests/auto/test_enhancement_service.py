#!/usr/bin/env python3
"""
Test script for EnhancementService
"""

import sys
import os
# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

import unittest
from unittest.mock import Mock, patch
from enhancement_service import EnhancementService

class TestEnhancementService(unittest.TestCase):
    """Test cases for EnhancementService"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_client = Mock()
        self.service = EnhancementService(client=self.mock_client)
    
    def test_generate_ascii_art_success(self):
        """Test successful ASCII art generation"""
        self.mock_client.generate_poetry.return_value = "  *\n / \\\n *-*"
        
        result = self.service.generate_ascii_art("winter")
        
        self.assertEqual(result, "*\n / \\\n *-*")
        self.mock_client.generate_poetry.assert_called_once()
        
        # Check that the prompt contains the theme
        call_args = self.mock_client.generate_poetry.call_args
        prompt = call_args[0][0]
        self.assertIn("winter", prompt)
        self.assertIn("ASCII art", prompt)
    
    def test_generate_ascii_art_failure_fallback(self):
        """Test ASCII art generation falls back on error"""
        self.mock_client.generate_poetry.side_effect = Exception("API Error")
        
        result = self.service.generate_ascii_art("winter")
        
        # Should return fallback ASCII art
        self.assertEqual(result, "~*~*~*~\n Poetry \n~*~*~*~")
    
    def test_add_emojis_to_poetry_success(self):
        """Test successful emoji enhancement"""
        original_poetry = "Snow falls gently\nOn quiet paths\nWinter's embrace"
        enhanced_poetry = "Snow❄️ falls gently\nOn quiet paths🌨️\nWinter's embrace🤗"
        
        self.mock_client.generate_poetry.return_value = enhanced_poetry
        
        result = self.service.add_emojis_to_poetry(original_poetry, "winter")
        
        self.assertEqual(result, enhanced_poetry)
        self.mock_client.generate_poetry.assert_called_once()
        
        # Check that the prompt contains both poetry and theme
        call_args = self.mock_client.generate_poetry.call_args
        prompt = call_args[0][0]
        self.assertIn("winter", prompt)
        self.assertIn(original_poetry, prompt)
        self.assertIn("emojis", prompt)
    
    def test_add_emojis_to_poetry_failure_fallback(self):
        """Test emoji enhancement falls back to original on error"""
        original_poetry = "Snow falls gently\nOn quiet paths\nWinter's embrace"
        
        self.mock_client.generate_poetry.side_effect = Exception("API Error")
        
        result = self.service.add_emojis_to_poetry(original_poetry, "winter")
        
        # Should return original poetry unchanged
        self.assertEqual(result, original_poetry)
    
    def test_initialization_with_default_client(self):
        """Test initialization with default client when none provided"""
        with patch('enhancement_service.LLMClient') as mock_llm_client:
            mock_default_client = Mock()
            mock_llm_client.return_value = mock_default_client
            
            service = EnhancementService()
            
            mock_llm_client.assert_called_once()
            self.assertEqual(service.client, mock_default_client)
    
    def test_initialization_with_provided_client(self):
        """Test initialization with provided client"""
        provided_client = Mock()
        service = EnhancementService(client=provided_client)
        
        self.assertEqual(service.client, provided_client)

def run_tests():
    """Run all tests and return results"""
    print("Testing EnhancementService...")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestEnhancementService)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ All EnhancementService tests passed!")
        return True
    else:
        print(f"❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        return False

if __name__ == "__main__":
    run_tests()