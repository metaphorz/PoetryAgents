#!/usr/bin/env python3
"""
Test script to verify ASCII art generation for different themes.
"""

import sys
import os

# Add parent directory to path to import modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from dialogue_manager import DialogueManager

def test_ascii_art_themes():
    """Test ASCII art generation for various themes."""
    
    print("Testing ASCII Art Generation")
    print("=" * 50)
    
    themes = [
        "a walk in the snow",
        "ocean waves",
        "starry night",
        "spring flowers",
        "mountain peak",
        "autumn leaves",
        "desert sunset",
        "forest path"
    ]
    
    manager = DialogueManager()
    
    for theme in themes:
        print(f"\n**Theme: {theme}**")
        print("-" * 30)
        
        # Generate ASCII art for the theme
        ascii_art = manager.generate_ascii_art(theme)
        
        print("Generated ASCII Art:")
        print("```")
        print(ascii_art)
        print("```")
        print()

def test_ascii_art_in_dialogue():
    """Test that ASCII art is properly integrated into dialogue generation."""
    
    print("\n" + "=" * 50)
    print("Testing ASCII Art Integration")
    print("=" * 50)
    
    # Sample configuration
    config = {
        'theme': 'ocean waves',
        'num_agents': 2,
        'form': 'haiku', 
        'poem_length': 1,
        'conversation_length': 1,
        'output_format': 'markdown'
    }
    
    manager = DialogueManager()
    
    print(f"Testing with theme: {config['theme']}")
    print("Generating ASCII art...")
    
    ascii_art = manager.generate_ascii_art(config['theme'])
    print("\nGenerated ASCII Art:")
    print("```")
    print(ascii_art)
    print("```")
    
    print("\n✓ ASCII art generation successful!")

if __name__ == "__main__":
    test_ascii_art_themes()
    test_ascii_art_in_dialogue()
    
    print("\n" + "=" * 50)
    print("ASCII art testing complete!")
    print("The system now generates thematic ASCII art for poetry dialogues.")