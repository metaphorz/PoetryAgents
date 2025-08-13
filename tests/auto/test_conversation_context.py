#!/usr/bin/env python3
"""
Test script to demonstrate how conversation context is built.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from dialogue_manager import DialogueManager

def test_conversation_context():
    """Test the conversation context building method."""
    
    # Create a dialogue manager
    manager = DialogueManager()
    
    # Simulate a conversation history
    theme = "archery in the moonlight"
    conversation_history = [
        {
            'agent': 'Pierre',
            'poetry': 'Silver arrow flies through night\nDrawn by steady hand and will\nTarget gleams beneath moon\'s light',
            'round': 1,
            'agent_index': 0,
            'llm_used': 'Claude (Sonnet 3.5)'
        }
    ]
    
    # Build conversation context as Winston would see it
    context = manager._build_conversation_context(theme, conversation_history)
    
    print("=== Conversation Context for Winston ===")
    print(context)
    print("\n=== Example Prompt for Winston ===")
    
    from prompts import create_response_poetry_prompt
    prompt = create_response_poetry_prompt("Winston", context, "haiku", 3)
    print(prompt)

if __name__ == "__main__":
    test_conversation_context()