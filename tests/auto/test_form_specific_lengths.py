"""
Test script for form-specific length handling
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dialogue_manager import DialogueManager

def test_form_specific_lengths():
    """Test all poetry forms with their appropriate length handling."""
    print("Testing form-specific length handling...")
    
    test_cases = [
        # Fixed-length forms (should use traditional lengths)
        {
            'name': 'Haiku (fixed length)',
            'config': {
                'theme': 'spring morning',
                'num_agents': 2,
                'form': 'haiku',
                'poem_length': 3,
                'length_unit': 'lines',
                'conversation_length': 1,
                'agent1_llm': 'Claude',
                'agent2_llm': 'Gemini',
                'use_emojis': False
            },
            'expected_desc': '3 lines (traditional haiku)'
        },
        {
            'name': 'Sonnet (fixed length)', 
            'config': {
                'theme': 'timeless love',
                'num_agents': 2,
                'form': 'sonnet',
                'poem_length': 14,
                'length_unit': 'lines',
                'conversation_length': 1,
                'agent1_llm': 'Claude',
                'agent2_llm': 'Gemini',
                'use_emojis': False
            },
            'expected_desc': '14 lines (traditional sonnet)'
        },
        # Variable-length forms
        {
            'name': 'Ballad (stanzas)',
            'config': {
                'theme': 'folk tale',
                'num_agents': 2,
                'form': 'ballad',
                'poem_length': 3,
                'length_unit': 'stanzas',
                'conversation_length': 1,
                'agent1_llm': 'Claude',
                'agent2_llm': 'Gemini',
                'use_emojis': False
            },
            'expected_desc': '3 stanzas'
        },
        {
            'name': 'Ghazal (couplets)',
            'config': {
                'theme': 'lost love',
                'num_agents': 2,
                'form': 'ghazal',
                'poem_length': 7,
                'length_unit': 'couplets',
                'conversation_length': 1,
                'agent1_llm': 'Claude',
                'agent2_llm': 'Gemini',
                'use_emojis': False
            },
            'expected_desc': '7 couplets'
        },
        {
            'name': 'Prose (paragraphs)',
            'config': {
                'theme': 'city life',
                'num_agents': 2,
                'form': 'prose',
                'poem_length': 2,
                'length_unit': 'paragraphs',
                'conversation_length': 1,
                'agent1_llm': 'Claude',
                'agent2_llm': 'Gemini',
                'use_emojis': False
            },
            'expected_desc': '2 paragraphs'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"TEST {i}: {test_case['name']}")
        print('='*60)
        
        try:
            manager = DialogueManager()
            dialogue_data = manager.generate_dialogue(test_case['config'])
            
            print(f"✓ Generated dialogue: '{dialogue_data['title']}'")
            print(f"✓ Form: {test_case['config']['form']}")
            print(f"✓ Expected length desc: {test_case['expected_desc']}")
            
            # Save and check markdown output
            filename = manager.save_dialogue_to_markdown(dialogue_data)
            print(f"✓ Saved to: {filename}")
            
            # Verify the length description in the saved file
            with open(filename, 'r') as f:
                content = f.read()
                if test_case['expected_desc'] in content:
                    print(f"✓ Length description correct in markdown")
                else:
                    print(f"✗ Length description not found in markdown")
            
            # Show conversation length description
            rounds = test_case['config']['conversation_length']
            agents = test_case['config']['num_agents']
            total_poems = rounds * agents
            print(f"✓ Conversation: {rounds} rounds ({total_poems} total poems)")
            
        except Exception as e:
            print(f"✗ Test {i} failed: {str(e)}")
    
    print(f"\n{'='*60}")
    print("Form-specific length tests completed!")
    print('='*60)

if __name__ == "__main__":
    test_form_specific_lengths()