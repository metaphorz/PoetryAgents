"""
Test script for Gemini API connection
"""

import sys
import os
# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from gemini_client import GeminiClient

def test_gemini_connection():
    """Test basic Gemini functionality."""
    try:
        print("Testing Gemini API connection...")
        
        # Initialize client
        client = GeminiClient()
        print("✓ Gemini client initialized successfully")
        
        # Test connection
        try:
            if client.test_connection():
                print("✓ Gemini API connection test passed")
            else:
                print("✗ Gemini API connection test failed")
                return False
        except Exception as e:
            print(f"✗ Gemini API connection test failed with error: {str(e)}")
            return False
        
        # Test poetry generation directly
        print("\nTesting poetry generation...")
        prompt = "Write a short haiku about coding"
        try:
            poetry = client.generate_poetry(prompt, max_tokens=100)
            
            print("Generated poetry:")
            print("─" * 40)
            print(poetry)
            print("─" * 40)
            
            print("\n✓ Gemini poetry generation test completed successfully")
            return True
        except Exception as e:
            print(f"✗ Poetry generation failed: {str(e)}")
            return False
        
    except Exception as e:
        print(f"✗ Gemini test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_gemini_connection()