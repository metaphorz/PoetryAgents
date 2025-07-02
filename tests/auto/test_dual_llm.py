"""
Test script for dual LLM poetry generation (Claude + Gemini)
"""

from dialogue_manager import DialogueManager

def test_dual_llm_poetry():
    """Test poetry generation with both Claude and Gemini."""
    print("Testing dual LLM poetry generation...")
    
    # Create test configuration with user-specified LLMs
    config = {
        'theme': 'autumn leaves falling',
        'num_agents': 2,
        'form': 'haiku',
        'poem_length': 1,
        'conversation_length': 1,
        'agent1_llm': 'Claude',
        'agent2_llm': 'Gemini',
        'use_emojis': True
    }
    
    try:
        # Initialize dialogue manager
        manager = DialogueManager()
        print("✓ Dialogue manager initialized with Claude and Gemini clients")
        
        # Generate dialogue
        print(f"\nGenerating poetry dialogue about: {config['theme']}")
        dialogue_data = manager.generate_dialogue(config)
        
        print(f"✓ Generated dialogue with title: '{dialogue_data['title']}'")
        print(f"✓ Agents: {', '.join(dialogue_data['agents'])}")
        
        # Display the conversation
        print("\n" + "="*60)
        print("POETRY DIALOGUE")
        print("="*60)
        
        for entry in dialogue_data['conversation']:
            llm_used = entry.get('llm_used', 'Unknown')
            print(f"\n{entry['agent']} (via {llm_used}):")
            print("-" * 40)
            print(entry['poetry'])
        
        print("\n" + "="*60)
        
        # Save to markdown
        filename = manager.save_dialogue_to_markdown(dialogue_data)
        print(f"✓ Saved to: {filename}")
        
        print("\n✓ Dual LLM test completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_dual_llm_poetry()