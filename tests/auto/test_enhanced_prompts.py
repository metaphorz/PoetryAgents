#!/usr/bin/env python3
"""
Test script to validate enhanced prompts with comprehensive structural rules.
"""

from prompts import create_initial_poetry_prompt, create_response_poetry_prompt
from character_names import get_random_names

def test_prompt_structure():
    """Test that prompts include comprehensive structural rules."""
    print("=== Testing Enhanced Prompt Structure ===\n")
    
    # Test different poetry forms
    forms_to_test = ['haiku', 'sonnet', 'villanelle', 'limerick', 'ballad', 'ghazal', 'tanka', 'prose']
    theme = "winter moonlight"
    agent_names = get_random_names(2)
    
    for form in forms_to_test:
        print(f"--- Testing {form.upper()} ---")
        
        # Test initial prompt with character
        initial_prompt = create_initial_poetry_prompt(theme, form, 1, agent_names[0])
        
        # Check that prompt includes key components
        checks = {
            "Character persona": agent_names[0] in initial_prompt,
            "Character background": "CHARACTER BACKGROUND:" in initial_prompt,
            "Structural rules": f"{form.upper()} STRUCTURAL RULES:" in initial_prompt,
            "Quality guidelines": "QUALITY GUIDELINES:" in initial_prompt,
            "Formatting rules": "FORMATTING RULES:" in initial_prompt,
            "Theme reference": theme in initial_prompt,
            "Task instruction": "TASK:" in initial_prompt
        }
        
        print(f"Form: {form}")
        print(f"Character: {agent_names[0]}")
        for check, passed in checks.items():
            status = "✓" if passed else "✗"
            print(f"  {status} {check}")
        
        # Show prompt length (should be comprehensive)
        print(f"  Prompt length: {len(initial_prompt)} characters")
        print()

def test_character_enhancement():
    """Test that character personas include enhanced details."""
    print("=== Testing Character Enhancement ===\n")
    
    from character_names import get_enhanced_character_persona, CHARACTER_PERSONAS
    
    # Test a few well-known characters
    test_characters = ['Elizabeth', 'Sherlock', 'Gatsby', 'Jane']
    
    for char in test_characters:
        if char in CHARACTER_PERSONAS:
            enhanced_persona = get_enhanced_character_persona(char)
            
            print(f"--- {char} ---")
            print(f"Length: {len(enhanced_persona)} characters")
            
            # Check components
            checks = {
                "Basic persona": char in enhanced_persona,
                "Source info": "Source:" in enhanced_persona,
                "Character traits": "Character Traits:" in enhanced_persona,
                "Writing guidance": "WRITING GUIDANCE:" in enhanced_persona,
                "Trait embodiment": "Embody these character traits" in enhanced_persona
            }
            
            for check, passed in checks.items():
                status = "✓" if passed else "✗"
                print(f"  {status} {check}")
            print()

def test_structural_rules():
    """Test that structural rules are comprehensive for each form."""
    print("=== Testing Structural Rules ===\n")
    
    from poetry_rules import get_poetry_rules
    
    forms = ['haiku', 'sonnet', 'villanelle', 'limerick', 'ballad', 'ghazal', 'tanka', 'prose']
    
    for form in forms:
        rules = get_poetry_rules(form)
        print(f"--- {form.upper()} RULES ---")
        print(f"Length: {len(rules)} characters")
        
        # Check for key structural elements
        if form == 'haiku':
            checks = ["5-7-5", "syllable", "3 lines", "EXACTLY"]
        elif form == 'sonnet':
            checks = ["14 lines", "ABAB CDCD EFEF GG", "iambic pentameter", "quatrain"]
        elif form == 'villanelle':
            checks = ["19 lines", "refrain", "A1bA2", "tercet"]
        elif form == 'limerick':
            checks = ["5 lines", "AABBA", "anapestic", "witty"]
        elif form == 'ballad':
            checks = ["quatrain", "ABAB", "tetrameter", "narrative"]
        elif form == 'ghazal':
            checks = ["couplet", "radif", "qafia", "independent"]
        elif form == 'tanka':
            checks = ["5-7-5-7-7", "31 syllables", "pivot", "5 lines"]
        elif form == 'prose':
            checks = ["paragraph", "poetic devices", "imagery", "prose format"]
        
        for check in checks:
            found = check.lower() in rules.lower()
            status = "✓" if found else "✗"
            print(f"  {status} Contains '{check}'")
        print()

if __name__ == "__main__":
    test_prompt_structure()
    test_character_enhancement()
    test_structural_rules()
    print("=== Test Complete ===")