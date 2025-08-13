#!/usr/bin/env python3
"""
Quick test of OpenRouter integration
"""

import os
import sys
sys.path.append('../..')  # Add parent directory for imports

from dotenv import load_dotenv

load_dotenv()

def test_openrouter():
    """Test OpenRouter client functionality."""
    print("🧪 Testing OpenRouter Integration")
    print("=" * 40)
    
    # Check if API key is available
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found in environment")
        print("📝 Add OPENROUTER_API_KEY=your_key_here to .env file")
        return False
    
    try:
        from openrouter_client import OpenRouterClient
        
        # Test model search - focusing on Baidu
        print("🔍 Testing model search...")
        search_terms = ["Baidu", "Claude", "OpenAI"]
        
        for term in search_terms:
            print(f"\nSearching for '{term}':")
            matches = OpenRouterClient.search_models(term)
            if matches:
                print(f"  ✅ Found {len(matches)} matches")
                for i, match in enumerate(matches[:3], 1):
                    print(f"    {i}. {match['id']}")
            else:
                print(f"  ❌ No matches found")
        
        # Test client initialization and generation with Baidu
        print(f"\n🤖 Testing client with 'Baidu'...")
        baidu_matches = OpenRouterClient.search_models("Baidu")
        if baidu_matches:
            baidu_model = baidu_matches[0]['id']
            print(f"  Using Baidu model: {baidu_model}")
            client = OpenRouterClient(baidu_model)
            print(f"  Selected model: {client.model_id}")
            
            # Test poetry generation
            print("  Generating test poem...")
            result = client.generate_poetry("Write a haiku about testing", max_tokens=50)
            print(f"  ✅ Generated: {result[:50]}...")
        else:
            print("  ❌ No Baidu models found for testing")
        
        print("\n🎉 OpenRouter integration working!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_openrouter()