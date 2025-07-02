"""
Test script to demonstrate the new simplified question flow
"""

def show_question_flow():
    """Display the new simplified question flow."""
    print("=" * 60)
    print("NEW SIMPLIFIED QUESTION FLOW")
    print("=" * 60)
    print()
    
    print("1. What is the theme?")
    print("   → User enters theme (e.g., 'autumn leaves')")
    print()
    
    print("2. What is the form of dialogue?")
    print("   → Available: haiku, prose, sonnet, villanelle, limerick, ballad, ghazal, tanka")
    print()
    
    print("3. Length question (FORM-DEPENDENT):")
    print("   → Fixed forms (haiku, sonnet, etc.): Shows traditional length automatically")
    print("   → Ballad: 'How many stanzas for each ballad?'")
    print("   → Ghazal: 'How many couplets for each ghazal? (5-15 recommended)'")
    print("   → Prose: 'How many paragraphs for each prose piece?'")
    print()
    
    print("4. How many rounds of conversation? (each agent will write one poem per round)")
    print("   → Clarifies that 2 agents × 3 rounds = 6 total poems")
    print()
    
    print("5. Which LLM should Agent 1 use? (Claude/Gemini)")
    print("   → Always asks, since we always have 2 agents")
    print()
    
    print("6. Which LLM should Agent 2 use? (Claude/Gemini)")
    print("   → Always asks, since we always have 2 agents")
    print()
    
    print("7. Add emojis to enhance the poetry? (yes/no)")
    print("   → Optional emoji enhancement")
    print()
    
    print("=" * 60)
    print("CHANGES MADE:")
    print("=" * 60)
    print("✓ REMOVED: 'How many agents are there?' (now always 2)")
    print("✓ IMPROVED: Length questions are form-specific")
    print("✓ CLARIFIED: Conversation length explains rounds vs total poems")
    print("✓ SIMPLIFIED: Question numbering reduced from 8 to 7")
    print("✓ STREAMLINED: Agent 2 LLM question always appears (no conditional logic)")
    print()

if __name__ == "__main__":
    show_question_flow()