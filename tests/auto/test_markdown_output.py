#!/usr/bin/env python3
"""
Test script to verify the markdown output functionality.
"""

import sys
import os

# Add parent directory to path to import modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from dialogue_manager import DialogueManager

def test_markdown_output():
    """Test markdown file generation with sample data."""
    
    print("Testing Markdown Output")
    print("=" * 50)
    
    # Create sample dialogue data (simulating what would come from LLM)
    sample_dialogue_data = {
        'title': 'Winter Walk',
        'ascii_art': '    *  *  *\n   /     \\\n  * Snow *\n   \\     /\n    *  *  *',
        'agents': ['Elizabeth', 'Gandalf'],
        'conversation': [
            {
                'agent': 'Elizabeth',
                'poetry': 'Fresh snow crunches soft\nBeneath my careful footsteps—\nSilent world awaits\n\nBreath clouds drift and fade\nWhile bare branches frame the sky\nPeace in winter\'s grip',
                'round': 1,
                'agent_index': 0
            },
            {
                'agent': 'Gandalf',
                'poetry': 'Your tracks mark the path\nI follow through drifted white—\nTwo souls, one winter\n\nWhere you found silence\nI hear whispers in the wind\nSpeaking of spring\'s hope',
                'round': 1,
                'agent_index': 1
            }
        ],
        'config': {
            'theme': 'a walk in the snow',
            'num_agents': 2,
            'form': 'haiku',
            'poem_length': 2,
            'conversation_length': 1,
            'output_format': 'markdown'
        }
    }
    
    # Test markdown generation
    manager = DialogueManager()
    filename = manager.save_dialogue_to_markdown(sample_dialogue_data)
    
    print(f"✓ Sample markdown file created: {filename}")
    
    # Read and display a preview
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("\nMarkdown Content Preview:")
    print("-" * 30)
    print(content[:500] + "..." if len(content) > 500 else content)
    
    return filename

if __name__ == "__main__":
    filename = test_markdown_output()
    print(f"\n✓ Markdown output test complete!")
    print(f"Open '{filename}' in any markdown viewer to see the formatted poetry.")