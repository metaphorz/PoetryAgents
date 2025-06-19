#!/usr/bin/env python3
"""
Test script for the Poetry Agent Dialogue System
"""

from dialogue_manager import DialogueManager

def test_example_scenario():
    """Test the system with the example from Requirements.md"""
    
    # Example configuration from requirements
    config = {
        'theme': 'a walk in the snow',
        'num_agents': 2,
        'form': 'haiku',
        'poem_length': 2,  # 2 stanzas as per example
        'conversation_length': 1  # Each agent speaks once
    }
    
    print("Testing Poetry Agent Dialogue System")
    print("====================================")
    print(f"Configuration: {config}")
    print()
    
    try:
        # Create dialogue manager and generate dialogue
        manager = DialogueManager()
        dialogue_data = manager.generate_dialogue(config)
        
        # Display results
        formatted_output = manager.format_dialogue_output(dialogue_data)
        print("Generated Dialogue:")
        print("==================")
        print(formatted_output)
        
        return True
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_prose_scenario():
    """Test with prose poetry"""
    
    config = {
        'theme': 'morning coffee',
        'num_agents': 2,
        'form': 'prose',
        'poem_length': 4,  # 4 lines each
        'conversation_length': 1
    }
    
    print("\n" + "="*50)
    print("Testing Prose Poetry Scenario")
    print("="*50)
    print(f"Configuration: {config}")
    print()
    
    try:
        manager = DialogueManager()
        dialogue_data = manager.generate_dialogue(config)
        
        formatted_output = manager.format_dialogue_output(dialogue_data)
        print("Generated Dialogue:")
        print("==================")
        print(formatted_output)
        
        return True
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Running Poetry Agent Dialogue System Tests")
    print("=" * 50)
    
    # Test the haiku example
    success1 = test_example_scenario()
    
    # Test prose poetry
    success2 = test_prose_scenario()
    
    print("\n" + "="*50)
    if success1 and success2:
        print("All tests completed successfully!")
    else:
        print("Some tests failed - check output above.")