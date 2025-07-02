#!/usr/bin/env python3
"""
Demo run of the Poetry Agent Dialogue System with predefined inputs
"""

from dialogue_manager import DialogueManager

def demo_haiku_scenario():
    """Demo the example from Requirements.md"""
    
    config = {
        'theme': 'a walk in the snow',
        'num_agents': 2,
        'form': 'haiku',
        'poem_length': 2,  # 2 stanzas
        'conversation_length': 1
    }
    
    print("="*60)
    print("POETRY AGENT DIALOGUE GENERATOR - DEMO")
    print("="*60)
    print(f"Theme: {config['theme']}")
    print(f"Agents: {config['num_agents']}")
    print(f"Form: {config['form']}")
    print(f"Poem Length: {config['poem_length']} stanzas")
    print(f"Conversation Length: {config['conversation_length']} round")
    print("="*60)
    
    manager = DialogueManager()
    dialogue_data = manager.generate_dialogue(config)
    
    formatted_output = manager.format_dialogue_output(dialogue_data)
    print(formatted_output)

if __name__ == "__main__":
    demo_haiku_scenario()