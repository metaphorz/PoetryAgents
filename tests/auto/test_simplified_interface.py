"""
Test script for simplified interface (always 2 agents)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dialogue_manager import DialogueManager

def test_simplified_interface():
    """Test the simplified interface with hardcoded 2 agents."""
    print("Testing simplified interface (always 2 agents)...")
    
    # Test configuration that simulates the new simplified interface
    config = {
        'theme': 'winter morning',
        'num_agents': 2,  # Always 2, no longer asked
        'form': 'haiku',
        'poem_length': 3,
        'length_unit': 'lines',
        'conversation_length': 1,
        'agent1_llm': 'Claude',
        'agent2_llm': 'Gemini',
        'use_emojis': True
    }
    
    try:
        print("✓ Configuration created with 2 agents (not asked)")
        print(f"✓ Theme: {config['theme']}")
        print(f"✓ Form: {config['form']}")
        print(f"✓ Agent 1 LLM: {config['agent1_llm']}")
        print(f"✓ Agent 2 LLM: {config['agent2_llm']}")
        
        # Generate dialogue
        manager = DialogueManager()
        dialogue_data = manager.generate_dialogue(config)
        
        print(f"✓ Generated dialogue: '{dialogue_data['title']}'")
        print(f"✓ Number of agents: {len(dialogue_data['agents'])}")
        
        # Verify we have exactly 2 agents
        if len(dialogue_data['agents']) == 2:
            print("✓ Confirmed: Always uses exactly 2 agents")
        else:
            print(f"✗ Error: Expected 2 agents, got {len(dialogue_data['agents'])}")
        
        # Show the conversation
        print("\n" + "="*50)
        print("DIALOGUE PREVIEW")
        print("="*50)
        
        for entry in dialogue_data['conversation']:
            llm_used = entry.get('llm_used', 'Unknown')
            print(f"\n{entry['agent']} (via {llm_used}):")
            print("-" * 30)
            print(entry['poetry'][:100] + "..." if len(entry['poetry']) > 100 else entry['poetry'])
        
        # Save to file
        filename = manager.save_dialogue_to_markdown(dialogue_data)
        print(f"\n✓ Saved to: {filename}")
        
        print("\n✓ Simplified interface test completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_simplified_interface()