#!/usr/bin/env python3
"""
Script to systematically update tests for the new numbered model selection interface.
"""

import os
import re

def update_test_file(filepath, updates):
    """Update a test file with the given updates."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Apply updates
        for old_pattern, new_pattern in updates:
            content = re.sub(old_pattern, new_pattern, content, flags=re.MULTILINE | re.DOTALL)
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"✅ Updated {filepath}")
        return True
    except Exception as e:
        print(f"❌ Error updating {filepath}: {e}")
        return False

def main():
    """Main function to update all test files."""
    print("🔧 Updating tests for new numbered model selection interface...")
    
    # Define systematic updates needed across test files
    updates = [
        # Update expected config structure to include model selections
        (
            r"'agent1_llm': '(Claude|Gemini|OpenAI)',\s*'agent2_llm': '(Claude|Gemini|OpenAI)',\s*'use_emojis':",
            r"'agent1_llm': '\1',\n            'agent2_llm': '\2',\n            'agent1_claude_model': None,\n            'agent1_gemini_model': None,\n            'agent1_openai_model': None,\n            'agent2_claude_model': None,\n            'agent2_gemini_model': None,\n            'agent2_openai_model': None,\n            'use_emojis':"
        ),
        
        # Update test inputs to include model numbers
        (
            r"'(Claude|Gemini|OpenAI)',\s*#\s*agent\s*(\d+)\s*LLM\s*\n\s*'(yes|no|y|n)'",
            r"'\1',         # agent \2 LLM\n            '1',              # agent \2 model selection\n            '\3'"
        ),
        
        # Update model expectations in initialization tests
        (
            r'self\.assertEqual\(client\.model, "claude-3-5-sonnet-20241022"\)',
            'self.assertEqual(client.model, "claude-sonnet-4-20250514")  # Updated for dynamic discovery'
        ),
        
        # Add mocking for model discovery in relevant tests
        (
            r'def test_([^(]*)\(self\):',
            r'@patch("main.OpenAIClient", autospec=True)\n    @patch("main.GeminiClient", autospec=True)\n    @patch("main.LLMClient", autospec=True)\n    def test_\1(self, mock_llm, mock_gemini, mock_openai):'
        )
    ]
    
    # Test files to update
    test_files = [
        '/Users/paul/PoetryAgents/tests/user/test_coverage_main.py',
        '/Users/paul/PoetryAgents/tests/user/test_coverage_llm_client.py',
        '/Users/paul/PoetryAgents/tests/user/test_coverage_gemini_client.py',
        '/Users/paul/PoetryAgents/tests/user/test_coverage_dialogue_manager.py'
    ]
    
    print("Note: Due to the extensive nature of interface changes, these tests may need")
    print("manual review and adjustment. The new interface includes:")
    print("- Dynamic model discovery")
    print("- Numbered model selection (1-6)")
    print("- Additional config fields for model selections")
    print()
    
    success_count = 0
    for filepath in test_files:
        if os.path.exists(filepath):
            if update_test_file(filepath, updates):
                success_count += 1
        else:
            print(f"⚠️  File not found: {filepath}")
    
    print(f"\n📊 Summary: {success_count}/{len(test_files)} files processed")
    print("\n💡 Recommendation: Many tests will still need manual updates due to the")
    print("   significant interface changes. Consider focusing on integration tests")
    print("   rather than trying to fix all unit tests for now.")

if __name__ == "__main__":
    main()