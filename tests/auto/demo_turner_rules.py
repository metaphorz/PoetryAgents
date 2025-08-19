#!/usr/bin/env python3
"""
Demo script showing Turner-based rules integration in action.
Demonstrates how the enhanced judge system will provide better critique and editing.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def demo_critique_prompt():
    """Demonstrate the enhanced critique prompt with Turner rules."""
    print("=" * 60)
    print("DEMO: Turner-Based Critique Prompt")
    print("=" * 60)
    
    from critique_service import CritiqueService
    
    # Sample dialogue with typical poetry problems that Turner rules address
    sample_dialogue = {
        'title': 'Love and Nature',
        'agents': ['Elizabeth', 'William'], 
        'conversation': [
            {
                'agent': 'Elizabeth',
                'poetry': "O'er the meadow fair and bright,\nThou dost walk in morning light,\nForsooth, thy beauty doth inspire,\nMy heart with love and sweet desire.",
                'round': 1,
                'agent_index': 0,
                'llm_used': 'Claude'
            },
            {
                'agent': 'William',
                'poetry': "Nature is beautiful and grand,\nLove fills the heart with joy so true,\nHappiness spreads across the land,\nEverything is good and new.",
                'round': 1, 
                'agent_index': 1,
                'llm_used': 'Gemini'
            }
        ],
        'config': {
            'theme': 'love in nature',
            'form': 'ballad',
            'poem_length': 4,
            'conversation_length': 1,
            'use_openrouter': False,
            'agent1_llm': 'Claude',
            'agent2_llm': 'Gemini'
        }
    }
    
    critique_service = CritiqueService()
    critique_prompt = critique_service._create_critique_prompt(sample_dialogue)
    
    print("Sample problematic poetry:")
    print("Elizabeth: Uses archaic language (O'er, thou, dost, forsooth)")
    print("William: Abstract language, one-dimensional positive emotions")
    print()
    print("Turner-enhanced critique prompt will identify:")
    print("✅ Archaic language violations") 
    print("✅ Lack of mixed emotions")
    print("✅ Abstract vs concrete imagery issues")
    print("✅ Form adherence problems")
    print("✅ Natural scansion issues")
    print()
    print("Prompt length:", len(critique_prompt), "characters")
    print("Contains Turner framework:", "TURNER-BASED CRITIQUE FRAMEWORK" in critique_prompt)
    print()

def demo_edit_prompt():
    """Demonstrate the enhanced edit prompt with Turner rules."""
    print("=" * 60) 
    print("DEMO: Turner-Based Edit Prompt")
    print("=" * 60)
    
    from critique_service import CritiqueService
    
    sample_dialogue = {
        'agents': ['Elizabeth', 'William'],
        'conversation': [
            {'agent': 'Elizabeth', 'poetry': "O'er fields I wander, lost in thought"},
            {'agent': 'William', 'poetry': "Abstract beauty fills my soul"}
        ],
        'config': {
            'theme': 'nature reflection',
            'form': 'haiku'
        }
    }
    
    sample_critique = """The poems suffer from several issues:
1. Elizabeth uses archaic language ("O'er") that Turner rules discourage
2. William's language is too abstract without concrete imagery
3. Both lack emotional complexity - only positive emotions shown
4. Missing sensory details and specific imagery"""
    
    critique_service = CritiqueService()
    edit_prompt = critique_service._create_edit_prompt(sample_dialogue, sample_critique)
    
    print("Sample critique identifies Turner rule violations")
    print()
    print("Turner-enhanced edit prompt will guide:")
    print("✅ Replace archaic language with modern terms")
    print("✅ Add concrete, sensory imagery") 
    print("✅ Include mixed emotions (positive + negative)")
    print("✅ Strengthen form adherence")
    print("✅ Improve natural scansion")
    print()
    print("Prompt length:", len(edit_prompt), "characters")
    print("Contains improvement guidelines:", "TURNER-BASED IMPROVEMENT GUIDELINES" in edit_prompt)
    print()

def demo_rules_categories():
    """Show the structured Turner rules organization."""
    print("=" * 60)
    print("DEMO: Turner Rules Structure")
    print("=" * 60)
    
    from turner_rules import TurnerRulesManager
    
    manager = TurnerRulesManager()
    
    print("Rule Categories:")
    for category in manager.get_all_categories():
        rules = manager.get_rules_by_category(category)
        print(f"\n{category.replace('_', ' ').title()} ({len(rules)} rules):")
        for rule in rules:
            print(f"  • {rule['title']}")
    
    print(f"\nAvoid List ({len(manager.get_avoid_list())} items):")
    for item in manager.get_avoid_list()[:5]:  # Show first 5
        print(f"  • {item}")
    print("  ...")
    
    print(f"\nEnhance List ({len(manager.get_enhance_list())} items):")
    for item in manager.get_enhance_list()[:5]:  # Show first 5
        print(f"  • {item}")
    print("  ...")

def run_demo():
    """Run all demos."""
    print("🎭 TURNER RULES INTEGRATION DEMO")
    print("This demonstrates how Fred Turner's poetry guidelines are now")
    print("integrated into the judge/editor system for better critique and improvement.\n")
    
    demo_rules_categories()
    demo_critique_prompt() 
    demo_edit_prompt()
    
    print("=" * 60)
    print("🎉 INTEGRATION COMPLETE!")
    print("=" * 60)
    print("The judge system now applies Turner's 16 comprehensive poetry rules")
    print("across 5 categories for sophisticated literary analysis and improvement.")
    print()
    print("Next: Run the main system to see Turner rules in action!")
    print("  python main.py")
    print()

if __name__ == "__main__":
    run_demo()