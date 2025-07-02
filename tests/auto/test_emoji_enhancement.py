#!/usr/bin/env python3
"""
Test script to verify emoji enhancement functionality.
"""

import sys
import os

# Add parent directory to path to import modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from dialogue_manager import DialogueManager

def test_emoji_enhancement():
    """Test emoji enhancement for sample poetry."""
    
    print("Testing Emoji Enhancement")
    print("=" * 50)
    
    manager = DialogueManager()
    
    # Sample poetry without emojis
    sample_poetry = """Fresh snow crunches soft
Beneath my careful footsteps—
Silent world awaits

Breath clouds drift and fade
While bare branches frame the sky
Peace in winter's grip"""
    
    theme = "a walk in the snow"
    
    print("**Original Poetry:**")
    print(sample_poetry)
    print()
    
    print("**Enhanced with Emojis:**")
    # Test the emoji enhancement function
    enhanced_poetry = manager.add_emojis_to_poetry(sample_poetry, theme)
    print(enhanced_poetry)
    print()

def test_markdown_with_emojis():
    """Test markdown generation with emoji configuration."""
    
    print("\n" + "=" * 50)
    print("Testing Markdown with Emoji Configuration")
    print("=" * 50)
    
    # Sample dialogue data with emojis enabled
    sample_dialogue_data = {
        'title': 'Winter Walk',
        'ascii_art': '    *   *   *\n  *   *   *\n*   SNOW   *\n  *   *   *\n    *   *   *',
        'agents': ['Elizabeth', 'Gandalf'],
        'conversation': [
            {
                'agent': 'Elizabeth',
                'poetry': 'Fresh snow❄️ crunches soft\nBeneath my careful footsteps👣—\nSilent world🌍 awaits',
                'round': 1,
                'agent_index': 0
            }
        ],
        'config': {
            'theme': 'a walk in the snow',
            'num_agents': 2,
            'form': 'haiku',
            'poem_length': 1,
            'conversation_length': 1,
            'use_emojis': True,
            'output_format': 'markdown'
        }
    }
    
    manager = DialogueManager()
    filename = manager.save_dialogue_to_markdown(sample_dialogue_data)
    
    print(f"✓ Sample markdown file with emojis created: {filename}")
    
    # Read and display a preview
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("\nMarkdown Content Preview:")
    print("-" * 30)
    lines = content.split('\n')
    for i, line in enumerate(lines[:20]):  # Show first 20 lines
        print(line)
        if i == 19 and len(lines) > 20:
            print("...")
    
    return filename

if __name__ == "__main__":
    test_emoji_enhancement()
    filename = test_markdown_with_emojis()
    
    print("\n" + "=" * 50)
    print("Emoji enhancement testing complete!")
    print(f"Check '{filename}' to see emojis in formatted output.")