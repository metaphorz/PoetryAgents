"""
Comprehensive unit tests with coverage for prompts.py
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from prompts import (
    create_initial_poetry_prompt,
    create_response_poetry_prompt,
    create_title_prompt
)


class TestPrompts(unittest.TestCase):
    """Test prompt generation functions."""
    
    def test_create_initial_poetry_prompt_haiku(self):
        """Test creating initial prompt for haiku."""
        prompt = create_initial_poetry_prompt("spring flowers", "haiku", 3, "Elizabeth")
        
        self.assertIsInstance(prompt, str)
        self.assertIn("spring flowers", prompt)
        self.assertIn("haiku", prompt)
        self.assertIn("Elizabeth", prompt)
        self.assertIn("5-7-5", prompt)
        self.assertIn("3 lines", prompt)
        
        # Should not contain response-specific instructions
        self.assertNotIn("responds to", prompt)
        self.assertNotIn("previous poetry", prompt)
    
    def test_create_initial_poetry_prompt_prose(self):
        """Test creating initial prompt for prose."""
        prompt = create_initial_poetry_prompt("city life", "prose", 5, "Gatsby")
        
        self.assertIn("city life", prompt)
        self.assertIn("prose", prompt)
        self.assertIn("Gatsby", prompt)
        self.assertIn("free verse", prompt)
        self.assertIn("5 lines", prompt)
        
        # Should include prose-specific instructions
        self.assertIn("expressive language", prompt)
        self.assertIn("natural rhythm", prompt)
    
    def test_create_initial_poetry_prompt_sonnet(self):
        """Test creating initial prompt for sonnet."""
        prompt = create_initial_poetry_prompt("love", "sonnet", 14, "Shakespeare")
        
        self.assertIn("love", prompt)
        self.assertIn("sonnet", prompt)
        self.assertIn("Shakespeare", prompt)
        self.assertIn("14 lines", prompt)
        self.assertIn("ABAB CDCD EFEF GG", prompt)
        self.assertIn("iambic pentameter", prompt)
    
    def test_create_initial_poetry_prompt_villanelle(self):
        """Test creating initial prompt for villanelle."""
        prompt = create_initial_poetry_prompt("time", "villanelle", 19, "Dylan")
        
        self.assertIn("time", prompt)
        self.assertIn("villanelle", prompt)
        self.assertIn("Dylan", prompt)
        self.assertIn("19 lines", prompt)
        self.assertIn("A1bA2", prompt)
        self.assertIn("refrain", prompt)
    
    def test_create_initial_poetry_prompt_limerick(self):
        """Test creating initial prompt for limerick."""
        prompt = create_initial_poetry_prompt("funny cat", "limerick", 5, "Edward")
        
        self.assertIn("funny cat", prompt)
        self.assertIn("limerick", prompt)
        self.assertIn("Edward", prompt)
        self.assertIn("5 lines", prompt)
        self.assertIn("AABBA", prompt)
        self.assertIn("humorous", prompt)
    
    def test_create_initial_poetry_prompt_ballad(self):
        """Test creating initial prompt for ballad."""
        prompt = create_initial_poetry_prompt("hero's journey", "ballad", 4, "Bard")
        
        self.assertIn("hero's journey", prompt)
        self.assertIn("ballad", prompt)
        self.assertIn("Bard", prompt)
        self.assertIn("4 stanzas", prompt)
        self.assertIn("ABAB", prompt)
        self.assertIn("narrative", prompt)
    
    def test_create_initial_poetry_prompt_ghazal(self):
        """Test creating initial prompt for ghazal."""
        prompt = create_initial_poetry_prompt("desert wind", "ghazal", 7, "Hafez")
        
        self.assertIn("desert wind", prompt)
        self.assertIn("ghazal", prompt)
        self.assertIn("Hafez", prompt)
        self.assertIn("7 couplets", prompt)
        self.assertIn("radif", prompt)
        self.assertIn("qafiya", prompt)
    
    def test_create_initial_poetry_prompt_tanka(self):
        """Test creating initial prompt for tanka."""
        prompt = create_initial_poetry_prompt("mountain", "tanka", 5, "Basho")
        
        self.assertIn("mountain", prompt)
        self.assertIn("tanka", prompt)
        self.assertIn("Basho", prompt)
        self.assertIn("5 lines", prompt)
        self.assertIn("5-7-5-7-7", prompt)
        self.assertIn("5-7-5-7-7", prompt)
    
    def test_create_initial_poetry_prompt_unknown_form(self):
        """Test creating initial prompt for unknown form."""
        prompt = create_initial_poetry_prompt("mystery", "unknown_form", 3, "Poet")
        
        self.assertIn("mystery", prompt)
        self.assertIn("unknown_form", prompt)
        self.assertIn("Poet", prompt)
        # For unknown forms, just check the basic structure
        
        # Should have fallback instructions - just check it's a valid prompt
        self.assertGreater(len(prompt), 20)
    
    def test_create_response_poetry_prompt_haiku(self):
        """Test creating response prompt for haiku."""
        previous_poetry = "Cherry blossoms fall\nSoftly on the morning ground\nSpring whispers goodbye"
        prompt = create_response_poetry_prompt("Basho", previous_poetry, "haiku", 3)
        
        self.assertIsInstance(prompt, str)
        self.assertIn("Basho", prompt)
        self.assertIn("haiku", prompt)
        self.assertIn("Cherry blossoms fall", prompt)
        self.assertIn("5-7-5", prompt)
        self.assertIn("Respond to", prompt)
        
        # Should have response-specific instructions
        self.assertIn("Incorporate elements", prompt)
        self.assertIn("previous poetry", prompt)
    
    def test_create_response_poetry_prompt_prose(self):
        """Test creating response prompt for prose."""
        previous_poetry = "The city sleeps beneath neon dreams"
        prompt = create_response_poetry_prompt("Ginsberg", previous_poetry, "prose", 4)
        
        self.assertIn("Ginsberg", prompt)
        self.assertIn("prose", prompt)
        self.assertIn("city sleeps", prompt)
        self.assertIn("4-line", prompt)
        self.assertIn("free verse", prompt)
    
    def test_create_response_poetry_prompt_sonnet(self):
        """Test creating response prompt for sonnet."""
        previous_poetry = "Shall I compare thee to a summer's day?"
        prompt = create_response_poetry_prompt("Elizabeth", previous_poetry, "sonnet", 14)
        
        self.assertIn("Elizabeth", prompt)
        self.assertIn("sonnet", prompt)
        self.assertIn("summer's day", prompt)
        self.assertIn("14 lines", prompt)
        self.assertIn("ABAB CDCD EFEF GG", prompt)
    
    def test_create_response_poetry_prompt_all_forms(self):
        """Test response prompts for all supported forms."""
        previous_poetry = "Sample previous poetry"
        forms = ["haiku", "prose", "sonnet", "villanelle", "limerick", "ballad", "ghazal", "tanka"]
        
        for form in forms:
            with self.subTest(form=form):
                prompt = create_response_poetry_prompt("Poet", previous_poetry, form, 5)
                self.assertIn("Poet", prompt)
                self.assertIn(form, prompt)
                self.assertIn("Sample previous poetry", prompt)
                self.assertGreater(len(prompt), 100)  # Should be substantial
    
    def test_create_title_prompt(self):
        """Test creating title prompt."""
        prompt = create_title_prompt("autumn leaves")
        
        self.assertIsInstance(prompt, str)
        self.assertIn("autumn leaves", prompt)
        self.assertIn("title", prompt)
        self.assertGreater(len(prompt), 20)
        
        # Should include title-specific instructions
        self.assertIn("title", prompt.lower())
        self.assertIn("theme", prompt.lower())
    
    def test_create_title_prompt_various_themes(self):
        """Test title prompts for various themes."""
        themes = [
            "winter morning",
            "love lost",
            "city at night",
            "childhood memories",
            "ocean waves",
            "mountain peak"
        ]
        
        for theme in themes:
            with self.subTest(theme=theme):
                prompt = create_title_prompt(theme)
                self.assertIn(theme, prompt)
                self.assertGreater(len(prompt), 15)
    
    def test_prompt_structure_consistency(self):
        """Test that all prompts have consistent structure."""
        # Test initial prompts
        for form in ["haiku", "prose", "sonnet", "villanelle", "limerick", "ballad", "ghazal", "tanka"]:
            prompt = create_initial_poetry_prompt("test theme", form, 5, "TestPoet")
            
            with self.subTest(form=form, prompt_type="initial"):
                self.assertIsInstance(prompt, str)
                self.assertGreater(len(prompt), 50)
                self.assertIn("TestPoet", prompt)
                self.assertIn("test theme", prompt)
                self.assertIn(form, prompt)
        
        # Test response prompts
        for form in ["haiku", "prose", "sonnet", "villanelle", "limerick", "ballad", "ghazal", "tanka"]:
            prompt = create_response_poetry_prompt("TestPoet", "previous poetry", form, 5)
            
            with self.subTest(form=form, prompt_type="response"):
                self.assertIsInstance(prompt, str)
                self.assertGreater(len(prompt), 50)
                self.assertIn("TestPoet", prompt)
                self.assertIn("previous poetry", prompt)
                self.assertIn(form, prompt)
    
    def test_edge_cases(self):
        """Test edge cases for prompt generation."""
        # Empty theme
        prompt = create_initial_poetry_prompt("", "haiku", 3, "Poet")
        self.assertIsInstance(prompt, str)
        self.assertIn("haiku", prompt)
        
        # Very long theme
        long_theme = "This is a very long theme that goes on and on " * 10
        prompt = create_initial_poetry_prompt(long_theme, "prose", 5, "Poet")
        self.assertIn(long_theme, prompt)
        
        # Special characters in theme
        special_theme = "theme with @#$%^&*() characters"
        prompt = create_initial_poetry_prompt(special_theme, "haiku", 3, "Poet")
        self.assertIn(special_theme, prompt)
        
        # Zero length
        prompt = create_initial_poetry_prompt("theme", "prose", 0, "Poet")
        self.assertIn("0-line", prompt)
        
        # Large length
        prompt = create_initial_poetry_prompt("theme", "prose", 100, "Poet")
        self.assertIn("100-line", prompt)


if __name__ == '__main__':
    unittest.main()