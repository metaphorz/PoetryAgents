"""
Coverage tests for enhancement_service.py - ASCII art and emoji enhancement
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from enhancement_service import EnhancementService

class TestEnhancementService(unittest.TestCase):
    """Comprehensive coverage tests for EnhancementService"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_client = MagicMock()
        self.service = EnhancementService(client=self.mock_client)
    
    def test_initialization_with_provided_client(self):
        """Test initialization with provided LLM client"""
        mock_client = MagicMock()
        service = EnhancementService(client=mock_client)
        
        self.assertEqual(service.client, mock_client)
    
    @patch('enhancement_service.LLMClient')
    def test_initialization_with_default_client(self, mock_llm_client):
        """Test initialization creates default LLMClient when none provided"""
        mock_default_client = MagicMock()
        mock_llm_client.return_value = mock_default_client
        
        service = EnhancementService()
        
        mock_llm_client.assert_called_once()
        self.assertEqual(service.client, mock_default_client)
    
    def test_generate_ascii_art_success(self):
        """Test successful ASCII art generation"""
        expected_art = "  *\n / \\\n*-*-*"
        self.mock_client.generate_poetry.return_value = expected_art
        
        result = self.service.generate_ascii_art("winter forest")
        
        self.assertEqual(result, "*\n / \\\n*-*-*")  # Should be stripped
        self.mock_client.generate_poetry.assert_called_once()
        
        # Verify prompt contains theme and ASCII instructions
        call_args = self.mock_client.generate_poetry.call_args
        prompt = call_args[0][0]
        max_tokens = call_args[1]['max_tokens']
        
        self.assertIn('winter forest', prompt)
        self.assertIn('ASCII art', prompt)
        self.assertIn('text art', prompt)
        self.assertIn('4-8 lines maximum', prompt)
        self.assertEqual(max_tokens, 250)
    
    def test_generate_ascii_art_with_guidelines(self):
        """Test that ASCII art prompt includes proper guidelines"""
        self.mock_client.generate_poetry.return_value = "test art"
        
        self.service.generate_ascii_art("ocean waves")
        
        call_args = self.mock_client.generate_poetry.call_args
        prompt = call_args[0][0]
        
        # Check for specific guidelines
        self.assertIn('basic ASCII characters', prompt)
        self.assertIn('visually appealing', prompt)
        self.assertIn('thematically appropriate', prompt)
        self.assertIn('complement poetry', prompt)
        
        # Check for examples
        self.assertIn('Snow/winter', prompt)
        self.assertIn('Ocean/water', prompt)
        self.assertIn('Night/stars', prompt)
        
        # Check for instruction to return only art
        self.assertIn('ONLY the ASCII art', prompt)
        self.assertIn('no explanatory text', prompt)
    
    def test_generate_ascii_art_api_error_fallback(self):
        """Test ASCII art generation falls back on API error"""
        self.mock_client.generate_poetry.side_effect = Exception("API Error")
        
        result = self.service.generate_ascii_art("mountain peak")
        
        # Should return fallback ASCII art
        self.assertEqual(result, "~*~*~*~\n Poetry \n~*~*~*~")
    
    def test_generate_ascii_art_empty_response_fallback(self):
        """Test ASCII art generation falls back on empty response"""
        self.mock_client.generate_poetry.return_value = ""
        
        result = self.service.generate_ascii_art("desert sunset")
        
        # Should return fallback ASCII art since empty is stripped to ""
        self.assertEqual(result, "~*~*~*~\n Poetry \n~*~*~*~")
    
    def test_add_emojis_to_poetry_success(self):
        """Test successful emoji enhancement"""
        original_poetry = "Snow falls gently\nOn quiet forest paths\nWinter's peaceful embrace"
        enhanced_poetry = "Snow❄️ falls gently\nOn quiet forest🌲 paths\nWinter's peaceful embrace🤗"
        
        self.mock_client.generate_poetry.return_value = enhanced_poetry
        
        result = self.service.add_emojis_to_poetry(original_poetry, "winter nature")
        
        self.assertEqual(result, enhanced_poetry)
        self.mock_client.generate_poetry.assert_called_once()
        
        # Verify prompt contains original poetry and theme
        call_args = self.mock_client.generate_poetry.call_args
        prompt = call_args[0][0]
        max_tokens = call_args[1]['max_tokens']
        
        self.assertIn('winter nature', prompt)
        self.assertIn(original_poetry, prompt)
        self.assertIn('emojis', prompt)
        self.assertEqual(max_tokens, 400)
    
    def test_add_emojis_to_poetry_with_instructions(self):
        """Test that emoji enhancement prompt includes proper instructions"""
        original = "Roses are red\nViolets are blue"
        self.mock_client.generate_poetry.return_value = "Enhanced poetry"
        
        self.service.add_emojis_to_poetry(original, "flowers")
        
        call_args = self.mock_client.generate_poetry.call_args
        prompt = call_args[0][0]
        
        # Check for specific instructions
        self.assertIn('immediately AFTER words', prompt)
        self.assertIn('word🌟 not 🌟word', prompt)
        self.assertIn('nouns, nature words, emotions', prompt)
        self.assertIn("don't add emojis to articles", prompt)
        self.assertIn('2-4 emojis per line maximum', prompt)
        self.assertIn('exact line structure', prompt)
        
        # Check for formatting requirements
        self.assertIn('ONLY the enhanced poetry', prompt)
        self.assertIn('no explanatory text', prompt)
        self.assertIn('same line breaks', prompt)
    
    def test_add_emojis_to_poetry_preserves_structure_instruction(self):
        """Test that emoji prompt emphasizes preserving original structure"""
        original = "Line 1\n\nLine 3 with gap"
        self.mock_client.generate_poetry.return_value = "Enhanced"
        
        self.service.add_emojis_to_poetry(original, "test")
        
        call_args = self.mock_client.generate_poetry.call_args
        prompt = call_args[0][0]
        
        self.assertIn(original, prompt)
        self.assertIn('Preserve the exact line structure', prompt)
        self.assertIn('maintaining the same line breaks', prompt)
    
    def test_add_emojis_to_poetry_api_error_fallback(self):
        """Test emoji enhancement falls back to original on API error"""
        original_poetry = "Original verse\nShould be unchanged"
        
        self.mock_client.generate_poetry.side_effect = Exception("API Error")
        
        result = self.service.add_emojis_to_poetry(original_poetry, "theme")
        
        # Should return original poetry unchanged
        self.assertEqual(result, original_poetry)
    
    def test_add_emojis_to_poetry_empty_response_fallback(self):
        """Test emoji enhancement falls back to original on empty response"""
        original_poetry = "Original verse\nShould be unchanged"
        
        self.mock_client.generate_poetry.return_value = ""
        
        result = self.service.add_emojis_to_poetry(original_poetry, "theme")
        
        # Should return original poetry since empty string is stripped
        self.assertEqual(result, original_poetry)
    
    def test_add_emojis_to_poetry_whitespace_only_response_fallback(self):
        """Test emoji enhancement falls back to original on whitespace-only response"""
        original_poetry = "Original verse\nShould be unchanged"
        
        self.mock_client.generate_poetry.return_value = "   \n\t  "
        
        result = self.service.add_emojis_to_poetry(original_poetry, "theme")
        
        # Should return original poetry since whitespace is stripped to empty
        self.assertEqual(result, original_poetry)
    
    def test_both_methods_with_different_themes(self):
        """Test both methods work correctly with various themes"""
        themes = ["ocean storm", "mountain climbing", "city nightlife", "garden flowers"]
        
        for theme in themes:
            with self.subTest(theme=theme):
                # Reset mock for each test
                self.mock_client.reset_mock()
                
                # ASCII art
                self.mock_client.generate_poetry.return_value = f"ASCII for {theme}"
                ascii_result = self.service.generate_ascii_art(theme)
                self.assertEqual(ascii_result, f"ASCII for {theme}")
                
                # Emoji enhancement  
                self.mock_client.generate_poetry.return_value = f"Enhanced poetry about {theme}"
                emoji_result = self.service.add_emojis_to_poetry("Original poetry", theme)
                self.assertEqual(emoji_result, f"Enhanced poetry about {theme}")
                
                # Verify both methods were called
                self.assertEqual(self.mock_client.generate_poetry.call_count, 2)

if __name__ == '__main__':
    unittest.main()