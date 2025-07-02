#!/usr/bin/env python3
"""
Test script to verify the literary personas are working correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from character_names import get_character_persona, get_random_names
from prompts import create_initial_poetry_prompt, create_response_poetry_prompt

def test_persona_examples():
    """Test a few persona examples to see the enhanced prompts."""
    
    print("Testing Literary Personas")
    print("=" * 50)
    
    # Test a few specific characters
    test_characters = ["Elizabeth", "Gandalf", "Sherlock", "Gatsby", "Holden"]
    
    for char in test_characters:
        print(f"\n**{char}:**")
        persona = get_character_persona(char)
        print(f"Persona: {persona}")
        
        # Test initial prompt
        initial_prompt = create_initial_poetry_prompt(
            theme="a walk in the snow",
            form="haiku", 
            length=1,
            agent_name=char
        )
        print(f"\nInitial Prompt Preview:")
        print(f"'{initial_prompt[:100]}...'")
        
        # Test response prompt
        response_prompt = create_response_poetry_prompt(
            agent_name=char,
            previous_poetry="Snow falls gently down\nCovering the silent earth\nWinter's peace descends",
            form="haiku",
            length=1
        )
        print(f"\nResponse Prompt Preview:")
        print(f"'{response_prompt[:100]}...'")
        print("-" * 30)

def test_random_selection():
    """Test that random name selection includes persona characters."""
    
    print("\n\nTesting Random Name Selection")
    print("=" * 50)
    
    # Get 5 random names
    names = get_random_names(5)
    print(f"Random names selected: {names}")
    
    for name in names:
        persona = get_character_persona(name)
        print(f"\n{name}: {persona[:50]}...")

if __name__ == "__main__":
    test_persona_examples()
    test_random_selection()
    
    print("\n" + "=" * 50)
    print("Persona testing complete!")
    print("The system now uses rich literary personas for enhanced poetry generation.")