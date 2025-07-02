"""
Comprehensive unit tests with coverage for character_names.py
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from character_names import (
    CHARACTER_PERSONAS, 
    ADDITIONAL_NAMES, 
    FICTIONAL_NAMES,
    get_random_names, 
    get_random_name, 
    get_character_persona, 
    get_character_info
)


class TestCharacterNames(unittest.TestCase):
    """Test character names module functionality."""
    
    def test_character_personas_structure(self):
        """Test that CHARACTER_PERSONAS has proper structure."""
        self.assertIsInstance(CHARACTER_PERSONAS, dict)
        self.assertGreater(len(CHARACTER_PERSONAS), 25)  # Should have 35+ characters
        
        # Test structure of a known character
        self.assertIn("Elizabeth", CHARACTER_PERSONAS)
        elizabeth = CHARACTER_PERSONAS["Elizabeth"]
        required_keys = ["persona", "source", "qualities"]
        for key in required_keys:
            self.assertIn(key, elizabeth)
            self.assertIsInstance(elizabeth[key], str)
            self.assertGreater(len(elizabeth[key]), 5)
    
    def test_additional_names_structure(self):
        """Test ADDITIONAL_NAMES list."""
        self.assertIsInstance(ADDITIONAL_NAMES, list)
        self.assertGreater(len(ADDITIONAL_NAMES), 10)
        for name in ADDITIONAL_NAMES:
            self.assertIsInstance(name, str)
            self.assertGreater(len(name), 1)
    
    def test_fictional_names_combination(self):
        """Test that FICTIONAL_NAMES combines personas and additional names."""
        self.assertIsInstance(FICTIONAL_NAMES, list)
        expected_length = len(CHARACTER_PERSONAS) + len(ADDITIONAL_NAMES)
        self.assertEqual(len(FICTIONAL_NAMES), expected_length)
        
        # Check that persona characters are included
        for persona_name in CHARACTER_PERSONAS.keys():
            self.assertIn(persona_name, FICTIONAL_NAMES)
    
    def test_get_random_names_small_count(self):
        """Test getting small number of names (within persona range)."""
        names = get_random_names(3)
        self.assertEqual(len(names), 3)
        self.assertEqual(len(set(names)), 3)  # All unique
        
        # Should prioritize persona characters
        persona_count = sum(1 for name in names if name in CHARACTER_PERSONAS)
        self.assertGreaterEqual(persona_count, 2)  # Most should be from personas
    
    def test_get_random_names_large_count(self):
        """Test getting large number of names (beyond persona range)."""
        persona_count = len(CHARACTER_PERSONAS)
        names = get_random_names(persona_count + 5)
        
        self.assertEqual(len(names), persona_count + 5)
        self.assertEqual(len(set(names)), persona_count + 5)  # All unique
        
        # Should include all persona characters plus some additional
        persona_names_in_result = [name for name in names if name in CHARACTER_PERSONAS]
        self.assertGreaterEqual(len(persona_names_in_result), persona_count - 5)
    
    def test_get_random_names_edge_cases(self):
        """Test edge cases for get_random_names."""
        # Single name
        names = get_random_names(1)
        self.assertEqual(len(names), 1)
        
        # Zero names
        names = get_random_names(0)
        self.assertEqual(len(names), 0)
        
        # Maximum available names
        max_names = len(CHARACTER_PERSONAS) + len(ADDITIONAL_NAMES)
        names = get_random_names(max_names)
        self.assertEqual(len(names), max_names)
        self.assertEqual(len(set(names)), max_names)
    
    def test_get_random_name(self):
        """Test getting single random name."""
        name = get_random_name()
        self.assertIsInstance(name, str)
        self.assertIn(name, FICTIONAL_NAMES)
        self.assertGreater(len(name), 1)
        
        # Test multiple calls return valid names
        for _ in range(10):
            name = get_random_name()
            self.assertIn(name, FICTIONAL_NAMES)
    
    def test_get_character_persona_with_known_character(self):
        """Test getting persona for known character."""
        persona = get_character_persona("Elizabeth")
        self.assertIsInstance(persona, str)
        self.assertIn("Elizabeth", persona)
        # The persona should mention the character name
        
        # Test another known character
        persona = get_character_persona("Gandalf")
        self.assertIn("Gandalf", persona)
        self.assertIsInstance(persona, str)
    
    def test_get_character_persona_with_unknown_character(self):
        """Test getting persona for unknown character."""
        persona = get_character_persona("UnknownCharacter")
        self.assertIsInstance(persona, str)
        self.assertIn("UnknownCharacter", persona)
        self.assertIn("distinctive literary character", persona)
    
    def test_get_character_info_with_known_character(self):
        """Test getting complete character info for known character."""
        info = get_character_info("Elizabeth")
        self.assertIsInstance(info, dict)
        
        required_keys = ["persona", "source", "qualities"]
        for key in required_keys:
            self.assertIn(key, info)
            self.assertIsInstance(info[key], str)
        
        self.assertIn("Pride and Prejudice", info["source"])
        self.assertIn("Jane Austen", info["source"])
    
    def test_get_character_info_with_unknown_character(self):
        """Test getting character info for unknown character."""
        info = get_character_info("UnknownCharacter")
        self.assertIsInstance(info, dict)
        
        required_keys = ["persona", "source", "qualities"]
        for key in required_keys:
            self.assertIn(key, info)
            self.assertIsInstance(info[key], str)
        
        self.assertEqual(info["source"], "Various literature")
        self.assertIn("UnknownCharacter", info["persona"])
    
    def test_all_persona_characters_have_complete_info(self):
        """Test that all characters in CHARACTER_PERSONAS have complete information."""
        for name, info in CHARACTER_PERSONAS.items():
            with self.subTest(character=name):
                # Test persona
                self.assertIn("persona", info)
                self.assertIn(name, info["persona"])
                self.assertGreater(len(info["persona"]), 50)
                
                # Test source
                self.assertIn("source", info)
                self.assertGreater(len(info["source"]), 10)
                
                # Test qualities
                self.assertIn("qualities", info)
                self.assertGreater(len(info["qualities"]), 20)
    
    def test_no_duplicate_names_in_lists(self):
        """Test that there are no duplicate names in the lists."""
        # No duplicates in CHARACTER_PERSONAS keys
        persona_names = list(CHARACTER_PERSONAS.keys())
        self.assertEqual(len(persona_names), len(set(persona_names)))
        
        # No duplicates in ADDITIONAL_NAMES
        self.assertEqual(len(ADDITIONAL_NAMES), len(set(ADDITIONAL_NAMES)))
        
        # No overlap between persona names and additional names
        persona_set = set(CHARACTER_PERSONAS.keys())
        additional_set = set(ADDITIONAL_NAMES)
        self.assertEqual(len(persona_set.intersection(additional_set)), 0)


if __name__ == '__main__':
    unittest.main()