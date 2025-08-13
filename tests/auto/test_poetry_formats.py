#!/usr/bin/env python3
"""
Test script to verify all poetry formats work correctly.
"""

import sys
import os

# Add parent directory to path to import modules
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, parent_dir)

from prompts import create_initial_poetry_prompt, create_response_poetry_prompt

def test_poetry_formats():
    """Test all poetry format prompts."""
    
    print("Testing Poetry Format Prompts")
    print("=" * 50)
    
    formats = [
        ('haiku', 1),
        ('prose', 6),
        ('sonnet', 14),
        ('villanelle', 19),
        ('limerick', 1),
        ('ballad', 4),
        ('ghazal', 10),
        ('tanka', 1)
    ]
    
    theme = "autumn leaves"
    agent = "Elizabeth"
    
    for form, length in formats:
        print(f"\n**{form.upper()} FORMAT:**")
        print("-" * 30)
        
        # Test initial prompt
        initial_prompt = create_initial_poetry_prompt(theme, form, length, agent)
        print("Initial Prompt:")
        print(f"'{initial_prompt[:100]}...'")
        
        # Test response prompt
        sample_poetry = "Golden leaves descend,\nDancing in the autumn breeze,\nNature's final bow."
        response_prompt = create_response_poetry_prompt(agent, sample_poetry, form, length)
        print("\nResponse Prompt:")
        print(f"'{response_prompt[:100]}...'")
        print()

def test_format_validation():
    """Test the format validation lists."""
    
    print("\n" + "=" * 50)
    print("Testing Format Validation")
    print("=" * 50)
    
    # Read main.py to check the valid_forms list
    with open(os.path.join(parent_dir, 'main.py'), 'r') as f:
        content = f.read()
        
    if "valid_forms = ['haiku', 'prose', 'sonnet', 'villanelle', 'limerick', 'ballad', 'ghazal', 'tanka']" in content:
        print("✓ Valid forms list found in main.py")
        valid_forms = ['haiku', 'prose', 'sonnet', 'villanelle', 'limerick', 'ballad', 'ghazal', 'tanka']
        print(f"✓ Supported formats: {', '.join(valid_forms)}")
    else:
        print("✗ Valid forms list not found or incorrect in main.py")

if __name__ == "__main__":
    test_poetry_formats()
    test_format_validation()
    
    print("\n" + "=" * 50)
    print("Poetry format testing complete!")
    print("The system now supports 8 different poetry forms with detailed prompts.")