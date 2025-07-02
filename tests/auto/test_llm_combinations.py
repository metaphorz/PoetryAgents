"""
Test script for different LLM combinations
"""

from dialogue_manager import DialogueManager

def test_llm_combinations():
    """Test all possible LLM combinations."""
    print("Testing all LLM combinations...")
    
    combinations = [
        ('Claude', 'Claude', 'Both agents use Claude'),
        ('Gemini', 'Gemini', 'Both agents use Gemini'),
        ('Claude', 'Gemini', 'Agent 1: Claude, Agent 2: Gemini'),
        ('Gemini', 'Claude', 'Agent 1: Gemini, Agent 2: Claude')
    ]
    
    for i, (agent1_llm, agent2_llm, description) in enumerate(combinations, 1):
        print(f"\n{'='*60}")
        print(f"TEST {i}: {description}")
        print('='*60)
        
        config = {
            'theme': f'starlight reflections test {i}',
            'num_agents': 2,
            'form': 'haiku',
            'poem_length': 1,
            'conversation_length': 1,
            'agent1_llm': agent1_llm,
            'agent2_llm': agent2_llm,
            'use_emojis': False  # Disable emojis for cleaner comparison
        }
        
        try:
            manager = DialogueManager()
            dialogue_data = manager.generate_dialogue(config)
            
            print(f"Title: {dialogue_data['title']}")
            print(f"Agents: {', '.join(dialogue_data['agents'])}")
            
            for entry in dialogue_data['conversation']:
                llm_used = entry.get('llm_used', 'Unknown')
                print(f"\n{entry['agent']} (via {llm_used}):")
                print("-" * 30)
                print(entry['poetry'])
            
            filename = manager.save_dialogue_to_markdown(dialogue_data)
            print(f"\n✓ Saved to: {filename}")
            
        except Exception as e:
            print(f"✗ Test {i} failed: {str(e)}")
    
    print(f"\n{'='*60}")
    print("All LLM combination tests completed!")
    print('='*60)

if __name__ == "__main__":
    test_llm_combinations()