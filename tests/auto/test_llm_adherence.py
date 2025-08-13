#!/usr/bin/env python3
"""
Test LLM adherence to enhanced structural rules.
This script generates actual prompts and can be used to test with LLM providers.
"""

from prompts import create_initial_poetry_prompt, create_response_poetry_prompt
from character_names import get_random_names

def test_haiku_prompt():
    """Generate a comprehensive haiku prompt to test LLM adherence."""
    print("=== HAIKU PROMPT TEST ===\n")
    
    agent_name = "Elizabeth"  # Elizabeth Bennet
    theme = "autumn leaves falling"
    form = "haiku"
    length = 1
    
    prompt = create_initial_poetry_prompt(theme, form, length, agent_name)
    
    print("Generated Haiku Prompt:")
    print("-" * 50)
    print(prompt)
    print("-" * 50)
    print(f"Prompt length: {len(prompt)} characters")
    print()
    
    # Key adherence points to check in LLM response:
    print("Expected LLM adherence points:")
    print("✓ Exactly 3 lines")
    print("✓ 5-7-5 syllable pattern")
    print("✓ No explanatory text")
    print("✓ Elizabeth Bennet's witty, perceptive voice")
    print("✓ Present tense, nature focus")
    print("✓ Total of 17 syllables")
    print()

def test_sonnet_prompt():
    """Generate a comprehensive sonnet prompt to test LLM adherence."""
    print("=== SONNET PROMPT TEST ===\n")
    
    agent_name = "Sherlock"  # Sherlock Holmes
    theme = "solving a mystery"
    form = "sonnet"
    length = 14
    
    prompt = create_initial_poetry_prompt(theme, form, length, agent_name)
    
    print("Generated Sonnet Prompt:")
    print("-" * 50)
    print(prompt)
    print("-" * 50)
    print(f"Prompt length: {len(prompt)} characters")
    print()
    
    print("Expected LLM adherence points:")
    print("✓ Exactly 14 lines")
    print("✓ ABAB CDCD EFEF GG rhyme scheme")
    print("✓ Iambic pentameter (10 syllables per line)")
    print("✓ 3 quatrains + 1 couplet structure")
    print("✓ Sherlock's analytical, observant voice")
    print("✓ Final couplet provides resolution")
    print()

def test_response_prompt():
    """Generate a response prompt to test dialogue adherence."""
    print("=== RESPONSE PROMPT TEST ===\n")
    
    agent_name = "Gatsby"  # Jay Gatsby  
    form = "haiku"
    length = 1
    
    # Simulate conversation context
    conversation_context = """Theme: winter moonlight

Elizabeth:
Frost whispers softly
Silver light on bare branches
Winter's gentle breath"""
    
    prompt = create_response_poetry_prompt(agent_name, conversation_context, form, length)
    
    print("Generated Response Prompt:")
    print("-" * 50)
    print(prompt)
    print("-" * 50)
    print(f"Prompt length: {len(prompt)} characters")
    print()
    
    print("Expected LLM adherence points:")
    print("✓ Responds to Elizabeth's haiku about winter/frost")
    print("✓ Maintains haiku structure (5-7-5)")
    print("✓ References previous poem's images/themes")
    print("✓ Gatsby's romantic, idealistic voice")
    print("✓ Continues the conversation meaningfully")
    print()

def test_complex_form():
    """Test a complex form like villanelle."""
    print("=== VILLANELLE PROMPT TEST ===\n")
    
    agent_name = "Heathcliff"  # Passionate, stormy character
    theme = "obsessive love"
    form = "villanelle"
    length = 19
    
    prompt = create_initial_poetry_prompt(theme, form, length, agent_name)
    
    print("Generated Villanelle Prompt:")
    print("-" * 50)
    print(prompt[:500] + "..." if len(prompt) > 500 else prompt)  # Truncate for readability
    print("-" * 50)
    print(f"Prompt length: {len(prompt)} characters")
    print()
    
    print("Expected LLM adherence points:")
    print("✓ Exactly 19 lines")
    print("✓ A1bA2 abA1 abA2 abA1 abA2 abA1A2 pattern")
    print("✓ Two refrains (A1 and A2) repeated correctly")
    print("✓ Only 2 rhyme sounds throughout")
    print("✓ 5 tercets + 1 quatrain structure")
    print("✓ Heathcliff's passionate, intense voice")
    print("✓ Theme of obsessive love")
    print()

def show_character_details():
    """Show how character details are incorporated."""
    print("=== CHARACTER PERSONA INTEGRATION ===\n")
    
    from character_names import get_enhanced_character_persona
    
    test_chars = ["Elizabeth", "Sherlock", "Gatsby", "Heathcliff"]
    
    for char in test_chars:
        persona = get_enhanced_character_persona(char)
        print(f"--- {char} ---")
        print(persona[:200] + "..." if len(persona) > 200 else persona)
        print()

if __name__ == "__main__":
    test_haiku_prompt()
    test_sonnet_prompt() 
    test_response_prompt()
    test_complex_form()
    show_character_details()
    
    print("=== TESTING COMPLETE ===")
    print("\nTo test LLM adherence:")
    print("1. Copy any of the generated prompts above")
    print("2. Send to your preferred LLM (Claude, GPT-4, Gemini, etc.)")
    print("3. Check the response against the adherence points listed")
    print("4. Verify structural requirements are met")