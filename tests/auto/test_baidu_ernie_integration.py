#!/usr/bin/env python3
"""
Final test of OpenRouter integration with Baidu ERNIE model
"""

import os
import sys
sys.path.append('../..')  # Add parent directory for imports

from dotenv import load_dotenv
load_dotenv()

def test_baidu_ernie():
    """Test the complete flow with Baidu ERNIE model."""
    print("🧪 Testing OpenRouter with Baidu ERNIE 4.5 300B")
    print("=" * 55)
    
    # Verify API key
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found")
        return False
    
    print(f"✅ API Key: {api_key[:15]}...")
    
    try:
        from openrouter_client import OpenRouterClient
        
        # Test 1: Search for Baidu models
        print("\n🔍 Step 1: Searching for Baidu models...")
        matches = OpenRouterClient.search_models("baidu")
        
        if matches:
            print(f"✅ Found {len(matches)} Baidu model(s):")
            for i, match in enumerate(matches, 1):
                print(f"  {i}. {match['id']}")
                print(f"     {match.get('name', 'No name')}")
                
            # Should find: baidu/ernie-4.5-300b-a47b
            expected_model = "baidu/ernie-4.5-300b-a47b"
            found_expected = any(m['id'] == expected_model for m in matches)
            
            if found_expected:
                print(f"✅ Found expected model: {expected_model}")
                
                # Test 2: Initialize client
                print(f"\n🤖 Step 2: Initializing client with {expected_model}...")
                client = OpenRouterClient(expected_model)
                print(f"✅ Client model ID: {client.model_id}")
                
                # Test 3: Generate poetry
                print("\n📝 Step 3: Testing poetry generation...")
                test_prompt = "Write a haiku about artificial intelligence and poetry"
                
                try:
                    result = client.generate_poetry(test_prompt, max_tokens=100)
                    print("✅ Poetry generation successful!")
                    print("=" * 40)
                    print(result)
                    print("=" * 40)
                    
                    print("\n🎉 All tests passed! Baidu ERNIE model working perfectly!")
                    return True
                    
                except Exception as e:
                    print(f"❌ Poetry generation failed: {e}")
                    return False
            else:
                print(f"❌ Expected model {expected_model} not found")
                return False
        else:
            print("❌ No Baidu models found")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

# Simple execution test
if __name__ == "__main__":
    print("Starting test...")
    success = test_baidu_ernie()
    
    print("\n" + "=" * 55)
    print("🏁 FINAL RESULTS")
    print("=" * 55)
    
    if success:
        print("🎉 SUCCESS: OpenRouter + Baidu ERNIE integration working!")
        print("\n✅ Verified capabilities:")
        print("  • API authentication")
        print("  • Model discovery (Baidu ERNIE 4.5 300B)")
        print("  • Client initialization")
        print("  • Poetry generation")
        print("\n🚀 Ready for full Poetry Agent usage!")
    else:
        print("❌ FAILED: Some issues encountered")
        
    print("\nTo use in main app:")
    print("  1. python main.py")
    print("  2. Choose option 2 (OpenRouter)")
    print("  3. Search for 'baidu' for both agents")